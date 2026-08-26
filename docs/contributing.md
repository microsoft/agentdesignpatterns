---
title: Contributing
description: Guidance for contributing articles to Agent Design Patterns.
---

# Contributing

Contributions may include concise implementation examples when code helps explain the guidance.

For example:

```python
for attempt in range(max_tool_calls):
	result = call_tool()
	if task_is_complete(result):
		break
else:
	report_incomplete_task()
```

Keep examples focused on the behavior being described and omit unrelated setup.

## Run the Site Locally

From the repository root, start the local development server:

```shell
./tools/serve.sh
```

Open `http://127.0.0.1:8000`. The server rebuilds the site when documentation files change.

Before submitting a change, run the strict production build used by CI:

```shell
./tools/build.sh
```