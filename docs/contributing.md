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
  - unbounded-retries
---
```

Use `type: anti-pattern` for anti-patterns. Every metadata key shown above is required. Use an empty array when an article has no related entries:

```yaml
related: []
```

## Article Structure

After the title, patterns must contain these level-two sections in order:

1. `Description`
2. `Applicability`
3. `Implementation`
4. `References`

Anti-patterns must contain:

1. `Description`
2. `Issue`
3. `Implementation`
4. `References`

The site renders the frontmatter description as a caption below the article title. Do not repeat it manually. The site also generates the `Related` section, categorized catalog indexes, and tag index from frontmatter.

Implementation examples should use [TypeScript](https://www.typescriptlang.org/docs/) and Microsoft technologies where practical, including [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry) and [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/). Keep examples focused on the behavior being described and omit unrelated setup. An anti-pattern implementation must be clearly identified as an example that readers should not adopt.

In the Implementation section, hyperlink every named tool, framework, programming language, SDK, service, or other technology to its canonical product overview or reference documentation. The References section must also contain each of those sources, even when the same link appears inline. This makes the implementation readable in place while preserving a complete source list.

References should favor Microsoft Learn, Microsoft Tech Community, and other Microsoft sources. Include relevant primary documentation from other publishers when it helps readers apply or understand the article.

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