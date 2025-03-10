# Git style guide

[TOC]

# Repository
## Documents
Every repository should have most the following documents, even if they are empty. 
### .editorconfig
A editorconfig will make sure every editor behaves the same. For more information see [editorconfig.org](https://editorconfig.org/). 
What every editorconfig should include are:
- indent_style: The preffered style is tabs.
- indent_size: The preffered size is 4.
- tab_width: This should match the indent_size.
- end_of_line: LF is preffered for intercompatability.
- charset: While there is a argument for using UTF-16 we will stick to UTF-8 due to using less memory. 
- trim_trailing_whitespace: The preffered style is true.
- insert_final_newline: The preffered style is true.
- max_line_length: The preffered value is 80
- root: Set to true unless there are other editorconfigs in the repository.

These may look different depending on the language but a example is included in [Templates](https://github.com/Lrssn-blog/Templates).
### .gitattributes
### .gitignore
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
### .gitmodules
This file is only needed if there are submodules in the repository.
### .mailmap
A .mailmap should be included with entries for every developer that commits from within the organization. 
### Readme
The Readme should contain all information necessary to understand what the project does and how to use it.
It should include how to install the project and its dependencies or add it to a project.
It should have a Get Started section and a few examples on how to use the project.
### License
Every repository should have a licens. 
Github has created [ChooseALicense](https://choosealicense.com/) to make it easier to choose one.
### Code of conduct
Every Repo should have a code of conduct.
If not writing one just use the one in [Templates](https://github.com/Lrssn-blog/Templates).
### Changelog
Should have every change included in all releases.

Here is a template:

### [Version number](#) (Link to release) (Date)

### Features
* **Function:** Change ([First 8 number of commit](https://github.com/catppuccin/nvim/commit/85e93601e0f0b48aa2c6bbfae4d0e9d7a1898280))

### Bug Fixes

* **Function:** Change ([#Issue](https://github.com/Lrssn-blog/Templates/issues/#)) ([First 8 number of commit](https://github.com/Lrssn-blog/Templates/commit/#))
* **Function:** Change ([First 8 number of commit](https://github.com/Lrssn-blog/Templates/commit/#)), closes [#Issue](https://github.com/Lrssn-blog/Templates/issues/#)

### Performance Improvements

* **Function:** Change ([First 8 number of commit](https://github.com/Lrssn-blog/Templates/commit/#))

### Authors
The Authors file have a list of everyone who contributed to the project.
### Maintainers
This document describes the current project maintainers.
This document is placed in the .github folder.
### Owners
This document describes the current repository owners.
This document is placed in the .github folder.
### Contributing
This document describes how to contribute to the repository. 
This includes creating pull requests, creating issues and how to check and structure the code.

# Commits
* Each commit should be a single *logical change*. Don't make several *logical changes* in one commit. For example, if a patch fixes a bug and optimizes the performance of a feature, split it into two separate commits.

  *Tip: Use `git add -p` to interactively stage specific portions of the
  modified files.*

* Don't split a single *logical change* into several commits. For example, the implementation of a feature and the corresponding tests should be in the same commit.

* Commit *early* and *often*. Small, self-contained commits are easier to understand and revert when something goes wrong.

* Commits should be ordered *logically*. For example, if *commit X* depends on changes done in *commit Y*, then *commit Y* should come before *commit X*.

Note: While working alone on a local branch that *has not yet been pushed*, it's fine to use commits as temporary snapshots of your work. However, it still holds true that you should apply all of the above *before* pushing it.

## Messages

Commit messages should tell you how the code has been changed and why. It should not tell you how as this should be shown through the diff. 
The commit message should be structured as:

> `<type>[scope]: <description>`
>
> `[optional body]`
>
> `[optional footer(s)]`

The commit type can include the following:

- **feat** – a new feature is introduced with the changes
- **fix** – a bug fix has occurred
- **chore** – changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies)
- **refactor** – refactored code that neither fixes a bug nor adds a feature
- **docs** – updates to documentation such as a the README or other markdown files
- **style** – changes that do not affect the meaning of the code, likely related to code formatting such as white-space, missing semi-colons, and so on.
- **test** – including new or correcting previous tests
- **perf** – performance improvements
- **ci** – continuous integration related
- **build** – changes that affect the build system or external dependencies
- **revert** – reverts a previous commit

The scope is the module, such as authentication or rendering.

The description is what has been changed. 

The body is why it has been changed. Here is also information about breaking changes such as deprecation of functions or changes to schemas.

The footer is the issues or tickets the commit works on. 

# Folders
These folders are commonly used in repositories.
## .github
In this folder we keep everything that has to do with Github
### Issue templates
A folder containing the templates for the different issues people can add. 
### Workflows
### Actions
## Scripts
This is where all scripts that are not needed for running the project are stored. 
## Submodules
All submodules are to be stored in a separate folder.
## Documentation
All documentation should be put in the Docs folder in the root of the repository.
Both markdown and compiled for web or wiki.

# Issues
Issues are added and tracked through github.
The issue is labeled and assigned to by a maintainer.
## Templates
When adding a new issue a template should be used.
### Bug report
A bug report should include:
A name that is a short description on what the bug does.
A full explanation on what the bug does and how it impacts the project.
OS and version of os
Version of software
The steps needed to reproduce the bug.  
### Crash report
A crash report should include:
A name that is a short description on how the software crashed.
A full description on what happened prior to crash.
OS and version of os
Version of software
The steps needed to reproduce the crash.

Finally a crash log should be added in the comments.
### Feature request
A feature request should include:
A name that is a short description of the new feature.
A description on how the new feature will impact the project.

In the comments should be a discussion on how the feature will impact development.

# Branches
* Choose *short* and *descriptive* names:

  ```shell
  $ git checkout -b oauth-migration     # good
  $ git checkout -b login_fix           # bad
  ```

* Identifiers from corresponding tickets in an external service (eg. a GitHub
  issue) are also good candidates for use in branch names. For example:

  ```shell
  # GitHub issue #15
  $ git checkout -b issue-15
  ```

* Use lowercase in branch names.
  letters are a valid exception. Use *hyphens* to separate words.

  ```shell
  $ git checkout -b new-feature         # good
  $ git checkout -b New_Feature         # bad
  ```

* When several people are working on the *same* feature, it might be convenient
  to have *personal* feature branches and a *team-wide* feature branch.
  Use the following naming convention:

  ```shell
  $ git checkout -b feature-a/main # team-wide branch
  $ git checkout -b feature-a/maria  # Maria's personal branch
  $ git checkout -b feature-a/nick   # Nick's personal branch
  ```

  Merge at will the personal branches to the team-wide branch (see ["Merging"](#merging)).
  Eventually, the team-wide branch will be merged to "main".

* Delete your branch from the upstream repository after it's merged, unless
  there is a specific reason not to.

  Tip: Use the following command while being on "main", to list merged
  branches:

  ```shell
  $ git branch --merged | grep -v "\*"
  ```


# Pull request
## Opening a request

- Before opening the PR, make sure you're up to date with `master` so that your changes are easier to merge
- The title and description should help the reviewer. Make the title succinct and descriptive, and then add detail in the description.
- The description should summarise your changes and include useful links, eg to a Pivotal ticket, ZenDesk ticket or related PR. If the changes involve frontend code, we love screenshots!
- When raising a PR, the title and description are emailed to those following the repo. Any subsequent changes are not emailed, so it's worth spending a bit of time getting it right at the point of raising the PR.
- It is worth explaining/highlighting any potentially contentious changes, and any testing that you have already done.

Note: The canonical description of changes should always be in the individual commits - Pull Requests are an artefact of GitHub, and we would lose that data
if we switched away.

## Reviewing a request

### Guidelines for review

- It is important to take time to review a pull request properly; the review stage is as important as writing the code in the first place
- If you're not sure how the individual wants their request reviewed, ask them before starting - they may prefer some of the feedback to be done in person or while pairing (especially if they're less experienced).
- If the code is good, or solves something in a clever way, *say so*. Call out individual bits of quality - it signposts good practice for others, and rewards the person submitting the request.
- State what, if anything, is a blocker explicitly

### Communicate with others who may consider reviewing the PR

- If you're going to discuss some issues offline, please comment as such in the
  PR so that no-one merges it in the meantime - "A few issues here, going to
  discuss offline" would be enough. When conversation has taken place elsewhere,
  summarise the conversation as a comment on the PR for the benefit of others.
- If you look at a PR but don't feel comfortable merging it please say what
  you've looked at or not so other reviewers know the request hasn't been
  properly reviewed.
- If you're committed to reviewing the request through to merging or closing,
  assign the PR to yourself


### Helpful things to consider while reviewing

- Try running the code - even if the tests pass it might have bugs
- Consider security when reviewing code, particularly where there is user input.
  The [basic security guidance](basic-security.md) might help.
- Remember that a PR does not have to entirely solve the problem. If it adds
  value on its own it is better to merge now rather than wait for the rest of
  the changes required.
- Always comment on individual lines in the full-file diff view, not on a commit
  page because GitHub loses them if you rebase
- Ensure that any relevant documentation (`README` files, things in the `doc`
  folder) is up to date with the changes


## Addressing comments

Any comments flagged as blocking should be addressed. This includes spelling or grammatical errors in documentation.

- If you're changing something minor in an existing commit (eg renaming a variable for clarity, adding a missing test), amend the existing commit (please ask for help if you don't know how to do this)
- Major changes should probably be addressed in a separate commit - be sure that when addressing changes you follow existing commit guidelines - "Addressed feedback" isn't an acceptable commit message
- Explicitly comment that all relevant comments have been addressed to notify any watchers - you don't need to do this on a per-comment basis 
  - Refactoring can and should be done in follow-up separate pull request - it should never be considered a blocker

## 'Done'

'Done' doesn't just come when the code is merged. Features should not be considered delivered until they're in production, and it's the responsibility of the programmer who wrote the code to ensure their work is deployed in a timely fashion.

# Merges
* **Do not rewrite published history.** The repository's history is valuable in its own right and it is very important to be able to tell *what actually happened*. Altering published history is a common source of problems for anyone working on the project.

* However, there are cases where rewriting history is legitimate. These are when:

  * You are the only one working on the branch and it is not being reviewed.

  * You want to tidy up your branch (eg. squash commits) and/or rebase it onto the "main" in order to merge it later.

  That said, *never rewrite the history of the "main" branch* or any other special branches (ie. used by production or CI servers).

* Keep the history *clean* and *simple*. *Just before you merge* your branch:

    1. Make sure it conforms to the style guide and perform any needed actions if it doesn't (squash/reorder commits, reword messages etc.)

    2. Rebase it onto the branch it's going to be merged to:

       ```shell
       [my-branch] $ git fetch
       [my-branch] $ git rebase origin/main
       # then merge
       ```

       This results in a branch that can be applied directly to the end of the "main" branch and results in a very simple history.

       *(Note: This strategy is better suited for projects with short-running branches. Otherwise it might be better to occassionally merge the "main" branch instead of rebasing onto it.)*

* If your branch includes more than one commit, do not merge with a fast-forward:

  ```shell
  # good - ensures that a merge commit is created
  $ git merge --no-ff my-branch

  # bad
  $ git merge my-branch
  ```

# Patches

# Notes

# Releases
## Versioning

# Github
## Projects
## Workflows
## Actions
## Codespaces