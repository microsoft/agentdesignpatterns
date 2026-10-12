---
name: author-article
description: "Author, revise, or review pattern and anti-pattern articles for the Agent Design Patterns catalog. Use when creating catalog content, changing article frontmatter or structure, writing Microsoft-stack TypeScript implementations, adding canonical technology links and references, assigning categories or tags, or connecting related articles."
argument-hint: "Describe the pattern or anti-pattern to author or revise"
---

# Author Article

Create or revise a catalog article by applying the project-wide Article Standards instruction and using the appropriate starter template.

## Workflow

1. Inspect the existing articles and indexes before choosing an ID, category, tags, or related IDs:
   - `docs/patterns/`
   - `docs/anti-patterns/`
   - `docs/patterns/index.md`
   - `docs/anti-patterns/index.md`
2. Determine whether the article is a pattern or anti-pattern.
3. Start from the corresponding template:
   - [Pattern template](./assets/pattern-template.md)
   - [Anti-pattern template](./assets/anti-pattern-template.md)
4. Research and write the article in the matching `docs/` directory, following the ambient Article Standards instruction.
5. Run the strict site build:

   ```shell
   bash tools/build.sh
   ```

6. Fix all metadata, structure, navigation, generated-link, and build errors before finishing.
