# AGENTS.md

Instructions for AI coding agents working in this repository.
For people, see `README.md`.

## Overview

This repository holds the Lrssn style guides.
There is one guide per topic in `src/<topic>/`, and no application code.

## Commands

- Lint the Markdown: `npx markdownlint-cli2`
- Check that the config files match the guides: `scripts/configs.py`
- Regenerate the config files after changing a guide: `scripts/configs.py --write`
- Check the links: `lychee --config .lychee.toml '**/*.md'`

Run the first two before you say a task is done.

## Layout

- `src/<topic>/<Topic>.md`: the guide for one topic.
- `src/<topic>/`: ready to copy config files, generated from code blocks in the guide.
- `scripts/`: the config check and the wiki sync.
- `.github/workflows/`: CI and the wiki mirror.

## Conventions

- Follow the [Markdown style guide](./src/markdown/Markdown.md).
  Write one sentence per line.
- Match the tone and the section order of the existing guides.
- Never edit a generated config file by hand.
  Change the code block in the guide, and run `scripts/configs.py --write`.
- Never edit the GitHub wiki.
  It is overwritten from this repository.
- Add a new guide to the list in `README.md`.

## Git and pull requests

- Follow the [Git style guide](./src/git/Git.md) and the [Agentic development style guide](./src/agentic/Agentic.md).
- `main` is the root branch.
  Work on a branch from `main`, and never commit to `main`.
- Open a pull request only when asked, against `main`.

## Boundaries

Ask first:

- Changing CI, the scripts or the lint configuration.
- Adding a dependency.

Never:

- Skip, weaken or disable a check to make it pass.
- Commit secrets.
