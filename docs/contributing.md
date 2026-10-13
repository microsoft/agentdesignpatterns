---
title: Contributing
description: Guidance for contributing articles to Agent Design Patterns.
---

# Contributing

Articles use YAML frontmatter so the site can validate and organize the catalog. IDs must be unique lowercase kebab-case values. Categories provide the groupings on catalog indexes, tags are rendered as navigable links, and `related` contains the IDs of related patterns or anti-patterns.

## Submission Workflow

Create a topic branch from the latest `main`. If you do not have write access to the
repository, create the branch in your fork. Submit the article through a pull request
targeting `main`; direct pushes to `main` are not accepted.

Keep each commit meaningful and preserve the pull request's individual commits. If the
base branch advances, rebase your topic branch onto the latest `main` rather than merging
`main` into it. Do not squash commits or create merge commits. Maintainers merge approved
pull requests using GitHub's **Rebase and merge** method after required reviews and checks
pass.

Pattern frontmatter follows this format:

```yaml
---
id: bounded-tool-calls
title: Bounded Tool Calls
description: Limit tool execution to prevent runaway agent loops.
type: pattern
category: Reliability and control
tags:
  - reliability
  - tool-use
related:
  - tool-call-circuit-breaker
---
```

Use `type: anti-pattern` for anti-patterns. Every metadata key shown above is required. Use an empty array when an article has no related entries:

```yaml
related: []
```

## Article Structure

After the title, patterns must contain these level-two sections in order:

1. `Pattern`
2. `Applicability`
3. `Implementation`
4. `References`

Anti-patterns must contain:

1. `Anti-Pattern`
2. `Issue`
3. `Implementation`
4. `Recommended Approach`
5. `References`

The site renders the frontmatter description as a caption below the article title. Do not repeat it manually. The site also generates the `Related` section, category-first left navigation, categorized catalog indexes, and tag index from frontmatter.

Implementation examples should use Python and TypeScript with Microsoft technologies where practical, including [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry) and [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/). Keep examples focused on the behavior being described and omit unrelated setup. An anti-pattern implementation must be clearly identified as an example that readers should not adopt. Put corrected code and prescriptive replacement guidance in Recommended Approach.

## Language-Specific Samples

Every executable sample must provide equivalent Python and TypeScript implementations without duplicating the surrounding explanation. Put each pair in linked content tabs, with Python first:

````markdown
=== "Python"

    ```python
    def example() -> None:
        ...
    ```

=== "TypeScript"

    ```typescript
    function example(): void {
      // ...
    }
    ```
````

Use the labels and fence identifiers exactly as shown. The strict build rejects a Python or TypeScript fence outside a paired group, reversed or duplicate tabs, mismatched labels and fence identifiers, unsupported language identifiers, malformed indentation, and missing translations.

The site initially displays Python. Selecting either language on any sample updates every sample on the page and stores the preference in browser-local storage, so the same language remains selected across articles and later sessions.

Mermaid diagrams and supporting configuration or policy fragments such as YAML, Rego, and shell commands remain ordinary fenced blocks without language tabs. If an executable translation is temporarily unavailable, do not silently show another language under the selected label. Add an explicit prose explanation and complete the missing implementation before submitting the article.

In Implementation and Recommended Approach, hyperlink technologies that materially support the agent behavior, architecture, or APIs central to the example. The References section must also contain each of those sources, even when the same link appears inline.

References should favor Microsoft Learn, Microsoft Tech Community, and other Microsoft sources. Include relevant primary documentation from other publishers when it helps readers apply or understand the article. Do not add general-purpose language, credential, serialization, or transport documentation for incidental implementation mechanics unless the article depends on behavior specific to that technology.

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