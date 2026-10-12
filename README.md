# Agent Design Patterns

This repository publishes a catalog of patterns and anti-patterns for building reliable AI agents.

The site uses Material for MkDocs. Article metadata drives categorized indexes, tag navigation, description captions, and related-article links. The build validates each article's frontmatter and required section structure.

## Run Locally

```shell
./tools/serve.sh
```

Open `http://127.0.0.1:8000`. The development server rebuilds the site when documentation files change.

Before submitting a change, run the strict production build:

```shell
./tools/build.sh
```

See the [contribution guide](docs/contributing.md) for the pattern and anti-pattern authoring requirements.
