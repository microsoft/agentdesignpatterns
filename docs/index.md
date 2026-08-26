# Pattern: Bounded Tool Calls

Limit the number of tool calls an agent may make while completing a task.

A call budget prevents accidental loops from consuming resources indefinitely. Track each tool call, stop when the budget is exhausted, and return a clear explanation of what remains unfinished.

The budget should match the task. A small lookup may need only a few calls, while a repository-wide change may need more.

```python
for attempt in range(max_tool_calls):
	result = call_tool()
	if task_is_complete(result):
		break
else:
	report_incomplete_task()
```