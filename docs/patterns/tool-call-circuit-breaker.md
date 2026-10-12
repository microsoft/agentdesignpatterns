---
id: tool-call-circuit-breaker
title: Tool Call Circuit Breaker
description: Stop agent tools from repeatedly calling an unhealthy dependency.
type: pattern
category: Tool Calling
tags:
  - fault-tolerance
  - reliability
  - tool-use
related:
  - bounded-tool-calls
---

# Tool Call Circuit Breaker

## Pattern

Place a circuit breaker at the boundary between an agent tool and each remote dependency whose failures can persist across calls. The breaker records qualifying dependency failures and moves through three states:

- **Closed:** Calls reach the dependency. Consecutive qualifying failures count toward a threshold.
- **Open:** Calls fail immediately without contacting the dependency.
- **Half-open:** After a cooldown, one controlled probe call determines whether the dependency has recovered.

```mermaid
stateDiagram-v2
    [*] --> Closed
    Closed --> Closed: Call succeeds
    Closed --> Open: Failure threshold reached
    Open --> Open: Fail fast during cooldown
    Open --> HalfOpen: Cooldown expires
    HalfOpen --> Closed: Probe succeeds
    HalfOpen --> Open: Probe fails
```

Maintain a separate breaker for each independently failing tool or backend. When a circuit is open, return an explicit temporary-unavailability result that the agent can report or use to select an approved fallback. Do not let the model repeatedly probe the dependency or fabricate a successful result.

Unlike [Contextual Tool Authorization](contextual-tool-authorization.md), which decides whether a call is permitted, or [Bounded Tool Calls](bounded-tool-calls.md), which caps per-run call volume, this pattern suppresses calls based on dependency health across operations.

## Applicability

Use this pattern when an agent tool calls a remote service that can remain degraded across multiple requests, especially when:

- Many agent runs share the same dependency.
- Repeated calls would amplify load during an outage.
- Calls consume model tokens, service quotas, or metered capacity.
- Other tools can still complete useful work while one dependency recovers.
- The application can classify which failures indicate dependency health.

Count failures such as connection errors, timeouts, and selected service-unavailable responses. Do not trip the circuit for invalid tool arguments, denied authorization, policy rejection, or other caller-specific failures that do not indicate an unhealthy dependency.

A circuit breaker complements but does not replace bounded retries and tool-call budgets. A retry policy governs a small number of attempts for one operation. A tool-call budget limits total work during one agent run. A circuit breaker suppresses calls across operations while a dependency is likely to remain unhealthy.

Choose thresholds and cooldowns from the dependency's latency, recovery behavior, and service objectives. For horizontally scaled applications, use a gateway or shared state when every instance must observe the same circuit; an in-memory breaker protects only one process.

## Implementation

The [Azure Architecture Center circuit-breaker guidance](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) defines the closed, open, and half-open state transitions. The following TypeScript abstraction applies those transitions around a tool handler. It permits only one half-open probe and counts only failures classified as dependency-health signals.

```typescript
type CircuitState = "closed" | "open" | "half-open";
type AttemptKind = "normal" | "probe";

interface CircuitBreakerOptions {
  failureThreshold: number;
  openDurationMs: number;
  shouldCountFailure: (error: unknown) => boolean;
  now?: () => number;
}

class ToolCircuitOpenError extends Error {
  constructor(
    readonly toolName: string,
    readonly retryAfterMs: number,
  ) {
    super(
      retryAfterMs > 0
        ? `${toolName} is unavailable; retry after ${retryAfterMs} ms.`
        : `${toolName} is unavailable; a recovery probe is already running.`,
    );
  }
}

class ToolCircuitBreaker {
  private state: CircuitState = "closed";
  private failures = 0;
  private openedAt = 0;
  private probeInFlight = false;
  private readonly now: () => number;

  constructor(
    private readonly toolName: string,
    private readonly options: CircuitBreakerOptions,
  ) {
    if (
      !Number.isInteger(options.failureThreshold) ||
      options.failureThreshold < 1
    ) {
      throw new RangeError("failureThreshold must be a positive integer.");
    }
    if (options.openDurationMs <= 0) {
      throw new RangeError("openDurationMs must be greater than zero.");
    }

    this.now = options.now ?? Date.now;
  }

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    const attempt = this.startAttempt();

    try {
      const result = await operation();
      this.recordSuccess(attempt);
      return result;
    } catch (error) {
      this.recordFailure(attempt, error);
      throw error;
    } finally {
      if (attempt === "probe" && this.state === "half-open") {
        this.probeInFlight = false;
      }
    }
  }

  get currentState(): CircuitState {
    return this.state;
  }

  private startAttempt(): AttemptKind {
    if (this.state === "open") {
      const retryAfterMs =
        this.openedAt + this.options.openDurationMs - this.now();

      if (retryAfterMs > 0) {
        throw new ToolCircuitOpenError(this.toolName, retryAfterMs);
      }

      this.state = "half-open";
    }

    if (this.state === "half-open") {
      if (this.probeInFlight) {
        throw new ToolCircuitOpenError(this.toolName, 0);
      }

      this.probeInFlight = true;
      return "probe";
    }

    return "normal";
  }

  private recordSuccess(attempt: AttemptKind): void {
    if (attempt === "probe") {
      this.state = "closed";
      this.failures = 0;
      this.probeInFlight = false;
    } else if (this.state === "closed") {
      this.failures = 0;
    }
  }

  private recordFailure(attempt: AttemptKind, error: unknown): void {
    if (!this.options.shouldCountFailure(error)) {
      return;
    }

    if (attempt === "probe") {
      this.openCircuit();
      return;
    }

    if (this.state !== "closed") {
      return;
    }

    this.failures += 1;
    if (this.failures >= this.options.failureThreshold) {
      this.openCircuit();
    }
  }

  private openCircuit(): void {
    this.state = "open";
    this.openedAt = this.now();
    this.failures = 0;
    this.probeInFlight = false;
  }
}
```

Create one breaker for the inventory dependency and wrap the handler before exposing it as a tool:

```typescript
interface InventoryService {
  availableUnits(sku: string): Promise<number>;
}

declare const inventoryService: InventoryService;

class DependencyUnavailableError extends Error {}

const inventoryBreaker = new ToolCircuitBreaker("get_inventory", {
  failureThreshold: 5,
  openDurationMs: 30_000,
  shouldCountFailure: (error) =>
    error instanceof DependencyUnavailableError,
});

async function getInventory(sku: string): Promise<number> {
  return inventoryBreaker.execute(() =>
    inventoryService.availableUnits(sku),
  );
}
```

The service client should translate connection failures, timeouts, and selected transient responses into `DependencyUnavailableError`. Input and authorization failures pass through without changing circuit health.

Register the wrapped `getInventory` handler as a function tool with [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) or a [Microsoft Foundry prompt agent](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling). Translate `ToolCircuitOpenError` into a structured tool failure that identifies temporary unavailability and the remaining cooldown. The agent may use another approved source or report the limitation, but it should not retry before the circuit permits a probe.

In a distributed deployment, place equivalent circuit-breaking behavior in a shared service layer or gateway when instances must coordinate dependency health. Keep tool-level telemetry for state transitions, rejected calls, probes, and recovery so operators can distinguish an open circuit from a model or tool-selection failure.

## References

- [Circuit Breaker pattern — Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
- [Retry pattern — Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
- [Transient fault handling — Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)
- [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Use function calling with Microsoft Foundry agents](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling)
