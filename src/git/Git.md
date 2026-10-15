# Git style guide

[TOC]

## Repository

### Documents

Every repository should have most of the following documents, even if they are empty.

#### .editorconfig

An editorconfig will make sure every editor behaves the same. For more information see [editorconfig.org](https://editorconfig.org/).
What every editorconfig should include are:

- indent_style: The preferred style is spaces.
  Go is the exception, as `gofmt` indents with tabs (see the [Go style guide](../go/Go.md#editorconfig)).
- indent_size: The preferred size is 4.
- tab_width: This should match the indent_size.
- end_of_line: LF is preferred for intercompatibility.
- charset: While there is an argument for using UTF-16 we will stick to UTF-8 due to using less memory.
- trim_trailing_whitespace: The preferred style is true.
- insert_final_newline: The preferred style is true.
- max_line_length: The preferred value is 80.
- root: Set to true unless there are other editorconfigs in the repository.

These may look different depending on the language but an example is included in [Templates](https://github.com/Lrssn-blog/Templates).

#### .gitattributes

Add `*.sh text eol=lf` to keep shell scripts on LF line endings, even when Git checks them out on Windows. See the [Bash style guide](../bash/Bash.md#line-endings).

#### .gitignore

Ignored files are usually build artifacts and machine generated files that can be derived from your repository source or should otherwise not be committed. Some common examples are:

- dependency caches, such as the contents of /node_modules or /packages
- compiled code, such as .o, .exe, and .dll files
- Output directories, such as /bin, /out and /build
- Target files generated at runtime, such as .log, .lock, or .tmp
- Hidden system files, such as .DS_Store or Thumbs.db
- Personal IDE config files, such as .idea/workspace.xml
- Environment variables that are dependent on the runtime system
- Secrets such as API-keys and database passwords

These will look different depending on the language but an example for markdown is included in this repository

#### .gitmodules

This file is only needed if there are submodules in the repository.

#### .mailmap

A .mailmap should be included with entries for every developer that commits from within the organization.

#### Readme

The Readme should contain all information necessary to understand what the project does and how to use it.
It should include how to install the project and its dependencies or add it to a project.
It should have a Get Started section and a few examples on how to use the project.

#### License

Every repository should have a license.
GitHub has created [ChooseALicense](https://choosealicense.com/) to make it easier to choose one.

#### Code of conduct

Every repository should have a code of conduct.
If not writing one just use the one in [Templates](https://github.com/Lrssn-blog/Templates).

#### Changelog

Should have every change included in all releases.

Here is a template:

```bash
[Version number](#) (Link to release) (Date)
```

#### Features

- **Function:** Change ([First 8 number of commit](https://github.com/catppuccin/nvim/commit/85e93601e0f0b48aa2c6bbfae4d0e9d7a1898280))

#### Bug Fixes

- **Function:** Change ([#Issue](https://github.com/Lrssn-blog/Templates/issues/#)) ([First 8 number of commit](https://github.com/Lrssn-blog/Templates/commit/#))
- **Function:** Change ([First 8 number of commit](https://github.com/Lrssn-blog/Templates/commit/#)), closes [#Issue](https://github.com/Lrssn-blog/Templates/issues/#)

#### Performance Improvements

- **Function:** Change ([First 8 number of commit](https://github.com/Lrssn-blog/Templates/commit/#))

#### Authors

The Authors file have a list of everyone who contributed to the project.

#### Maintainers

This document describes the current project maintainers.
This document is placed in the .github folder.

#### Owners

This document describes the current repository owners.
This document is placed in the .github folder.

#### Contributing

This document describes how to contribute to the repository.
This includes creating pull requests, creating issues and how to check and structure the code.

## Commits

- Each commit should be a single *logical change*.
  Don't make several *logical changes* in one commit.
  For example, if a patch fixes a bug and optimizes the performance of a feature, split it into two separate commits.

  *Tip: Use `git add -p` to interactively stage specific portions of the modified files.*

- Don't split a single *logical change* into several commits.
  For example, the implementation of a feature and the corresponding tests should be in the same commit.

- Commit *early* and *often*.
  Small, self-contained commits are easier to understand and revert when something goes wrong.

- Commits should be ordered *logically*.
  For example, if *commit X* depends on changes done in *commit Y*, then *commit Y* should come before *commit X*.

Note: While working alone on a local branch that *has not yet been pushed*, it's fine to use commits as temporary snapshots of your work. However, it still holds true that you should apply all of the above *before* pushing it.

### Messages

Commit messages should tell you what has been changed and why. They should not tell you how, as the diff shows that.
The commit message should be structured as:

```bash
<type>[scope]: <description>

[optional body]

[optional footer(s)]
```

The commit type can include the following:

- **feat** – a new feature is introduced with the changes
- **fix** – a bug fix has occurred
- **chore** – changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies)
- **refactor** – refactored code that neither fixes a bug nor adds a feature
- **docs** – updates to documentation such as the README or other markdown files
- **style** – changes that do not affect the meaning of the code, likely related to code formatting such as white-space, missing semi-colons, and so on.
- **test** – including new or correcting previous tests
- **perf** – performance improvements
- **ci** – continuous integration related
- **build** – changes that affect the build system or external dependencies
- **revert** – reverts a previous commit

The scope is the module, such as authentication or rendering.

The description is what has been changed.

The body is why it has been changed. Here is also information about breaking changes such as deprecation of functions or changes to schemas.

For commits and pull requests written with an AI coding agent, see also the [Agentic development style guide](../agentic/Agentic.md#git-and-pull-requests).

The footer holds issue references, such as `Closes #42`, and trailers such as `Co-Authored-By:` or `Claude-Session:`. Put each trailer on its own line after a blank line.

## Folders

These folders are commonly used in repositories.

### .github

In this folder we keep everything that has to do with GitHub

#### Issue templates

A folder containing the templates for the different issues people can add.

#### Workflows

\**TBA**

#### Actions

\**TBA**

### Scripts

This is where all scripts that are not needed for running the project are stored.

### Submodules

All submodules are to be stored in a separate folder.

### Documentation

All documentation should be put in the `docs` folder in the root of the repository.
Both markdown and compiled for web or wiki.

## Issues

Issues are added and tracked through GitHub.
A maintainer labels and assigns the issue. If you file an issue, leave the labels and assignee to the maintainer.

### Templates

When adding a new issue a template should be used.

#### Bug report

A bug report should include:

- A name that is a short description on what the bug does.
- A full explanation on what the bug does and how it impacts the project.
- OS and version of os
- Version of software
- The steps needed to reproduce the bug.

#### Crash report

A crash report should include:

- A name that is a short description on how the software crashed.
- A full description on what happened prior to crash.
- OS and version of os
- Version of software
- The steps needed to reproduce the crash.

Finally a crash log should be added in the comments.

#### Feature request

A feature request should include:

- A name that is a short description of the new feature.
- A description on how the new feature will impact the project.

In the comments should be a discussion on how the feature will impact development.

## Branches

### Main and staging

`main` is the root of every repository.
It is the default branch, it exists from the first commit, and it always holds code that can be released.
Do not use `master`, `trunk` or `develop` instead.
Every other branch starts from `main`, and every pull request targets `main`.

A repository may also have a `staging` branch, but only when it needs a place to verify changes before a release, such as a pre-production environment that is deployed from a branch.
Do not add `staging` by default.

- `staging` starts from `main`, and is only updated by merging `main` into it.
- `staging` is never merged into `main`.
  Fixes found there are made on a branch from `main`, merged into `main` with a pull request, and then merged into `staging`.
- Never commit directly to `main` or `staging`, and never rewrite their history.
- Do not add other long-lived branches for environments, such as `production`.
  Deploy production from `main`.

### Working branches

- Choose *short* and *descriptive* names:

  ```bash
  git checkout -b oauth-migration     # good
  git checkout -b login_fix           # bad
  ```

- Identifiers from corresponding tickets in an external service (eg. a GitHub issue) are also good candidates for use in branch names.
  For example:

  ```bash
  # GitHub issue #15
  $ git checkout -b issue-15
  ```

- Use lowercase in branch names, with *hyphens* to separate words.

  ```bash
  git checkout -b new-feature         # good
  git checkout -b New_Feature         # bad
  ```

- When several people are working on the *same* feature, it might be convenient to have *personal* feature branches and a *team-wide* feature branch.
  Use the following naming convention:

  ```bash
  git checkout -b feature-a/main # team-wide branch
  git checkout -b feature-a/maria  # Maria's personal branch
  git checkout -b feature-a/nick   # Nick's personal branch
  ```

  Merge at will the personal branches to the team-wide branch.
  Eventually, the team-wide branch will be merged to "main".

- Delete your branch from the upstream repository after it's merged, unless there is a specific reason not to.

  Tip: Use the following command while being on "main", to list merged branches:

  ```bash
  git branch --merged | grep -v "\*"
  ```

## Pull request

### Opening a request

- Before opening the PR, make sure you're up to date with `main` so that your changes are easier to merge
- The title and description should help the reviewer.
  Make the title succinct and descriptive, and then add detail in the description.
- The description should summarise your changes and include useful links, eg to an issue, a ticket or a related PR.
  If the change affects a user interface, add a screenshot or describe the visible change.
- When raising a PR, the title and description are emailed to those following the repo.
  Any subsequent changes are not emailed, so it's worth spending a bit of time getting it right at the point of raising the PR.
- It is worth explaining/highlighting any potentially contentious changes, and any testing that you have already done.

Note: The canonical description of changes should always be in the individual commits.
Pull Requests are an artefact of GitHub, and we would lose that data if we switched away.

### Reviewing a request

#### Guidelines for review

- It is important to take time to review a pull request properly; the review stage is as important as writing the code in the first place
- If the reviewer's preference is unclear, state your assumption in the PR description before you review.
  Some people prefer feedback in person or while pairing, especially less experienced authors.
- If the code is good, or solves something in a clever way, *say so*.
  Call out individual bits of quality - it signposts good practice for others, and rewards the person submitting the request.
- State what, if anything, is a blocker explicitly

#### Communicate with others who may consider reviewing the PR

- If you're going to discuss some issues offline, please comment as such in the PR so that no-one merges it in the meantime - "A few issues here, going to discuss offline" would be enough.
  When conversation has taken place elsewhere, summarise the conversation as a comment on the PR for the benefit of others.
- If you look at a PR but don't feel comfortable merging it please say what you've looked at or not so other reviewers know the request hasn't been properly reviewed.
- If you're committed to reviewing the request through to merging or closing, assign the PR to yourself

#### Helpful things to consider while reviewing

- Try running the code - even if the tests pass it might have bugs
- Consider security when reviewing code, particularly where there is user input.
- Remember that a PR does not have to entirely solve the problem.
  If it adds value on its own it is better to merge now rather than wait for the rest of the changes required.
- Always comment on individual lines in the full-file diff view, not on a commit page because GitHub loses them if you rebase
- Ensure that any relevant documentation (`README` files, things in the `docs` folder) is up to date with the changes

### Addressing comments

Any comments flagged as blocking should be addressed. This includes spelling or grammatical errors in documentation.

- While a PR is in review, add a new commit for each round of fixes, for example to rename a variable or add a missing test.
  Do not amend or rebase commits that are already pushed.
- Before the first push, or on a branch that only you use, amend or squash freely.
  Then push with `git push --force-with-lease`, never `--force`, and never to `main`.
- If you are unsure how to do this, describe what you tried in the PR.
- Major changes should probably be addressed in a separate commit - be sure that when addressing changes you follow existing commit guidelines - "Addressed feedback" isn't an acceptable commit message
- Explicitly comment that all relevant comments have been addressed to notify any watchers - you don't need to do this on a per-comment basis
- Refactoring can and should be done in follow-up separate pull request - it should never be considered a blocker

### 'Done'

'Done' doesn't just come when the code is merged. Features should not be considered delivered until they're in production, and it's the responsibility of the programmer who wrote the code to ensure their work is deployed in a timely fashion.

## Merges

- **Do not rewrite published history.** The repository's history is valuable in its own right and it is very important to be able to tell *what actually happened*.
  Altering published history is a common source of problems for anyone working on the project.

- However, there are cases where rewriting history is legitimate.
  These are when:

  - You are the only one working on the branch and it is not being reviewed.

  - You want to tidy up your branch (eg. squash commits) and/or rebase it onto the "main" in order to merge it later.

  That said, *never rewrite the history of the "main" branch* or any other special branches (ie. used by production or CI servers).

- Keep the history *clean* and *simple*.
  *Just before you merge* your branch:

1. Make sure it conforms to the style guide and perform any needed actions if it doesn't (squash/reorder commits, reword messages etc.)

2. Rebase only a branch that nobody else has reviewed.
   For a reviewed branch, merge the base branch into it instead:

  ```bash
  # Not yet reviewed by anyone else: rebase.
  [my-branch] $ git fetch
  [my-branch] $ git rebase origin/main

  # Already reviewed: merge instead, which keeps history intact.
  [my-branch] $ git merge origin/main
  ```

Rebasing gives a branch that can be applied directly to the end of the "main" branch, with a very simple history.
*(Note: This strategy is better suited for projects with short-running branches. Otherwise it might be better to occasionally merge the "main" branch instead of rebasing onto it.)*

- If your branch includes more than one commit, do not merge with a fast-forward:

  ```bash
  # good - ensures that a merge commit is created
  $ git merge --no-ff my-branch

  # bad
  $ git merge my-branch
  ```

## Patches

\**TBA**

## Notes

\**TBA**

## Releases

\**TBA**

### Versioning

Versioning will be done using the Semantic Versioning scheme
Given a version number MAJOR.MINOR.PATCH, increment the:

- MAJOR version when you make incompatible API changes
- MINOR version when you add functionality in a backward compatible manner
- PATCH version when you make backward compatible bug fixes

Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format. For example, a beta release is `1.0.0-beta.1`.

## GitHub

\**TBA**
