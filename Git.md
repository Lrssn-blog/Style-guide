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

These may look different depending on the language but a example is included in this repository
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
### License
### Code of conduct
### Changelog
### Authors
### Maintainers
### Owners
### Contributing
## Security
## Documentation
## Submodules
## Scripts


# Commits
## Message
## Description

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