---
id: unbounded-retries
title: Unbounded Retries
description: Avoid retry loops that repeat failed actions without changing strategy.
type: anti-pattern
category: Reliability and control
tags:
  - error-handling
  - reliability
  - retries
related:
  - bounded-tool-calls
---

# Unbounded Retries

## Anti-Pattern

An agent repeats a failed operation indefinitely without a retry limit, backoff, cancellation path, or meaningful change in strategy.

## Issue

Repeated identical attempts waste time and can amplify load on an unhealthy service. They also hide the original failure behind a long sequence of secondary errors.

Unbounded retries are especially dangerous for agent tools because each attempt may consume model tokens, service quotas, or money. Repeated calls can also duplicate side effects when an operation is not idempotent. Permanent failures, such as invalid input or denied authorization, cannot be corrected by trying again.

A reliable implementation classifies failures, retries only transient faults, uses backoff and jitter, and preserves the last useful error when the retry budget is exhausted.

## Implementation

The following [TypeScript](https://www.typescriptlang.org/docs/) example demonstrates the anti-pattern. **Do not use this implementation.** It retries every error immediately, discards diagnostic information, and has no cancellation or termination condition.

```typescript
interface Agent {
  run(prompt: string): Promise<string>;
}

async function runUntilSuccess(
  agent: Agent,
  prompt: string,
): Promise<string> {
  while (true) {
    try {
      return await agent.run(prompt);
    } catch {
      // Anti-pattern: every failure is retried forever without delay.
    }
  }
}
```

In a [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry) or [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) application, this loop can repeatedly invoke the model and any tools selected by the agent. Replace it with a bounded retry policy that distinguishes transient failures from permanent failures and returns control to the caller after the final attempt.

## References

- [Microsoft Foundry overview](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)
- [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [TypeScript documentation](https://www.typescriptlang.org/docs/)
- [Retry pattern — Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
- [Transient fault handling — Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)
- [Agent Looping — Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/agents/looping)