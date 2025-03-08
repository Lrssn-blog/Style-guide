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
### Owners
This document describes the current repository owners.
### Contributing
This document describes how to contribute to the repository. 
This includes creating pull requests, creating issues and how to check and structure the code.
## Security
## Documentation
All documentation should be put in the Docs folder in the root of the repository.
Both markdown and compiled for web or wiki.
## Submodules
All submodules are to be stored in a separate folder.
## Scripts
This is where all scripts that are not needed for running the project are stored. 


# Commits
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


# Issues
## Templates

# Branches

# Pull request

# Merges

# Patches

# Notes

# Github
## Projects
## Workflows
## Actions
## Codespaces