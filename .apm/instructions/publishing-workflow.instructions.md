---
description: "Project-wide GitHub publishing workflow requiring pull requests to main, rebase-only merges, and preserved commits."
name: "Publishing Workflow"
---

# Publishing Workflow

- Treat `main` as protected. Never commit or push directly to `main`.
- Create a focused topic branch from the latest `origin/main`. Contributors without repository write access should work from a fork.
- Submit every change through a pull request targeting `main`.
- Keep the topic branch current by rebasing it onto `origin/main`; do not merge `main` into the topic branch.
- Preserve the pull request's individual commits. Do not squash commits or create merge commits.
- Use GitHub's **Rebase and merge** method when merging an approved pull request.
- Run the validation required for the changed files before requesting review.
- Do not merge a pull request unless the user explicitly asks and the repository's required reviews and status checks have passed.
