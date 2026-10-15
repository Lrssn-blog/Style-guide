# Bash Style Guide

A guide for writing Bash scripts that run on Linux, macOS and Windows.
It is heavily based on the [Google Shell style guide](https://google.github.io/styleguide/shellguide.html).

Deviations from the Google guide:

- Code is indented by 4 spaces instead of 2, following the house rule in `.editorconfig`.
- Scripts start with `#!/usr/bin/env bash` instead of `#!/bin/bash`, so that they find Bash on every platform.
- Scripts enable strict mode with `set -euo pipefail`.
- A section on [portability](#portability) covers macOS and Windows.

## Table of contents

[TOC]

## Background

### Which shell to use

Bash is the shell for executable scripts in this repository.
Do not write scripts for `sh`, `zsh` or `fish`.

The exception is environments where Bash is not installed, such as minimal container images based on Alpine Linux.
Scripts for those are written for POSIX `sh` and still follow this guide where the shell allows it.

### When to use shell

Shell is a good choice for small utilities and wrapper scripts that mostly call other programs.
It is a poor choice for anything else.

Use a language such as Python or Go instead when:

- The script is longer than about 100 lines.
- The script needs data structures other than simple arrays.
- The control flow is complex.
- Performance matters.

Scripts tend to grow.
Rewrite a script in another language early, before the rewrite becomes expensive.

## Source files

### File names

File names are lowercase, with underscores or hyphens between words.
Follow the convention of the project.

Scripts in a repository have the `.sh` extension, so that editors and tools recognize them.
Commands that are installed on the `PATH` have no extension, since the user should not need to know what language a command is written in.

Libraries, which are only meant to be sourced by other scripts, have the `.sh` extension and are not executable.

Scripts that are not needed to run the project belong in the `scripts` folder, as described in the [Git style guide](../git/Git.md#scripts).

### File encoding and line endings

Source files are encoded in UTF-8 and use LF line endings.
Bash cannot run a script with CRLF line endings, so this matters on Windows.
See [Line endings](#line-endings) for how to enforce it.

### Executable permissions

Executable scripts have the executable bit set, and libraries do not.

```bash
chmod +x scripts/deploy.sh
```

### SUID and SGID

SUID and SGID are forbidden on shell scripts.
There are too many security issues with shell to make it safe enough to allow them.
Use `sudo` to give elevated access if needed.

## Source file structure

A script consists of the following, in order:

1. The shebang line.
1. A file header comment.
1. `set -euo pipefail`.
1. Constants, environment variables and `source` statements for libraries.
1. Function definitions.
1. The `main` function.
1. A call to `main "$@"` as the last line.

Separate each section with a blank line.

### Shebang

Start executable scripts with this shebang line:

```bash
#!/usr/bin/env bash
```

`env` finds Bash on the `PATH`, which works on Linux, on macOS with a newer Bash installed, and in Git Bash on Windows.

### File header

Start each file with a comment that describes what it does.
Add usage information if the script takes arguments.

```bash
#!/usr/bin/env bash
#
# Back up the database to the configured storage bucket.
#
# Usage: backup_db.sh [--dry-run] DATABASE
```

A copyright notice, if the file needs one, goes after the description.

### Strict mode

Enable strict mode directly after the file header:

```bash
set -euo pipefail
```

| Option | Effect |
| --- | --- |
| `-e` | Exit when a command fails |
| `-u` | Exit when an unset variable is used |
| `-o pipefail` | A pipeline fails if any command in it fails, not only the last one |

Strict mode turns many silent errors into immediate failures, but it is not a replacement for checking errors:

- `set -e` does not apply to commands in conditions, such as in `if` statements or before `&&` and `||`.
- `local var="$(command)"` hides the exit code of `command`.
  See [Local variables](#local-variables).
- An arithmetic command that evaluates to `0`, such as `((count++))` when `count` is `0`, counts as a failure.
  See [Arithmetic](#arithmetic).

### The main function

A script that is long enough to contain at least one other function has a function called `main` that contains the top level code.
The last line of the script calls it with all arguments.

```bash
main() {
    parse_args "$@"
    check_dependencies
    run_backup
}

main "$@"
```

This makes the start of the program easy to find, and lets `main` declare its variables with `local`.

## Environment

### STDOUT versus STDERR

All error messages go to `STDERR`.
This keeps them apart from the normal output, which may be piped to another program.

Use a function to print error messages with a timestamp:

```bash
err() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

if ! do_something; then
    err "Unable to do_something"
    exit 1
fi
```

## Comments

### Function comments

Every function that is not both obvious and short has a comment.
Every function in a library has a comment, regardless of length.

A function comment describes what the function does and lists, where they apply:

- **Globals**: the global variables that are used or changed.
- **Arguments**: the arguments the function takes.
- **Outputs**: what is printed to `STDOUT` or `STDERR`.
- **Returns**: the return value, if it is not the status of the last command.

```bash
# Delete a file from the backup directory.
# Globals:
#   BACKUP_DIR
# Arguments:
#   The name of the file to delete, relative to BACKUP_DIR.
# Outputs:
#   Writes an error message to STDERR if the file does not exist.
# Returns:
#   0 if the file was deleted, 1 otherwise.
delete_backup() {
    local file="${BACKUP_DIR}/$1"
    if [[ ! -f "${file}" ]]; then
        err "No such backup: ${file}"
        return 1
    fi
    rm -- "${file}"
}
```

### Implementation comments

Comment tricky, non-obvious, interesting or important parts of the code.
Do not comment everything.
If a piece of code needs a long comment, consider whether it can be made simpler.

### TODO comments

Write `TODO` comments with a link to an issue, such as `TODO(#42)`. If no issue exists yet, open one first.

```bash
# TODO(#41): Handle the case where the bucket does not exist.
# TODO(#42): Support incremental backups.
```

## Formatting

### Indentation

Indent by 4 spaces.
Never use tabs.

The only place tabs would be needed is in the body of a `<<-` here document.
Use a plain `<<` here document with unindented content instead.

Use blank lines between blocks to improve readability.

### Line length

The maximum line length is 80 characters.

Use a here document or an embedded newline for long strings.

```bash
cat << EOF
I am an exceptionally long
string.
EOF

long_string="I am an exceptionally
long string."
```

Paths and URLs that are longer than 80 characters may stay on one line.
Store them in a variable if that makes the code easier to read.

### Long commands

Break long commands with a backslash at the end of each line, and indent the continuation lines by 4 spaces.
Put one option per line when a command has many options.

```bash
docker run \
    --rm \
    --volume "${PWD}:/workspace" \
    --workdir /workspace \
    "${IMAGE}" make test
```

### Pipelines

Keep a pipeline on one line if it fits.
If it does not fit, put each command on its own line, start the continuation lines with the pipe, and indent them by 4 spaces.
The same applies to chains of `&&` and `||`.

```bash
# All fits on one line.
command1 | command2

# Long commands.
command1 \
    | command2 \
    | command3 \
    | command4

# Long logical chains.
fetch_dependencies \
    && build_project \
    && run_tests
```

### Control flow

Put `; then` and `; do` on the same line as the `if`, `for` or `while`.
`else` goes on its own line, and the closing `fi` or `done` is aligned with the opening statement.

```bash
for dir in "${dirs_to_cleanup[@]}"; do
    if [[ -d "${dir}/${SESSION_ID}" ]]; then
        log_date "Cleaning up old files in ${dir}/${SESSION_ID}"
        rm -r -- "${dir:?}/${SESSION_ID}" || error_message
    else
        mkdir -p "${dir}/${SESSION_ID}" || error_message
    fi
done
```

Do not leave out the `in "$@"` of a `for` loop that iterates over the arguments.

```bash
for arg in "$@"; do
    echo "argument: ${arg}"
done
```

### Case statements

- Indent the alternatives by 4 spaces.
- A one-line alternative has a space after the closing parenthesis and before the `;;`.
- In a multi-line alternative, the commands are indented by another 4 spaces and the `;;` is on its own line.
- Do not use the optional opening parenthesis before the pattern.

```bash
case "${expression}" in
    a)
        variable="..."
        some_command "${variable}" "${other_expr}"
        ;;
    absolute)
        actions="relative"
        another_command "${actions}" "${other_expr}"
        ;;
    *)
        error "Unexpected expression '${expression}'"
        ;;
esac
```

Simple commands may go on the same line as the pattern.

```bash
verbose='false'
while getopts 'abf:v' flag; do
    case "${flag}" in
        a) aflag='true' ;;
        b) bflag='true' ;;
        f) files="${OPTARG}" ;;
        v) verbose='true' ;;
        *) usage ;;
    esac
done
```

### Variable expansion

Use `"${var}"` with braces rather than `"$var"`.
The braces make the end of the name obvious and prevent mistakes such as `"$var_suffix"`.

Do not use braces for single-character shell variables and positional parameters, such as `$1`, `$?` and `$#`, unless they are followed by text that would change their meaning.

```bash
# Good:
echo "PATH=${PATH}, PWD=${PWD}, mine=${some_var}"
echo "Positional: $1 $5 $3"
echo "Ten arguments: ${10}"
echo "Many parameters: $#"

# Bad:
echo "a=$avar and b=$bvar"
echo "PID=${$}"
echo "${1}0${2}0${3}0"
```

### Quoting

- Always quote strings that contain variables, command substitutions, spaces or shell meta characters.
- Use arrays to safely pass lists of elements, such as command line flags.
  See [Arrays](#arrays).
- Quote `"$@"` to pass on the arguments, and never use `$*` unless you want to join them into one string.
- Use single quotes for strings without substitutions.
- Integers and arithmetic expressions do not need quotes.

```bash
# 'Single' quotes indicate that no substitution is wanted.
# "Double" quotes indicate that substitution is wanted.

flag="$(some_command and its args "$@" 'quoted separately')"

echo "${flag}"

number="$((2 + 2))"

if [[ "${number}" -gt 3 ]]; then
    echo 'Larger than three'
fi

grep -li Hugo /dev/null "$1"

git send-email --to "${reviewers}" "${msg}"
```

## Features and bugs

### ShellCheck

Run [ShellCheck](https://www.shellcheck.net/) on every script.
It finds common bugs and warnings, many of which are covered by this guide.
See [Tooling](#tooling).

### Command substitution

Use `$(command)` instead of backticks.
`$(...)` can be nested without escaping and is easier to read.

```bash
# Good:
var="$(command "$(command1)")"

# Bad:
var="`command \`command1\``"
```

### Tests

Use `[[ ... ]]` instead of `[ ... ]`, `test` and `/usr/bin/[`.
`[[ ... ]]` does not split words or expand file names, and supports pattern and regular expression matching.

```bash
# Matches when the name starts with 'f' followed by letters and digits.
if [[ "${filename}" =~ ^f[[:alnum:]]+$ ]]; then
    echo "Match"
fi

# Matches the pattern "f*", not files that start with f.
if [[ "${filename}" == f* ]]; then
    echo "Match"
fi
```

### Testing strings

Use `-z` and `-n` to test for empty and non-empty strings, rather than comparing with an empty string.
Use `==` for string equality, not `=`.

```bash
# Good:
if [[ -z "${my_var}" ]]; then
    do_something
fi

if [[ "${my_var}" == "some_string" ]]; then
    do_something
fi

# Bad:
if [[ "${my_var}" == "" ]]; then
    do_something
fi
```

Use `(( ... ))` or the `-lt`, `-gt` and similar operators to compare numbers.
Never use `<` and `>` inside `[[ ... ]]` for numbers, as they compare strings.

```bash
# Good:
if ((my_var > 3)); then
    do_something
fi

# Bad: compares the strings, so 22 is less than 3.
if [[ "${my_var}" > 3 ]]; then
    do_something
fi
```

### Wildcard expansion of file names

Use an explicit path when expanding wildcards.
A file name that starts with `-` would otherwise be read as an option.

```bash
# Good: the files are passed as ./-f, ./-r and so on.
rm -v ./*

# Bad: a file named -rf would be read as the options -r and -f.
rm -v *
```

### Eval

Do not use `eval`.
It runs any code in its input, makes the script hard to read, and hides what variables are set.

### Arrays

Use arrays to store lists of elements, and especially lists of command arguments.
Do not store a list in a string and rely on word splitting.

```bash
# Good:
declare -a flags
flags=(--foo --bar='baz')
flags+=(--greeting="Hello ${name}")
mybinary "${flags[@]}"

# Bad: breaks when an element contains a space.
flags='--foo --bar=baz'
flags+=" --greeting=\"Hello ${name}\""
mybinary ${flags}
```

Always expand arrays with `"${array[@]}"`, including the quotes.

### Pipes to while

Do not pipe into a `while` loop.
The loop runs in a subshell, so variables set inside it are lost when it ends.

```bash
# Bad: last_line is always 'NULL' after the loop.
last_line='NULL'
your_command | while read -r line; do
    if [[ -n "${line}" ]]; then
        last_line="${line}"
    fi
done
echo "${last_line}"
```

Use process substitution or `readarray` instead.

```bash
# Good:
last_line='NULL'
while read -r line; do
    if [[ -n "${line}" ]]; then
        last_line="${line}"
    fi
done < <(your_command)
echo "${last_line}"

# Good: reads all lines into an array first.
readarray -t lines < <(your_command)
for line in "${lines[@]}"; do
    process "${line}"
done
```

Always use `read -r`, so that backslashes in the input are not treated as escapes.

### Looping over files

Loop over a wildcard directly.
Never loop over the output of `ls`, as it breaks on file names with spaces.

```bash
# Good:
for file in ./*.txt; do
    process "${file}"
done

# Bad:
for file in $(ls *.txt); do
    process "${file}"
done
```

To find files recursively, use `find` with `-print0` together with `read -d ''`.

```bash
while IFS= read -r -d '' file; do
    process "${file}"
done < <(find . -name '*.txt' -print0)
```

### Arithmetic

Use `(( ... ))` and `$(( ... ))` for arithmetic.
Do not use `let`, `expr` or `$[ ... ]`.

```bash
# Simple calculation used as text.
echo "$((2 + 2)) is 4"

# Comparison.
if ((a < b)); then
    do_something
fi

# Assignment.
((i = 10 * j + 400))
```

Inside `(( ... ))`, variables do not need the `$` prefix.

Be careful with `(( ... ))` as a standalone command under `set -e`.
It fails when the expression evaluates to `0`, which ends the script.
Use an assignment with `$(( ... ))` for counters.

```bash
# Good:
count=$((count + 1))

# Bad: exits the script when count is 0 before the increment.
((count++))
```

### Aliases

Do not use aliases in scripts.
Use functions instead.

### Builtins versus external commands

Prefer builtins and parameter expansion over external programs such as `sed`, `awk` and `expr` for simple string operations.
They are faster, and behave the same on every platform.

| Expansion | Result |
| --- | --- |
| `${#var}` | The length of `var` |
| `${var#prefix}` | `var` without the shortest match of `prefix` at the start |
| `${var%suffix}` | `var` without the shortest match of `suffix` at the end |
| `${var//old/new}` | `var` with every `old` replaced by `new` |
| `${var:-default}` | `var`, or `default` if `var` is unset or empty |
| `${var:?message}` | `var`, or exit with `message` if `var` is unset or empty |

```bash
file='report.tar.gz'
echo "${file%%.*}" # report
echo "${file#*.}"  # tar.gz
```

### printf versus echo

Use `printf` when the output contains variables that may start with `-` or contain backslashes, or when you need formatting.
The behavior of `echo` with options such as `-e` and `-n` differs between platforms.

```bash
printf '%s\n' "${user_input}"
printf '%-10s %5d\n' "${name}" "${count}"
```

### Temporary files

Create temporary files and directories with `mktemp`, and remove them with a `trap` when the script exits.

```bash
tmp_dir="$(mktemp -d)"
trap 'rm -rf -- "${tmp_dir}"' EXIT
```

### Changing directory

Run commands in another directory inside a subshell, so that the rest of the script is not affected.

```bash
(
    cd "${build_dir}" || exit
    make all
)
```

## Naming

### Function names

Function names are lowercase, with underscores between words.
Libraries separate a package prefix from the name with `::`.

Write the parentheses after the name, put the opening brace on the same line, and do not use the `function` keyword.

```bash
# Single function.
my_func() {
    echo 'Hello'
}

# Part of a package.
mypackage::my_func() {
    echo 'Hello from mypackage'
}
```

### Variable names

Variable names are lowercase, with underscores between words.
Loop variables are named after what they loop over.

```bash
for zone in "${zones[@]}"; do
    something_with "${zone}"
done
```

### Constants and environment variables

Constants and exported environment variables are upper case, with underscores between words, and are declared at the top of the file.

```bash
# Constant.
readonly PATH_TO_FILES='/some/path'

# Both constant and exported to the environment.
declare -xr ORACLE_SID='PROD'
```

Variables that are set once at runtime, such as from command line arguments, are made read-only as soon as they are set.

```bash
ZIP_VERSION="$(dpkg --status zip | sed -n 's/^Version: //p')"
if [[ -z "${ZIP_VERSION}" ]]; then
    ZIP_VERSION="$(pacman -Q --info zip | sed -n 's/^Version *: //p')"
fi
if [[ -z "${ZIP_VERSION}" ]]; then
    handle_error_and_quit
fi
readonly ZIP_VERSION
```

### Local variables

Declare variables inside functions with `local`, so that they are only visible inside the function.

When the value comes from a command substitution, declare and assign the variable in separate statements.
`local` has its own exit code, which hides the exit code of the command.

```bash
my_func2() {
    local name="$1"

    # Separate lines for declaration and assignment:
    local my_var
    my_var="$(my_func)" || return

    # Bad: $? is always zero, as it is the exit code of 'local'.
    local my_var2="$(my_func)"
    (($? == 0)) || return
}
```

### Function location

Put all functions together near the top of the file, after the constants.
Do not put executable code between functions, as it makes the code hard to follow.

## Calling commands

### Checking return values

Always check the return value of a command whose failure matters, and give a useful error message.

```bash
if ! mv "${file_list[@]}" "${dest_dir}/"; then
    err "Unable to move ${file_list[*]} to ${dest_dir}"
    exit 1
fi
```

Use `PIPESTATUS` to check the exit code of each part of a pipeline.

```bash
tar -cf - ./* | (cd "${dir}" && tar -xf -)
return_codes=("${PIPESTATUS[@]}")
if ((return_codes[0] != 0)); then
    do_something
fi
if ((return_codes[1] != 0)); then
    do_something_else
fi
```

### End of options

Use `--` to mark the end of the options when passing arguments that may start with `-`, such as file names from user input.

```bash
rm -- "${file}"
grep -- "${pattern}" "${file}"
```

### Exit codes

Exit with `0` when the script succeeds and a non-zero code when it fails.
Document the exit codes in the file header if the script uses more than `0` and `1`.

## Portability

Scripts in this repository should run on Linux, on macOS and on Windows through Bash.

### Windows

On Windows, run scripts in the [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/) (WSL), which behaves like Linux, or in Git Bash, which is installed with [Git for Windows](https://gitforwindows.org/).
If a script must run on Windows without Bash, write it in PowerShell or in a language such as Python or Go instead.

Git Bash converts arguments that look like Unix paths to Windows paths when it calls Windows programs.
Convert paths explicitly with `cygpath` when a Windows program needs them, and turn the conversion off with `MSYS_NO_PATHCONV=1` when it changes arguments that are not paths.

```bash
if [[ "${OSTYPE}" == msys* || "${OSTYPE}" == cygwin* ]]; then
    config_path="$(cygpath -w "${config_path}")"
fi

MSYS_NO_PATHCONV=1 docker run --rm --volume "${PWD}:/workspace" alpine ls
```

Windows does not store an executable bit, so set it in Git:

```bash
git update-index --chmod=+x scripts/deploy.sh
```

### Line endings

Git on Windows may convert line endings to CRLF when files are checked out, which makes Bash fail with errors such as `$'\r': command not found`.
Add a `.gitattributes` file that keeps LF line endings for shell scripts:

```text
*.sh text eol=lf
```

### Bash version

macOS ships with Bash 3.2, which is missing many newer features, such as associative arrays (`declare -A`), `readarray` and case conversion (`${var,,}`).
Either avoid these features, or require Bash 4 or later and check the version at the start of the script.
Users can install a newer Bash with Homebrew, which `#!/usr/bin/env bash` then finds first.

```bash
if ((BASH_VERSINFO[0] < 4)); then
    echo "Bash 4 or later is required." >&2
    exit 1
fi
```

### GNU versus BSD tools

Linux uses the GNU versions of tools such as `sed`, `grep`, `date` and `find`, while macOS uses the BSD versions, which take different options.
Use only options that both support, or check which version is installed.

| Avoid | Reason | Instead |
| --- | --- | --- |
| `sed -i` | Takes different arguments on GNU and BSD | Write to a temporary file and `mv` it |
| `grep -P` | Not available on BSD | `grep -E` |
| `date -d` | Not available on BSD | Do the date calculation in another language |
| `xargs -r` | Not available on older BSD versions | Check for empty input first |
| Long options such as `--recursive` | Often not supported by BSD | Short options such as `-r` |

### Finding the script directory

Do not assume that the script runs from its own directory.
Find the directory with `BASH_SOURCE`.

```bash
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly script_dir
```

## Putting it together

A complete script that follows this guide:

```bash
#!/usr/bin/env bash
#
# Count the lines in all text files in a directory.
#
# Usage: count_lines.sh [-v] DIRECTORY

set -euo pipefail

USAGE="Usage: $(basename -- "$0") [-v] DIRECTORY"
readonly USAGE

verbose='false'

# Print an error message with a timestamp to STDERR.
# Arguments:
#   The message to print.
err() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

# Count the lines in a single file.
# Arguments:
#   The path of the file.
# Outputs:
#   Writes the number of lines to STDOUT.
count_file_lines() {
    local file="$1"
    local count
    count="$(wc -l < "${file}")"
    if [[ "${verbose}" == 'true' ]]; then
        printf '%s: %d\n' "${file}" "${count}" >&2
    fi
    printf '%d\n' "${count}"
}

main() {
    while getopts 'v' flag; do
        case "${flag}" in
            v) verbose='true' ;;
            *)
                err "${USAGE}"
                exit 2
                ;;
        esac
    done
    shift $((OPTIND - 1))

    if (($# != 1)); then
        err "${USAGE}"
        exit 2
    fi
    local dir="$1"
    if [[ ! -d "${dir}" ]]; then
        err "Not a directory: ${dir}"
        exit 1
    fi

    local total=0
    local file
    for file in "${dir}"/*.txt; do
        [[ -e "${file}" ]] || continue
        total=$((total + $(count_file_lines "${file}")))
    done
    printf 'Total: %d\n' "${total}"
}

main "$@"
```

## Tooling

### ShellCheck

Run [ShellCheck](https://www.shellcheck.net/) on every script, in your editor and in continuous integration.

```bash
shellcheck scripts/*.sh
```

Fix the warnings instead of disabling them.
If a warning really does not apply, disable it on the line before the code with a comment that explains why.

```bash
# The variable is used by the sourced configuration file.
# shellcheck disable=SC2034
readonly LOG_LEVEL='debug'
```

### shfmt

Format scripts with [shfmt](https://github.com/mvdan/sh).
shfmt reads its settings from `.editorconfig`, so add this section:

```ini
[*.sh]
indent_style = space
indent_size = 4
binary_next_line = true
switch_case_indent = true
space_redirects = true
```

shfmt removes the spaces inside `((...))` and `$((...))`, so the examples in this guide are written without them.
Then format all scripts in place:

```bash
shfmt --write scripts/
```

### Testing

Test scripts that are larger than a few lines with [Bats](https://github.com/bats-core/bats-core).
Bats tests use `[ ... ]` instead of `[[ ... ]]`, because a failing `[[ ... ]]` does not fail the test in older versions of Bash.

```bash
#!/usr/bin/env bats

@test "fails without a directory" {
    run ./count_lines.sh
    [ "${status}" -eq 2 ]
}
```

## See also

- [Google Shell style guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck wiki](https://www.shellcheck.net/wiki/)
- [Bash reference manual](https://www.gnu.org/software/bash/manual/bash.html)
