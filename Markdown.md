# Markdown Style Guide

A style guide for writing Markdown documents such as READMEs, changelogs and the style guides in this repository.
It is heavily based on the [Google Markdown style guide](https://google.github.io/styleguide/docguide/style.html) and the rules of [markdownlint](https://github.com/DavidAnson/markdownlint).

Deviations from the Google guide:

- Prose is written one sentence per line instead of being hard-wrapped at 80 columns.
  Code blocks still have an 80 column limit.
- GitHub Flavored Markdown is the target flavor, so GitHub specific features such as alerts and task lists are allowed.

## Table of contents

[TOC]

## Principles

Markdown is meant to be readable both as source and as rendered output.
Every rule in this guide serves one of these goals:

1. **Source text is readable and portable.**
   Someone reading the raw file in a terminal or a diff should understand it without rendering it.
2. **The documents are maintainable over time.**
   Changes should produce small, clear diffs that are easy to review.
3. **The syntax is simple and easy to remember.**
   Prefer the plain, common form of a construct over clever alternatives.

When this guide does not cover something, choose the option that best serves these goals and be consistent with the rest of the document.

## Source files

### File names

Markdown files use the `.md` extension.
Do not use `.markdown`, `.mdown` or other variants.

Repository level documents that tools and people look for use upper case names:

- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `LICENSE.md`
- `AUTHORS.md`

Other documents use lowercase names with hyphens between words, for example `docs/getting-started.md`.
Follow the convention of the repository you are working in.
This repository names its guides after the topic with a leading capital letter (`Git.md`, `Javascript.md`), and new guides follow that pattern.

Documentation that is not a repository level document belongs in the `docs` folder, as described in the [Git style guide](./Git.md#documentation).

### File encoding: UTF-8

Source files are encoded in UTF-8 without a byte order mark.
Lines end with a line feed (LF), and every file ends with a single newline.

### Whitespace characters

Use spaces, never tabs, for indentation.
This includes code inside fenced code blocks.

Trailing whitespace is forbidden.
Do not use two trailing spaces to force a line break, as they are invisible and are removed by most editors.
If a hard line break is really needed, end the line with a backslash (`\`).
Most of the time a new paragraph or a list is the better choice.

```markdown
First line of an address\
Second line of an address
```

Do not use more than one consecutive blank line.

### Flavor

Documents are written in [GitHub Flavored Markdown](https://github.github.com/gfm/) (GFM), which is a strict superset of [CommonMark](https://commonmark.org/).
Avoid syntax that only works in a single renderer unless the document is only ever displayed by that renderer.

## Document layout

In general, documents benefit from the following layout:

````markdown
# Document title

Short introduction.

## Table of contents

[TOC]

## Topic

Content.

## See also

- [A related document](./Related.md)
````

### Title

Each document has exactly one level 1 heading, and it is the first line of the file.
The title should describe what the document is about.
For a style guide, the title is the topic followed by "Style Guide", for example `# Python Style Guide`.

### Introduction

Directly after the title, write one to three sentences that explain what the document is about and who it is for.
A reader should be able to tell from the introduction whether they are reading the right document.
If the document is based on another source, credit it here.

### Table of contents

Documents with more than a few sections have a `## Table of contents` heading followed by the `[TOC]` directive.
Renderers that support the directive, such as Gitiles and Python-Markdown, replace it with a generated table of contents.
GitHub shows the directive as plain text, but provides its own outline from the headings, so the directive does no harm there.

Do not maintain a table of contents by hand.
It goes out of date as soon as a heading changes.

### See also

Put links to related documents at the end of the document in a `## See also` section, rather than scattering them through the introduction.

## Line length and line breaks

### One sentence per line

Write each sentence on its own line, and do not hard-wrap prose at a fixed column.
Markdown joins the lines of a paragraph when it is rendered, so the output looks the same.

````markdown
Good: each sentence starts on a new line.
A change to one sentence only changes one line in the diff.
The rendered paragraph still reads as a single block of text.

Bad: this paragraph has two sentences. A change to either changes the line.
````

A very long sentence may also be broken after a comma or another natural pause.
If a sentence is longer than about 300 characters, consider splitting it into two sentences instead.

### Column limit for code: 80

Lines inside fenced code blocks follow the column limit of the language they contain, which is 80 columns for all languages in this repository.
Code that is copied out of a document should not need to be reformatted.

Tables, headings and URLs are exempt from any column limit, because they cannot be wrapped without breaking them.

### Hard line breaks

Use a backslash at the end of a line for a hard line break, as described in [Whitespace characters](#whitespace-characters).
Do not use `<br>` outside tables.

## Headings

### ATX style headings

Use ATX style headings (`#`), not Setext style headings (underlined with `===` or `---`).
Setext headings are hard to spot and only support two levels.

```markdown
## Good heading

Bad heading
-----------
```

Put a single space between the `#` characters and the heading text.
Do not add closing `#` characters.

```markdown
## Good heading

##Bad heading

## Bad heading ##
```

### Spacing around headings

Surround headings with exactly one blank line.
The only exception is the title at the top of the file, which has nothing above it.

### Heading levels

Increase heading levels one at a time.
Do not skip from a level 2 heading straight to a level 4 heading.

```markdown
## Formatting

### Braces

#### Empty blocks
```

Use level 2 headings for the main sections of a document and level 3 and 4 headings for subsections.
If a document needs level 5 or 6 headings, it is usually a sign that the document should be split up.

### Heading text

Headings use sentence case: capitalize the first word and proper nouns only.

```markdown
## Local variable declarations
```

Headings are not followed by punctuation such as `.`, `:` or `,`.
A question mark is allowed when the heading is a question, for example in an FAQ.

Do not use bold or italic text instead of a heading.
Emphasized lines do not show up in the outline and cannot be linked to.

```markdown
## Good heading

**Bad heading**
```

### Unique headings

Give every heading a name that is unique within its parent section.
Headings are turned into anchors (`#heading-text`), and duplicate headings produce anchors such as `#heading-text-1` that are fragile to link to.

Prefer descriptive headings that work on their own when linked to.

```markdown
## Summary of the build system

## Summary
```

## Paragraphs and prose

### Paragraphs

Separate paragraphs with exactly one blank line.
Do not indent the first line of a paragraph, as an indentation of four or more spaces turns it into a code block.

### Writing style

- Write for the reader who is new to the topic.
  Explain terms the first time they are used.
- Use the second person ("you") and the present tense.
- Use the active voice: "The script deletes the file", not "The file is deleted by the script".
- Keep sentences short and put the most important information first.
- Use "must", "should" and "may" consistently.
  "Must" is a requirement, "should" is a strong recommendation with rare exceptions, and "may" is optional.

### Terminology notes

Introduce a term that needs explaining with a bold label at the start of the paragraph.

```markdown
**Terminology note**: Line wrapping is breaking a long line into several.
```

## Lists

### Bullet lists

Use a hyphen (`-`) for bullet lists.
Do not mix `-`, `*` and `+` in the same document.

```markdown
- First item
- Second item
- Third item
```

### Numbered lists

For short lists that are unlikely to change, number the items in order.

```markdown
1. Clone the repository.
2. Install the dependencies.
3. Run the tests.
```

For longer lists that may change, use lazy numbering, where every item is numbered `1.`.
Markdown renders the correct numbers, and inserting or removing an item does not change every following line.

```markdown
1. Clone the repository.
1. Install the dependencies.
1. Run the tests.
1. Build the project.
1. Publish the release.
```

Use one style or the other in a list, never a mix.

### Space after the list marker

Put exactly one space between the list marker and the text.

```markdown
- Good
-   Bad

1. Good
1.  Bad
```

### Nested lists

Indent nested lists by 4 spaces, for both bullet lists and numbered lists.

```markdown
1. Install the tools:
    - Git
    - Node.js
1. Clone the repository.
1. Install the dependencies:
    1. Run `npm install`.
    1. Run `npm run build`.
```

Do not nest lists more than three levels deep.
A deeper structure is easier to read as separate sections.

### Content inside list items

Further paragraphs, code blocks and other content that belong to a list item are indented by 4 spaces so that they stay part of the item.

````markdown
1. Install the dependencies:

    ```bash
    npm install
    ```

1. Run the tests.

    The tests take about a minute to run.
````

When a sentence in a list item continues on the next line, indent the continuation line so that it lines up with the text of the item.
This applies to the one sentence per line rule as well.

```markdown
- The first sentence of the item.
  The second sentence of the item.
1. The first sentence of the item.
   The second sentence of the item.
```

### Blank lines around lists

Surround lists with a blank line.
Some renderers do not recognize a list that directly follows a paragraph.

### Punctuation and capitalization

Start every list item with a capital letter.
End an item with a period if it is a complete sentence, and leave the period out if it is a fragment.
Be consistent within a list.

Keep the items of a list grammatically parallel, so that they all start with the same kind of word.

```markdown
Good:

- Install the tools.
- Clone the repository.
- Run the tests.

Bad:

- Install the tools.
- The repository has to be cloned.
- Tests.
```

### Task lists

Task lists (`- [ ]` and `- [x]`) may be used in issues, pull requests and planning documents.
Do not use them in documents that describe how something works.

## Code

### Inline code

Use backticks for short pieces of code, commands, file names, paths, flags, field names and values.

```markdown
Run `npm install` to install the dependencies listed in `package.json`.
```

Do not use backticks for emphasis or for names of products.
To include a backtick inside inline code, surround the code with double backticks instead of single ones.

### Fenced code blocks

Use fenced code blocks with three backticks for code that is longer than a single short line.
Do not use tildes (`~~~`) for fences.
If the code itself contains three backticks, fence it with four.

### Declare the language

Every fenced code block declares its language after the opening fence.
The language enables syntax highlighting and tells the reader what they are looking at.

````markdown
```python
def greet(name: str) -> str:
    return f'Hello, {name}'
```
````

Use these language identifiers:

| Content | Identifier |
| --- | --- |
| Bash scripts and commands | `bash` |
| BibTeX bibliographies | `bibtex` |
| C++ | `cpp` |
| CMake | `cmake` |
| Commands together with their output | `console` |
| Dockerfiles | `dockerfile` |
| Go | `go` |
| INI files, such as `.editorconfig` | `ini` |
| JavaScript | `javascript` |
| JSON | `json` |
| LaTeX | `latex` |
| Markdown | `markdown` |
| Perl, including `.latexmkrc` and `cpanfile` | `perl` |
| Plain text and program output | `text` |
| Python | `python` |
| Rust | `rust` |
| TOML | `toml` |
| TypeScript | `typescript` |
| YAML | `yaml` |

Only label a block `bash` or `shell` if it really contains shell code.
Code in another language that is labeled as shell gets the wrong highlighting.

### Commands and output

Do not prefix commands with a prompt such as `$` when only commands are shown.
The reader should be able to copy the whole block and run it.

```bash
git fetch origin
git rebase origin/main
```

When a block shows commands together with their output, use the `console` language and prefix the commands with a dollar sign and a space (`$`) so that the reader can tell them apart from the output.

```console
$ git branch --show-current
main
```

### Long commands

Break commands that are longer than 80 characters with a backslash at the end of each line, and indent the continuation lines by 4 spaces.

```bash
docker run \
    --rm \
    --volume "$(pwd):/workspace" \
    --workdir /workspace \
    node:22-slim npm test
```

### Do not use indented code blocks

Do not use code blocks made by indenting text with 4 spaces.
They cannot declare a language and are easy to create by accident.

Do not indent fenced code blocks either, unless they are nested inside a list item.
An indented fence puts extra spaces in front of every line of code, which ends up in the reader's clipboard.

### Code style inside code blocks

Code inside code blocks follows the style guide for its language, including the 4 space indentation.
Examples that show what not to do should say so in a comment.

```javascript
// Bad: uses var.
var count = 0;

// Good:
let count = 0;
```

## Links

### Link text

Write link text that describes where the link goes.
The reader should be able to understand the link without reading the rest of the sentence.
Never use "here", "this link" or "click here" as link text.

```markdown
Good: See the [Git style guide](./Git.md) for commit messages.

Bad: See [here](./Git.md) for commit messages.

Bad: See the Git style guide for commit messages: [link](./Git.md).
```

Keep link text short.
Link the most relevant words of the sentence, not the whole sentence.

### Relative links

Link to files in the same repository with relative paths.
Absolute links to GitHub break in forks and on other branches, and do not work in a local clone.

```markdown
Good: [Javascript style guide](./Javascript.md)

Bad: [Javascript style guide](https://github.com/Lrssn-blog/Style-guide/blob/master/Javascript.md)
```

Link to a section in the same document by its anchor.
Anchors are the heading text in lowercase, with spaces replaced by hyphens and most punctuation removed.

```markdown
See [Nested lists](#nested-lists) for the indentation rules.
```

### Reference links

Use reference links when a URL is long or when the same link is used several times.
Define the references at the end of the section or the document they are used in.

```markdown
Read the [CommonMark spec][commonmark] and the [GFM spec][gfm].

[commonmark]: https://spec.commonmark.org/
[gfm]: https://github.github.com/gfm/
```

### Bare URLs

Do not leave bare URLs in text.
Give the link descriptive text, or surround the URL with angle brackets if the URL itself is what the reader needs.

```markdown
Good: Report security issues to <https://example.com/security>.

Bad: Report security issues to https://example.com/security.
```

### Links to code

When linking to a specific line of code on GitHub, use a permanent link that contains the commit hash, not a link to a branch.
Links to branches point at different code as the branch changes.

## Images

### Alternative text

Every image has alternative text that describes what the image shows.
Screen readers read the text, and it is displayed when the image cannot be loaded.

```markdown
![The Lrssn color palette with the orange primary color](./images/palette.png)
```

### Storing images

Store images in the repository, in an `images` folder next to the documents that use them, and link to them with relative paths.
Images hosted elsewhere can disappear or change.

Name image files in lowercase with hyphens between words, for example `images/build-pipeline.png`.

### When to use images

Use images when they explain something better than text, for example a screenshot of a user interface or a diagram of an architecture.
Do not use images of text or code, as they cannot be searched, copied or read by screen readers.

Prefer SVG for diagrams.
GitHub also renders [Mermaid](https://mermaid.js.org/) diagrams from code blocks with the `mermaid` language, which keeps diagrams editable in the source.

## Tables

### When to use tables

Use tables for data that the reader needs to scan in two dimensions, such as a comparison of options against several properties.
Do not use a table where a list would do, and never use tables for layout.

Avoid long text in table cells.
If a cell needs more than a short sentence, use a list or a section for each row instead.

### Table formatting

- Every table has a header row.
- Rows start and end with a pipe (`|`).
- Cells have one space of padding on each side of the content.
- Every row has the same number of cells as the header.
- Tables are surrounded by blank lines.

Aligning the pipes of every row is optional.
Aligned tables are easier to read as source, but every change to the longest cell changes every row in the diff.

```markdown
| Setting | Value | Notes |
| --- | --- | --- |
| `indent_size` | `4` | Spaces per level |
| `max_line_length` | `80` | Code only |
```

Use colons in the separator row to align columns, for example `| ---: |` for a column of numbers.

## Emphasis

Use single asterisks for italic text and double asterisks for bold text.
Do not use underscores.

```markdown
This is *important*, and this is **very important**.
```

Use emphasis sparingly.
When everything is emphasized, nothing stands out.
Use bold for terms that are being defined and for labels such as **Note**, and italics for gentle stress on a word.

## Block quotes and alerts

Use block quotes (`>`) for quotations from other sources.

For notes and warnings in documents that are displayed on GitHub, use [GitHub alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts).
Use them sparingly, and never put two alerts directly after each other.

```markdown
> [!NOTE]
> Useful information that the reader should know.
```

```markdown
> [!WARNING]
> Critical information that prevents mistakes.
```

The available alert types are `NOTE`, `TIP`, `IMPORTANT`, `WARNING` and `CAUTION`.

## Horizontal rules

Use three hyphens (`---`) for horizontal rules.
Prefer headings to separate content, and use horizontal rules rarely.

## HTML

Avoid HTML in Markdown documents.
It makes the source harder to read, and many renderers remove or restrict it.

The exceptions are the `<details>` and `<summary>` elements, which may be used to collapse long, optional content such as logs.

```markdown
<details>
<summary>Full build log</summary>

The log goes here.

</details>
```

## Front matter

Only add YAML front matter when a tool such as a static site generator requires it.
When front matter is used, it is the first thing in the file and is followed by the title.

```markdown
---
title: Getting started
---

# Getting started
```

## Repository documents

The [Git style guide](./Git.md#documents) describes which documents a repository should have and what they should contain.
The layout and formatting rules in this guide apply to all of them.

## Tooling

### EditorConfig

The `.editorconfig` in every repository sets the encoding, line endings, indentation and trailing whitespace for Markdown files as well as code.
Because this guide never uses trailing spaces for line breaks, `trim_trailing_whitespace = true` is safe for Markdown files.

### markdownlint

Use [markdownlint](https://github.com/DavidAnson/markdownlint) to check documents.
It is available as the [markdownlint extension for VS Code](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) and as the [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) command line tool.

Add this `.markdownlint.json` to the root of the repository.
It enables all default rules and configures them to match this guide.

```json
{
    "default": true,
    "MD003": {"style": "atx"},
    "MD004": {"style": "dash"},
    "MD007": {"indent": 4},
    "MD013": {
        "line_length": 300,
        "code_block_line_length": 80,
        "tables": false
    },
    "MD024": {"siblings_only": true},
    "MD029": {"style": "one_or_ordered"},
    "MD033": {"allowed_elements": ["details", "summary"]},
    "MD035": {"style": "---"},
    "MD046": {"style": "fenced"},
    "MD048": {"style": "backtick"},
    "MD049": {"style": "asterisk"},
    "MD050": {"style": "asterisk"},
    "MD055": {"style": "leading_and_trailing"}
}
```

The `MD013` settings allow long lines of prose, since sentences are not hard-wrapped, while keeping code blocks within 80 columns.
The limit of 300 characters for prose catches paragraphs that were written on a single line.

Run the linter on every Markdown file in the repository:

```bash
npx markdownlint-cli2 "**/*.md"
```

### Continuous integration

Run markdownlint on every pull request with the official GitHub Action.

```yaml
name: Lint
on: [pull_request]
jobs:
    markdown:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: DavidAnson/markdownlint-cli2-action@v16
              with:
                  globs: "**/*.md"
```

## See also

- [Google Markdown style guide](https://google.github.io/styleguide/docguide/style.html)
- [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [GitHub Flavored Markdown specification](https://github.github.com/gfm/)
- [Git style guide](./Git.md)
