# Lrssn style guide

This repo is for all the different style guides I'll use going forward.

## [Git](./src/git/Git.md)

A guide for how to create, structure and maintain git repos. This also covers GitHub issues and pull requests.

## [JavaScript](./src/javascript/Javascript.md)

A style guide for JavaScript. Heavily based on the [Google styleguide](https://google.github.io/styleguide/jsguide.html).

## [TypeScript](./src/typescript/Typescript.md)

A style guide for TypeScript. Heavily based on the [Google styleguide](https://google.github.io/styleguide/tsguide.html).

## [Docker](./src/docker/Docker.md)

A style guide for Docker images and development. Based on Docker's [building best practices](https://docs.docker.com/build/building/best-practices/).

## [Go](./src/go/Go.md)

A style guide for the Go language. Heavily based on the [Google styleguide](https://google.github.io/styleguide/go/) and [Effective Go](https://go.dev/doc/effective_go).

## [Bash](./src/bash/Bash.md)

A guide for creating bash scripts for both Windows and Linux. Heavily based on the [Google styleguide](https://google.github.io/styleguide/shellguide.html).

## [Markdown](./src/markdown/Markdown.md)

A guide for writing good markdown files. Heavily based on the [Google styleguide](https://google.github.io/styleguide/docguide/style.html).

## [LaTeX](./src/latex/Latex.md)

A style guide and theme for writing different types of documents and plugins in LaTeX. The theme uses the [color palette](./src/colors/Colors.md).

## [C++](./src/cpp/Cpp.md)

A style guide for C++. Heavily based on the [Google styleguide](https://google.github.io/styleguide/cppguide.html).

## [Python](./src/python/Python.md)

A style guide for Python. Heavily based on the [Google styleguide](https://google.github.io/styleguide/pyguide.html) and [PEP 8](https://peps.python.org/pep-0008/).

## [Perl](./src/perl/Perl.md)

A style guide for Perl. Based on [perlstyle](https://perldoc.perl.org/perlstyle) and Perl Best Practices.

## [Rust](./src/rust/Rust.md)

A style guide for Rust. Based on the [Rust style guide](https://doc.rust-lang.org/style-guide/) and the [Rust API guidelines](https://rust-lang.github.io/api-guidelines/).

## [Haskell](./src/haskell/Haskell.md)

A style guide for Haskell. Based on [Johan Tibell's style guide](https://github.com/tibbe/haskell-style-guide) and the [Kowainik style guide](https://kowainik.github.io/posts/2019-02-06-style-guide).

## [Ruby](./src/ruby/Ruby.md)

A style guide for Ruby. Based on the community [Ruby Style Guide](https://rubystyle.guide/) and [RuboCop](https://rubocop.org/).

## [Agentic development](./src/agentic/Agentic.md)

A guide for working with AI coding agents: the instruction file, scoping tasks, permissions, verification, Git and review.
Based on the [AGENTS.md](https://agents.md/) convention and the [Claude Code documentation](https://code.claude.com/docs/).

## Checks

Pull requests run [markdownlint](https://github.com/DavidAnson/markdownlint-cli2) and a link check via GitHub Actions.
To lint locally, run `npx markdownlint-cli2`.

## Config files

Most guides have a `Tooling` section with linter and formatter settings.
The same settings are available as ready to copy files next to each guide, for example [`src/cpp/.clang-format`](./src/cpp/.clang-format).
They are generated from the code blocks in the guides, and CI fails if they differ.
After changing a block in a guide, run `scripts/configs.py --write` to update the files.

## Wiki

The guides are mirrored to the [GitHub wiki](https://github.com/Lrssn-blog/Style-guide/wiki) whenever `master` changes.
Do not edit the wiki directly, since the next sync overwrites it.
Edit the Markdown files in this repository instead.
The sync is done by [`scripts/sync-wiki.sh`](./scripts/sync-wiki.sh) in the `Wiki` workflow.
