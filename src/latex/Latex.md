# LaTeX Style Guide

A style guide and theme for writing documents and packages in LaTeX.
It collects common LaTeX conventions, including the list of obsolete commands from [l2tabu](https://ctan.org/pkg/l2tabuen), and describes the Lrssn theme, which brings the colors of the [color palette](../colors/Colors.md) to LaTeX.

The house rules apply to LaTeX files as well: files use UTF-8 and LF line endings, environments are indented by 4 spaces, and prose is written one sentence per line, as in the [Markdown style guide](../markdown/Markdown.md#one-sentence-per-line).

## Table of contents

[TOC]

## Engine and build

### LuaLaTeX

Compile documents with LuaLaTeX.
It reads UTF-8 source files natively and can use any font installed on the system through `fontspec`.
Use pdfLaTeX only when a publisher's template requires it.

### latexmk

Build documents with [latexmk](https://ctan.org/pkg/latexmk), which runs LuaLaTeX and Biber as many times as needed to resolve all references.
Add this `.latexmkrc` to the root of the project:

```perl
# Use LuaLaTeX to create the PDF.
$pdf_mode = 4;
# Put all generated files in the build folder.
$out_dir = 'build';
```

```bash
# Build the document.
latexmk main.tex

# Rebuild whenever a file changes.
latexmk -pvc main.tex

# Remove the generated files.
latexmk -c
```

### Generated files

Never commit generated files.
Add the build folder and LaTeX's auxiliary files to `.gitignore`:

```text
build/
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.run.xml
*.synctex.gz
*.toc
```

## Project structure

### Folders

A document project looks like this:

```text
report/
├── chapters/
│   ├── introduction.tex
│   └── results.tex
├── figures/
│   └── architecture.pdf
├── .latexmkrc
├── main.tex
└── references.bib
```

- `main.tex` contains the preamble and includes the chapters.
- Each chapter or major section is a file in `chapters`.
- Figures are in `figures`.
- References are in `references.bib`.

Shared packages, such as the Lrssn theme, are kept in their own repository and installed in the local TeX tree, rather than copied into every project.
The Lrssn theme lives in the [Color-theme](https://github.com/Lrssn-blog/Color-theme) repository.

### File names

File names are lowercase, with hyphens between words.
Never use spaces in file names, as many LaTeX commands cannot handle them.

```text
system-architecture.pdf
related-work.tex
```

### Splitting documents

Use `\input` to include a file at the current position.
Use `\include` for the chapters of a book or a report, which starts each chapter on a new page and lets you compile single chapters with `\includeonly`.

```latex
\input{chapters/introduction}
\input{chapters/results}
```

Leave out the `.tex` extension.

## Source files

### Encoding

Source files are encoded in UTF-8.
LuaLaTeX expects UTF-8, so do not load the `inputenc` package.

### One sentence per line

Write each sentence on its own line.
LaTeX joins the lines of a paragraph, so the output does not change, but diffs and review comments only touch the sentences that changed.

A blank line ends a paragraph.
Never use `\\` or `\newline` to end a paragraph.

```latex
% Good:
This is the first sentence of the paragraph.
This is the second sentence.

This is a new paragraph.

% Bad:
This is the first sentence of the paragraph. This is the second sentence.\\
This is a new paragraph.
```

### Indentation

Indent the content of every environment by 4 spaces, except for the `document` environment.
Never use tabs.

```latex
\begin{document}

\begin{itemize}
    \item The first item.
    \item The second item.
\end{itemize}

\end{document}
```

### Line length

Code in macros and packages is at most 80 characters long.
Prose is not wrapped, since each sentence is on its own line.

### Comments

Comments start with `%` followed by a space.
End a line with `%` inside macro definitions where the line break would otherwise add an unwanted space to the output.

```latex
% The name of the project, used in the title and the headers.
\newcommand{\projectname}{%
    Style guide%
}
```

## Document classes

Use the class that fits the kind of document:

| Document | Class |
| --- | --- |
| Short documents and articles | `article` or `scrartcl` |
| Reports and theses with chapters | `report` or `scrreprt` |
| Books | `book` or `scrbook` |
| Letters | `scrlttr2` |
| Presentations | `beamer` |

The `scr` classes are part of [KOMA-Script](https://ctan.org/pkg/koma-script), which follows European typographic conventions and has better defaults for A4 paper.

## Preamble

### Order

Load the packages in the preamble in this order:

1. The document class.
1. Language and fonts.
1. Page layout.
1. Mathematics.
1. Graphics, tables and units.
1. The Lrssn theme.
1. The bibliography.
1. Your own macros.
1. `hyperref`, followed by `cleveref`.

`hyperref` changes many other packages, so it must be loaded after them, and `cleveref` must be loaded after `hyperref`.

```latex
\documentclass[a4paper, 11pt]{scrartcl}

% Language and fonts.
\usepackage[english]{babel}
\usepackage{fontspec}
\usepackage{csquotes}

% Page layout.
\usepackage[margin=25mm]{geometry}

% Mathematics.
\usepackage{amsmath}
\usepackage{amssymb}

% Graphics, tables and units.
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{siunitx}
\usepackage{subcaption}

% The Lrssn theme.
\usepackage[shore]{lrssntheme}

% Bibliography.
\usepackage[backend=biber, style=authoryear]{biblatex}
\addbibresource{references.bib}

% Macros.
\DeclareMathOperator*{\argmax}{arg\,max}
\newcommand{\vect}[1]{\mathbf{#1}}

% Links and references. These must be loaded last.
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=LrssnInfo,
    citecolor=LrssnInfo,
    urlcolor=LrssnPrimaryText,
}
\usepackage[capitalise, nameinlink, noabbrev]{cleveref}
```

Set the language of the document with `babel`, for example `english` or `swedish`, so that hyphenation and generated names such as "Figure" are correct.

### Document body

```latex
\begin{document}

\title{A Report}
\author{Lrssn}
\maketitle

\tableofcontents

\input{chapters/introduction}
\input{chapters/results}

\printbibliography

\end{document}
```

## Sections

Put a blank line before each sectioning command, and the label on the line after it.

```latex
\section{System architecture}
\label{sec:system-architecture}

The system consists of three services.
```

Section titles use sentence case, as in the Markdown guide.
Do not skip levels, such as going from `\section` straight to `\subsubsection`.

## Macros

### Semantic macros

Define macros for anything that is used more than once, and name them after what they mean, not how they look.
If the notation changes, only the macro needs to change.

```latex
% Good: the macro describes the meaning.
\newcommand{\vect}[1]{\mathbf{#1}}
The velocity $\vect{v}$ is constant.

% Bad: the formatting is repeated everywhere.
The velocity $\mathbf{v}$ is constant.
```

### Defining macros

- Use `\newcommand` for simple macros, and `\NewDocumentCommand` for macros with optional or special arguments.
- Use `\renewcommand` only to deliberately change an existing macro.
- Never use `\def` in documents.
  It silently overwrites existing macros, including LaTeX's own.
- Put all macros in the preamble or in a package, never in the middle of the document.

```latex
\NewDocumentCommand{\todo}{o m}{%
    \IfValueTF{#1}%
    {\textcolor{LrssnError}{[#1: #2]}}%
    {\textcolor{LrssnError}{[#2]}}%
}
```

### Macro names

Macro names consist of letters only, as LaTeX does not allow digits or punctuation in command names. Use lowercase names for the macros you define; the theme's color names, such as `LrssnPrimaryText`, are the exception.
Choose descriptive names that do not clash with existing commands.

### Spaces after macros

LaTeX removes the space after a macro without arguments.
Follow such macros with `{}` when a space should follow.
Do not use the `xspace` package. An explicit `{}` after the macro is easier to read and to check than an automatic guess.

```latex
% Good:
The \LaTeX{} document.

% Bad: prints "The LaTeXdocument".
The \LaTeX document.
```

## Obsolete commands and packages

Do not use the commands and packages in the left column.
They are outdated, have bugs, or have better replacements.

| Avoid | Use instead |
| --- | --- |
| `$$ … $$` | `\[ … \]` or `equation*` |
| `eqnarray` | `align` |
| `\bf`, `\it`, `\tt`, `\rm`, `\sc` | `\textbf`, `\emph` or `\textit`, `\texttt`, `\textrm`, `\textsc` |
| `{a \over b}` | `\frac{a}{b}` |
| `\centerline` and the `center` environment in floats | `\centering` |
| `\sloppy` | Fix the overfull lines by rewording or with hyphenation hints |
| `a4`, `a4wide` and `anysize` packages | `geometry` |
| `times` and `mathptmx` packages | `fontspec`, or `newtxtext` and `newtxmath` with pdfLaTeX |
| `epsfig` package and `\psfig` | `\includegraphics` from `graphicx` |
| `subfigure` and `subfig` packages | `subcaption` |
| `fancyheadings` package | `fancyhdr`, or `scrlayer-scrpage` with KOMA-Script |
| `natbib` and BibTeX | `biblatex` and Biber |
| `inputenc` with LuaLaTeX | Nothing, UTF-8 is the default |

## Text

### Quotation marks

Use `\enquote` from the `csquotes` package, which uses the correct quotation marks for the document language.
Never use straight double quotes (`"`).

```latex
% Good:
He called it \enquote{the best tool for the job}.

% Bad:
He called it "the best tool for the job".
```

### Dashes

| Input | Output | Use |
| --- | --- | --- |
| `-` | Hyphen | Compound words, such as `well-known` |
| `--` | En dash | Ranges, such as `pages 10--20` |
| `---` | Em dash | Breaks in a sentence |

### Ellipsis

Use `\dots` instead of three periods.

### Non-breaking spaces

Use a non-breaking space (`~`) wherever a line break would separate things that belong together:

- Before a reference or a citation: `in~\cref{sec:results}`, `as shown by~\textcite{knuth1984texbook}`.
- Between a number and its unit, unless `siunitx` formats it.
- Between initials and a last name: `D.~E.~Knuth`.

### Abbreviations

LaTeX adds extra space after a period that ends a sentence.
After an abbreviation in the middle of a sentence, put a backslash before the space, as in `e.g.\ the`, to get a normal space.
After a sentence that ends with a capital letter, put `\@` before the period.

```latex
See the results of the test, e.g.\ the first one.
The data was provided by NASA\@.
```

### Emphasis

Use `\emph` to emphasize words.
It switches between italic and upright text depending on the surrounding text.
Use bold text only for labels, not for emphasis in running text.

### Units and numbers

Format numbers and units with `siunitx`.
It uses the correct spacing and keeps the formatting consistent.

```latex
The file is \qty{1.5}{\mega\byte} large and has \num{12345} lines.
```

### Manual spacing

Do not use `\vspace`, `\hspace`, `\newpage` or `\\` to adjust the layout of a document.
Fix layout problems in the preamble or the theme, so that the fix applies everywhere.
If manual spacing is unavoidable, add it only as the last step before publishing.

## Mathematics

### Inline and display math

Use `$ … $` for inline math, and `\[ … \]` or the `equation` environment for displayed math.
Use `align` for several equations that are aligned, and never use `eqnarray`.

```latex
The area of a circle is $A = \pi r^2$.

\begin{align}
    f(x) & = (x + 1)^2    \\
         & = x^2 + 2x + 1
\end{align}
```

Only number the equations that are referenced, using `equation*` and `align*` for the others.

### Punctuation

Equations are part of the sentence and are punctuated like it.

```latex
The total cost is
\[
    C = \sum_{i=1}^{n} c_i,
\]
where $c_i$ is the cost of item $i$.
```

### Operators and text

Use the predefined operators, such as `\sin`, `\log` and `\max`, and declare new ones with `\DeclareMathOperator` in the preamble.
Use `\text` for words inside math.

```latex
% Good:
$\argmax_{x} f(x)$ and $x_{\text{max}}$

% Bad: typeset as a product of variables.
$argmax_{x} f(x)$ and $x_{max}$
```

### Braces

Always put the arguments of macros in braces, even when they are a single character.
Braces are optional for single-character subscripts and superscripts.

```latex
% Good:
$\frac{1}{2}$ and $x^2$ and $x^{10}$

% Bad:
$\frac12$ and $x^10$
```

## Figures and tables

### Floats

- Leave out the placement specifier, or use `[htbp]`, and let LaTeX place the float.
- Center the content with `\centering`, not the `center` environment, which adds extra vertical space.
- Put the `\label` after the `\caption`, otherwise the reference points to the wrong number.
- Put captions below figures and above tables.

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\linewidth]{figures/architecture}
    \caption{The architecture of the system.}
    \label{fig:architecture}
\end{figure}
```

### Graphics

- Leave out the file extension in `\includegraphics`, so that LaTeX picks the best available format.
- Use vector formats, such as PDF, for diagrams and plots, and PNG or JPEG only for photographs and screenshots.
- Size figures relative to the text, such as `width=0.8\linewidth`, not in absolute units.

### Tables

Use the `booktabs` package for tables.

- Use `\toprule`, `\midrule` and `\bottomrule` instead of `\hline`.
- Do not use vertical rules.
- Align numbers at the decimal point with the `S` column type from `siunitx`.

```latex
\begin{table}[htbp]
    \centering
    \caption{Build times for each configuration.}
    \label{tab:build-times}
    \begin{tabular}{l S[table-format=3.1]}
        \toprule
        Configuration & {Time (\unit{\second})} \\
        \midrule
        Debug         & 12.4                    \\
        Release       & 108.0                   \\
        \bottomrule
    \end{tabular}
\end{table}
```

The formatter aligns the `&` of every row, which makes tables easier to read in the source.

### Subfigures

Use the `subfigure` environment from the `subcaption` package for figures with several parts.

### Code listings

Use the `listings` package for source code.
The Lrssn theme defines a style for it, `lrssntheme`, and makes it the default.
Avoid `minted`, which needs to run external programs during the build with `-shell-escape`.

```latex
\begin{lstlisting}[language=Python, caption={Greeting a user.}]
def greet(name):
    return f'Hello, {name}'
\end{lstlisting}
```

## Cross-references

### Labels

Give every label a prefix that says what kind of thing it refers to, followed by a lowercase name with hyphens between words.

| Prefix | Refers to |
| --- | --- |
| `ch:` | Chapter |
| `sec:` | Section or subsection |
| `fig:` | Figure |
| `tab:` | Table |
| `eq:` | Equation |
| `lst:` | Code listing |
| `app:` | Appendix |

```latex
\label{fig:system-architecture}
```

### References

Reference labels with `\cref` from the `cleveref` package, which adds the right name, such as "Figure" or "Section", automatically.
Use `\Cref` at the beginning of a sentence.

```latex
% Good:
The results are shown in \cref{fig:results}.
\Cref{tab:build-times} lists the build times.

% Bad: the name has to be written by hand.
The results are shown in Figure~\ref{fig:results}.
```

## Bibliography

### biblatex

Manage references with `biblatex` and the Biber backend.
Choose a citation style that fits the field, such as `authoryear`, `numeric` or `ieee`.

| Command | Output | Use |
| --- | --- | --- |
| `\autocite{key}` | Follows the style | Most citations |
| `\textcite{key}` | Knuth (1984) | When the author is part of the sentence |
| `\parencite{key}` | (Knuth 1984) | Citations in parentheses |

### Bibliography files

- Each entry has a key made of the first author's last name, the year and the first significant word of the title, in lowercase: `knuth1984texbook`.
- Fields are indented by 4 spaces and their values are in braces.
- Words that must keep their capitalization are protected with braces, such as `{TeX}` or `{Python}`.
- Dates use the `date` field with ISO 8601 dates.
- Include the DOI when there is one.

```bibtex
@book{knuth1984texbook,
    author = {Knuth, Donald E.},
    title = {The {\TeX}book},
    publisher = {Addison-Wesley},
    date = {1984},
    isbn = {0-201-13447-0},
}
```

## The Lrssn theme

The Lrssn theme is the package `lrssntheme`, from the [Color-theme](https://github.com/Lrssn-blog/Color-theme) repository.
It brings the colors of the [color palette](../colors/Colors.md) to LaTeX, in two themes: Lrssn Shore, which is light, and Lrssn Hearth, which is dark.
Color-theme generates the package from its palettes, so do not copy it into a project or edit it by hand.

### Installing the theme

Copy `latex/lrssntheme.sty` from Color-theme to the local TeX tree, for example `~/texmf/tex/latex/lrssntheme/`.

### Using the theme

Load the theme after the other packages and before `hyperref`, and set the link colors as shown in [Preamble](#preamble).
Choose the theme with an option:

| Option | Use |
| --- | --- |
| `shore` | The default: Shore's colors on a white page, for print. |
| `hearth` | Hearth's colors on a dark page, for PDFs read on a screen. |
| `nolistings` | Leaves out the style for `listings`. |

```latex
\usepackage[hearth]{lrssntheme}
```

For presentations, set the Beamer colors from the theme:

```latex
\documentclass{beamer}
\usepackage[shore]{lrssntheme}

\setbeamercolor{structure}{fg=LrssnPrimaryText}
\setbeamercolor{normal text}{fg=LrssnText, bg=LrssnBackground}
\setbeamercolor{alerted text}{fg=LrssnError}
```

### Colors

The theme defines semantic color names for use with `xcolor`.
Each name takes its value from the theme chosen with the option, so a document looks right in both.

| Name | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `LrssnBackground` | `#fdf6ea` | `#101a16` | The page. |
| `LrssnSurface` | `#f5ead7` | `#0c1411` | Boxes and panels. |
| `LrssnCode` | `#f8eedd` | `#15211c` | Behind code. |
| `LrssnRule` | `#e3d3b9` | `#2e343c` | Rules and frames. |
| `LrssnText` | `#13303d` | `#f0e3d0` | Text. |
| `LrssnMuted` | `#4f6470` | `#a3aebb` | Secondary text, such as captions. |
| `LrssnComment` | `#76664e` | `#8796aa` | Comments and line numbers in code. |
| `LrssnPrimary` | `#fc6600` | `#fc6600` | The brand orange: fills and rules, never text. |
| `LrssnPrimaryText` | `#b04600` | `#ff8a3d` | Orange text and links. |
| `LrssnPrimarySoft` | `#ffe3cc` | `#3a1f0e` | A tint behind highlighted text. |
| `LrssnOnPrimary` | `#14171c` | `#14171c` | Text on an orange fill. |
| `LrssnSecondary` | `#00999a` | `#4d94b8` | The cool accent: fills and rules, never text. |
| `LrssnSecondaryText` | `#00737a` | `#8cc8e3` | Text in the cool accent. |
| `LrssnSecondarySoft` | `#d2f1ee` | `#142430` | A tint behind secondary text. |
| `LrssnKeyword` | `#b04600` | `#fc6600` | Keywords in code. |
| `LrssnFunction` | `#00629c` | `#ffb547` | Functions in code. |
| `LrssnString` | `#00756a` | `#a9d48f` | Strings in code. |
| `LrssnNumber` | `#c2215a` | `#ff88c8` | Numbers and constants in code. |
| `LrssnType` | `#3550b0` | `#7fcbe6` | Types in code. |
| `LrssnBuiltin` | `#8a3fbf` | `#c4a5ff` | Built-ins in code. |
| `LrssnError` | `#c4262e` | `#ff6b5e` | Errors and danger. |
| `LrssnWarning` | `#965a00` | `#ffb547` | Warnings. |
| `LrssnSuccess` | `#1c7448` | `#a9d48f` | Success. |
| `LrssnInfo` | `#00629c` | `#7fcbe6` | Neutral information. |

```latex
\textcolor{LrssnPrimaryText}{Important}
\colorbox{LrssnPrimarySoft}{Highlighted text}
```

Use the colors for the same purpose in every document, as listed in the table.
Never use color as the only way to convey information, as some readers cannot see it.

## Writing packages and classes

### Packages versus classes

Write a package (`.sty`) for features that can be used in any document, such as the theme.
Write a class (`.cls`) only for a complete kind of document with its own layout, such as a letter or a thesis template.
A class builds on an existing class with `\LoadClass`.

### File header

Every package and class starts with `\NeedsTeXFormat` and `\ProvidesPackage` or `\ProvidesClass`.
The optional argument holds the release date, the version and a short description.
The version follows [Semantic Versioning](../git/Git.md#versioning), and matches the Git tag of the release.

```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{lrssntheme}[2026-10-23 v1.0.0 Lrssn Shore and Hearth colours]
```

### Loading other packages

Load dependencies with `\RequirePackage` in packages, and never with `\usepackage`.
Pass options to packages that the user may also load with `\PassOptionsToPackage` before loading them, to avoid option clashes.

### Internal names

Internal macros contain an `@`, which cannot be used in documents, and start with the package name: `\lrssntheme@listingstrue`.
Public macros and environments use names that are unlikely to clash with other packages, prefixed with the package name where they are generic.

### Options

Declare options with `\DeclareOption`, and process them with `\ProcessOptions\relax` before loading dependencies.
Store the state of an option in a switch created with `\newif`.

### expl3

Larger packages may be written in the LaTeX3 programming layer, `expl3`.
Use the package name as the module prefix for all functions and variables, such as `\lrssntheme_set_color:n` and `\l_lrssntheme_color_tl`.

### End of file

End packages and classes with `\endinput`.

## Tooling

### Linter

Check documents with [ChkTeX](https://ctan.org/pkg/chktex), which finds common mistakes such as wrong spacing, quotation marks and dashes.

```bash
chktex main.tex chapters/*.tex
```

ChkTeX warns about a `\label` on its own line after `\section` or `\caption` (warning 24).
That is the layout this guide recommends, and the warning is safe to ignore here.
Turn it off with a `.chktexrc` file in the root of the project:

```text
CmdLine { -n24 }
```

### Formatter

Format the source with [latexindent](https://ctan.org/pkg/latexindent), configured for 4 spaces.
Add this `.latexindent.yaml` to the root of the project:

```yaml
defaultIndent: "    "
onlyOneBackUp: 1
```

```bash
latexindent --local=.latexindent.yaml --overwrite main.tex
```

### Editor

[VS Code](https://code.visualstudio.com/) with the [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) extension builds the document with latexmk on save and shows the PDF next to the source.

## See also

- [l2tabu: obsolete commands and packages](https://ctan.org/pkg/l2tabuen)
- [The LaTeX project documentation](https://www.latex-project.org/help/documentation/)
- [KOMA-Script](https://ctan.org/pkg/koma-script)
- [biblatex](https://ctan.org/pkg/biblatex)
- [Color palette](../colors/Colors.md)
- [Color-theme](https://github.com/Lrssn-blog/Color-theme)
