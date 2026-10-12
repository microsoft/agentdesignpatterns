# Contributing

This project welcomes contributions and suggestions. Most contributions require you to
agree to a Contributor License Agreement (CLA) declaring that you have the right to,
and actually do, grant us the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

## Pull Request Workflow

All changes are submitted through pull requests to the protected `main` branch. Do not
push commits directly to `main`.

1. Create a focused topic branch from the latest `main`.
   - Repository collaborators can create the branch in this repository.
   - External contributors should fork the repository and create the branch in their fork.
2. Make and validate the change on the topic branch. For catalog changes, follow the
   [article contribution guide](docs/contributing.md).
3. Open a pull request targeting this repository's `main` branch.
4. Address review feedback and required status checks. If `main` advances, rebase the
   topic branch onto the latest `main`; do not merge `main` into the topic branch.
5. Preserve the pull request's individual commits. Do not squash them or add a merge
   commit. Maintainers merge approved pull requests using GitHub's **Rebase and merge**
   method.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
