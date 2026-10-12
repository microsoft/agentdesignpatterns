---
description: "Project-wide standards for maintaining Agent Design Patterns catalog articles, including metadata, structure, Microsoft-stack implementations, canonical links, references, categories, tags, related articles, generated site behavior, and validation."
name: "Article Standards"
---

# Agent Design Article Standards

## Audience and Voice

Write for engineers and technical leaders who design, implement, or review production AI agents. Favor concise, actionable engineering guidance over general AI explanation.

Use direct language. Define the behavior precisely, explain its operational consequences, and keep examples focused on the pattern or anti-pattern. Do not add setup that is unrelated to the behavior being demonstrated.

## File Location and Identity

- Patterns live in `docs/patterns/<id>.md`.
- Anti-patterns live in `docs/anti-patterns/<id>.md`.
- `id` must be unique across both article types.
- The ID and filename stem must match and use lowercase kebab-case.

## Frontmatter

Every article requires these keys:

```yaml
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
```

Rules:

- `type` is exactly `pattern` or `anti-pattern`.
- `description` is a short caption that completes the title; the site renders it below the heading.
- Do not repeat the description manually in the body.
- `category` is one human-readable classification. Reuse an existing category when it fits.
- `tags` is an array of lowercase topic labels. Prefer existing tags when they express the same concept.
- `related` is an array of existing article IDs. Use `related: []` when there are none.
- Do not add a `maturity` key. GitHub branches and pull requests manage editorial maturity.

The site hook validates this metadata, groups index pages by category, renders tags as navigable links, and turns `related` IDs into a Related section. Do not manually add a Related section.

## Pattern Structure

After the level-one title, use exactly these level-two sections in order:

1. `Description`
2. `Applicability`
3. `Implementation`
4. `References`

### Description

Define the pattern and its essential behavior. State what the implementation must do, not merely its intended outcome.

### Applicability

Explain when to use the pattern, the conditions that make it useful, important boundaries, and any complementary controls. Prefer specific scenarios or a concise bullet list.

### Implementation

Show how to implement the pattern. Use a Microsoft technology stack where practical:

- Microsoft Foundry and Foundry agents
- Microsoft Agent Framework
- TypeScript
- Azure services and official Microsoft SDKs
- Other Microsoft-native technologies appropriate to the pattern

Use real, current APIs when presenting code as directly usable. If exact framework integration would obscure the behavior, a focused TypeScript abstraction is acceptable, but describe clearly how it connects to the Microsoft stack. Do not imply that illustrative code is a complete production implementation.

## Anti-Pattern Structure

After the level-one title, use exactly these level-two sections in order:

1. `Description`
2. `Issue`
3. `Implementation`
4. `References`

### Description

Define the undesirable behavior without prescribing the solution.

### Issue

Explain why the behavior is harmful. Cover concrete reliability, cost, security, operability, data-integrity, or user-experience consequences as applicable. Explain the safer direction without turning the section into an unrelated pattern article.

### Implementation

Show a concise example of the anti-pattern so readers can recognize it. State immediately before the code that the implementation is intentionally unsafe or unreliable and must not be adopted. Explain how the example can fail in the relevant Microsoft agent stack and summarize the replacement behavior.

## Technology Links

In the Implementation section, hyperlink the first meaningful mention of every named:

- Product or service
- Framework or SDK
- Programming language
- API, protocol, schema, or tool
- Other technology-stack element

Link to the canonical product overview or reference documentation. Examples:

- [Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [TypeScript](https://www.typescriptlang.org/docs/)

Do not link to search results, unofficial summaries, or marketing pages when a canonical overview or reference exists.

## References

The References section is required and must be complete with respect to the Implementation section.

- Include every canonical source linked from implementation prose.
- Include sources for implementation APIs, SDKs, and important behavior.
- Prefer Microsoft Learn, Microsoft Tech Community, official Microsoft product pages, and Microsoft-owned source repositories.
- Use other publishers' primary sources when they own the relevant technology or specification, such as TypeScript, OpenAI APIs, or industry schemas.
- Use descriptive Markdown link text that identifies the document and publisher or product.
- Do not cite a source that was not consulted.
- Avoid duplicate entries and bare URLs.

Inline links make the implementation readable in context; the References section remains the complete source list even when this repeats a URL.

## Generated Site Behavior

`hooks/catalog.py` owns generated behavior:

- The frontmatter description becomes the article caption.
- Categories populate the home, Patterns, and Anti-Patterns indexes.
- Material for MkDocs turns tags into links and builds the Tags page.
- Related IDs become links in a generated Related section.
- Required metadata and section order are build validated.

Author source content for that contract rather than reproducing generated output manually.

## Validation

Run:

```shell
bash tools/build.sh
```

MkDocs strict mode and the catalog hook must complete successfully. Treat warnings about metadata, links, section order, navigation, or theme configuration as failures to resolve.
