# Javascript Style Guide
A basic javascript style guide, heavily based on the [Google styleguide](https://google.github.io/styleguide/jsguide.html).

# Table of contents
[TOC]

# Source Files
## File name
File names must be all lowercase and may include underscores (_) or dashes (-), but no additional punctuation. Follow the convention that your project uses. Filenames’ extension must be .js.

## File encoding: UTF-8
Source files are encoded in UTF-8.

## Special characters

### Whitespace characters
Aside from the line terminator sequence, the ASCII horizontal space character (0x20) is the only whitespace character that appears anywhere in a source file. This implies that
- All other whitespace characters in string literals are escaped, and
- Tab characters are not used for indentation.

### Special escape sequences
For any character that has a special escape sequence (\', \", \\, \b, \f, \n, \r, \t, \v), that sequence is used rather than the corresponding numeric escape (e.g \x0a, \u000a, or \u{a}). Legacy octal escapes are never used.

### Non-ASCII characters
For the remaining non-ASCII characters, either the actual Unicode character (e.g. ∞) or the equivalent hex or Unicode escape (e.g. \u221e) is used, depending only on which makes the code easier to read and understand.

  ```shell
    /* Best: perfectly clear even without a comment. */
    const units = 'μs';

    /* Allowed: but unnecessary as μ is a printable character. */
    const units = '\u03bcs'; // 'μs'

    /* Good: use escapes for non-printable characters with a comment for clarity. */
    return '\ufeff' + content;  // Prepend a byte order mark.
  ```