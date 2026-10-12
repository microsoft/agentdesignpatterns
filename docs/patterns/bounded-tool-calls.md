---
id: bounded-tool-calls
title: Bounded Tool Calls
description: Limit tool execution to prevent runaway agent loops.
type: pattern
category: Reliability and control
tags:
  - reliability
  - resource-control
  - tool-use
related:
  - unbounded-retries
---

# Bounded Tool Calls

## Description

Set an explicit maximum number of tool calls for each agent run. Count every attempted call, including calls that fail, and stop before invoking a tool when the budget is exhausted.

The agent should return a clear explanation when it reaches the limit, including what it completed and what remains unfinished. A call budget prevents accidental loops from consuming time, tokens, service quotas, or money indefinitely.

## Applicability

Use this pattern when an agent can select and invoke tools autonomously, especially when:

- A tool result can cause the model to request another tool.
- A task interacts with metered or rate-limited services.
- A tool has side effects.
- A malformed result could keep the agent in a repeated plan-and-act cycle.

Choose the limit for the task rather than using one global value. A lookup may need only a few calls, while a repository-wide change may require a larger budget. Combine the budget with cancellation, elapsed-time limits, and per-tool authorization where the risk warrants it.

## Implementation

The following [TypeScript](https://www.typescriptlang.org/docs/) wrapper enforces a shared budget around tools supplied to a [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) or [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry) agent. The wrapper counts failed attempts because they still consume resources.

```typescript
type AgentTool<TInput, TOutput> = (input: TInput) => Promise<TOutput>;

class ToolCallLimitExceeded extends Error {
  constructor(
    readonly limit: number,
    readonly toolName: string,
  ) {
    super(`Tool call limit of ${limit} reached before calling ${toolName}.`);
  }
}

class ToolCallBudget {
  private calls = 0;

  constructor(readonly limit: number) {
    if (!Number.isInteger(limit) || limit < 1) {
      throw new RangeError("Tool call limit must be a positive integer.");
    }
  }

  async invoke<TInput, TOutput>(
    toolName: string,
    tool: AgentTool<TInput, TOutput>,
    input: TInput,
  ): Promise<TOutput> {
    if (this.calls >= this.limit) {
      throw new ToolCallLimitExceeded(this.limit, toolName);
    }

    this.calls += 1;
    return tool(input);
  }

  get remaining(): number {
    return this.limit - this.calls;
  }
}
```

Create one `ToolCallBudget` for an agent run, then expose only wrapped tool handlers to the agent:

```typescript
const budget = new ToolCallBudget(8);

const searchTool = (query: string) =>
  budget.invoke("search", searchDocuments, query);

const updateTool = (change: ProposedChange) =>
  budget.invoke("update", applyProposedChange, change);
```

[Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) also supports [bounded agent loops](https://learn.microsoft.com/en-us/agent-framework/agents/looping). An iteration limit and a tool-call budget are complementary: one limits complete reasoning iterations, while the other limits calls at the tool boundary.

## References

- [Microsoft Foundry overview](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)
- [Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Agent Looping — Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/agents/looping)
- [TypeScript documentation](https://www.typescriptlang.org/docs/)
- [Azure AI Projects client library for JavaScript](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects)