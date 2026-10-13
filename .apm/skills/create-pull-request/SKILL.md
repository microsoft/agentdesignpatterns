---
name: create-pull-request
description: "Create or update a GitHub pull request for the current branch and automatically request a code review from brendonmatheson. Use when opening, publishing, submitting, or preparing a pull request for review."
argument-hint: "Optional pull request title or issue number"
---

# Create Pull Request

Create a complete pull request from the current topic branch and request review from `brendonmatheson`.

## Workflow

1. Inspect the current branch, working tree, upstream, commits relative to the base branch, and any existing pull request for the branch.
2. Stop if the current branch is `main`, the branch has no commits to submit, or required changes have not been published. Do not push unless the user explicitly asks.
3. Read the repository's pull request template before drafting the body:
   - `.github/pull_request_template.md`
   - `.github/PULL_REQUEST_TEMPLATE/`
4. Read the repository's contributor guidance and changed-file validation instructions. Run the smallest required validation against the committed tree so unrelated local changes cannot affect the result.
5. Draft the title and body from the submitted commits and linked issue. Preserve all template headings, comments, checklist items, and ordering. Record each exact validation command and whether it passed or failed. Clearly identify checks that were not run.
6. Create the pull request with the GitHub CLI, targeting `main` unless the user specifies another base. If a pull request already exists for the branch, update it instead of creating a duplicate.
7. Automatically request a code review from `brendonmatheson`. Prefer the GitHub REST endpoint so deprecated Projects Classic GraphQL fields cannot prevent the request:

   ```shell
   gh api --method POST \
     "repos/{owner}/{repo}/pulls/<pull-number>/requested_reviewers" \
     -f "reviewers[]=brendonmatheson"
   ```

8. Verify the pull request URL, base and head branches, state, body, and requested reviewers. Report the URL and validation results.

## Review Request Failures

- A review request is not complete until GitHub lists `brendonmatheson` under requested reviewers.
- If GitHub rejects the request because `brendonmatheson` authored the pull request, report that self-review is prohibited and ask for a different reviewer. Do not substitute an assignee or claim that review was requested.
- Surface authentication, authorization, branch, validation, and API failures explicitly. Do not return success-shaped output after a failed operation.

## Repository Rules

- Never commit or push directly to `main`.
- Do not commit, amend, force-push, merge, or rebase unless the user explicitly requests that operation.
- Preserve individual commits; do not squash or create merge commits.
- Do not merge the pull request unless the user explicitly asks and all required reviews and status checks have passed.
