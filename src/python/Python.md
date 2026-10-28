# Python Style Guide

A style guide for Python.
It is heavily based on the [Google Python style guide](https://google.github.io/styleguide/pyguide.html), which is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/), and [PEP 8](https://peps.python.org/pep-0008/).
The code examples are our own.

Deviations from the Google guide:

- Code is formatted with the [Ruff](https://docs.astral.sh/ruff/) formatter, which follows the Black code style, and linted with Ruff instead of Pylint.
- Strings use single quotes, as in the [JavaScript](../javascript/Javascript.md#string-literals) and [TypeScript](../typescript/Typescript.md) guides.
  Docstrings use triple double quotes.
- All public functions and methods have type annotations.

## Table of contents

[TOC]

## Python version

Code targets Python 3.12 or later.
Use the features of the target version, such as built-in generic types, the `X | None` syntax and `match` statements.

## Source files

### File names

File names are lowercase, with underscores between words, and have the `.py` extension.
Do not use dashes, as files with dashes in their names cannot be imported.

```text
user_service.py
user_service_test.py
```

Test files are named after the module they test, with a `_test` suffix.

### File encoding: UTF-8

Source files are encoded in UTF-8.
Do not add an encoding declaration such as `# -*- coding: utf-8 -*-`, as UTF-8 is the default.

### Shebang

Only files that are run directly have a shebang line.

```python
#!/usr/bin/env python3
```

Most files are imported as modules and have no shebang.

## Source file structure

A file consists of the following, in order:

1. The shebang line, if the file is run directly.
1. The module docstring.
1. Imports.
1. Module-level constants.
1. Classes and functions.
1. The main guard, if the file is run directly.

```python
"""Tools for loading and validating user accounts."""

import dataclasses
import logging

import requests

from lrssn.storage import user_store

MAX_RETRIES = 3

_logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class User:
    """A registered user."""

    name: str
    email: str


def load_user(user_id: str) -> User:
    """Loads a user from the store."""
    ...
```

### Imports

#### Import modules, not names

Use `import x` for packages and modules.
Use `from x import y` where `x` is the package and `y` is the module.
Use `from x import y as z` if two modules named `y` are imported, if `y` conflicts with a name in the current module, or if `y` is inconveniently long.
Use `import y as z` only for well-known abbreviations, such as `import numpy as np`.

```python
# Good:
import os
from lrssn.storage import user_store

user_store.load('42')

# Bad: the reader cannot tell where load comes from.
from lrssn.storage.user_store import load

load('42')
```

The exceptions are symbols from `typing`, `collections.abc` and `typing_extensions`, which may be imported directly.

```python
from collections.abc import Iterable, Mapping
from typing import Any, Literal
```

#### Full package paths

Import every module by its full package path.
Do not use relative imports, even within the same package.

```python
# Good:
from lrssn.storage import user_store

# Bad:
from . import user_store
from ..storage import user_store
```

#### Import formatting

Put each import on its own line.
The exceptions are `typing`, `collections.abc` and `typing_extensions`, where several names may be imported on one line.

```python
# Good:
import os
import sys

# Bad:
import os, sys
```

Group the imports in this order, with a blank line between each group:

1. `from __future__` imports.
1. Standard library imports.
1. Third-party imports.
1. Imports from the same repository.

Within each group, sort the imports by the full module path, ignoring case.
Ruff sorts the imports automatically with the configuration in [Tooling](#tooling).

```python
import collections
import os
import sys

from absl import flags
import requests

from lrssn.server import handlers
from lrssn.storage import user_store
```

#### No wildcard imports

Never use `from x import *`.
It makes it impossible to tell where names come from.

## Formatting

Do not format code by hand.
Use the Ruff formatter with the configuration in [Tooling](#tooling), and let it decide.
The rules below describe what the formatter produces.

### Line length

The maximum line length is 80 characters.

The exceptions are long import statements, URLs, paths and long string constants in tests, and lint suppression comments.

Do not use backslashes to continue lines.
Use Python's implicit line joining inside parentheses, brackets and braces.

```python
# Good:
if (
    width == 0
    and height == 0
    and color == 'red'
    and emphasis == 'strong'
    and highlight
):
    ...

# Bad:
if width == 0 and height == 0 and color == 'red' and \
        emphasis == 'strong' and highlight:
    ...
```

When an expression is split over several lines, the formatter breaks before binary operators such as `and` and `+`, as PEP 8 recommends.
This is different from the JavaScript and TypeScript guides, which break after operators.

When a literal string does not fit on a line, use parentheses for implicit concatenation.

```python
x = (
    'This will build a very long long long long long long long long '
    'long long long long long long long string'
)
```

### Indentation

Indent code blocks by 4 spaces.
Never use tabs.

When a call, a definition or a literal does not fit on one line, break after the opening bracket, indent the content by 4 spaces, and put the closing bracket on its own line.
The closing bracket on its own line separates the arguments from the body that follows.

```python
report = create_report(
    argument_one, argument_two, argument_three, argument_four
)


def create_report(
    argument_one: int, argument_two: int, argument_three: int
) -> None:
    print(argument_one)
```

### Trailing commas

When a list of items is split over several lines with one item per line, end the last item with a comma.
The formatter keeps a list that ends with a comma on separate lines, even if it would fit on one line.

```python
golomb4 = [
    0,
    1,
    4,
    6,
]
```

### Parentheses

Use parentheses sparingly.
Do not use them around the conditions of `if` and `while` statements, or around return values, unless they are needed for line joining or for tuples.

```python
# Good:
if foo:
    bar()
return spam, beans
for x, y in dict.items():
    ...

# Bad:
if (x):
    bar()
return (foo)
```

### Blank lines

Use two blank lines between top-level definitions, and one blank line between method definitions.
Do not put a blank line after a `def` line.
Use single blank lines within functions where it helps readability.

### Whitespace

Follow the standard typographic rules for spaces around punctuation:

- No whitespace inside parentheses, brackets or braces.
- No whitespace before a comma, semicolon or colon, but whitespace after them, except at the end of a line.
- No whitespace before the opening parenthesis of a call or the opening bracket of an index.
- One space around assignment, comparison and boolean operators.
- No spaces around `=` for keyword arguments and default values, except when a type annotation is present.
- No alignment of tokens on consecutive lines.

```python
# Good:
spam(ham[1], {'eggs': 2}, [])
x = 1
y = x * 2 + 1


def complex(real: float, imag: float = 0.0) -> Magic:
    return Magic(real, imag)


def func(a, b=0):
    return a + b


# Bad:
spam( ham[ 1 ], { 'eggs': 2 }, [ ] )
x             = 1
y=x*2+1


def complex(real: float, imag: float=0.0) -> Magic:
    return Magic(real, imag)
```

### Statements

Put each statement on its own line.
Do not end lines with semicolons, and do not use semicolons to put two statements on one line.

```python
# Good:
if foo:
    bar(foo)

# Bad:
if foo: bar(foo)
```

## Naming

### Rules by identifier type

| Type | Public | Internal |
| --- | --- | --- |
| Packages | `lower_with_under` | |
| Modules | `lower_with_under` | `_lower_with_under` |
| Classes | `CapWords` | `_CapWords` |
| Exceptions | `CapWords` | |
| Functions | `lower_with_under()` | `_lower_with_under()` |
| Global and class constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` |
| Global and class variables | `lower_with_under` | `_lower_with_under` |
| Instance variables | `lower_with_under` | `_lower_with_under` |
| Method names | `lower_with_under()` | `_lower_with_under()` |
| Function and method parameters | `lower_with_under` | |
| Local variables | `lower_with_under` | |
| Type variables | `CapWords` or `T` | `_CapWords` or `_T` |

Abbreviations in `CapWords` names are written in upper case: `HTTPServerError`, not `HttpServerError`.

### Internal names

A single leading underscore marks a module, class, function or variable as internal to its module or class.
Do not use two leading underscores, which trigger name mangling and make testing harder.

### Names to avoid

- Single character names, except for counters and iterators (`i`, `j`, `k`, `v`), `e` for an exception in an `except` block, `f` for a file handle in a `with` statement, and type variables.
- Dashes in any package or module name.
- Names that start and end with two underscores, which are reserved for Python.
- Names that include the type of the value, such as `id_to_name_dict`.
- Abbreviations that are unfamiliar to readers outside the project.

```python
# Good:
users_by_id = {}
num_errors = 0

# Bad:
id_to_user_dict = {}
nerr = 0
```

### Self and cls

The first parameter of an instance method is always named `self`, and the first parameter of a class method is always named `cls`.

### Exception names

Exception classes end with `Error`, unless they are not errors.
Do not repeat the module name: use `user_store.NotFoundError`, not `user_store.UserStoreNotFoundError`.

### Test names

Test functions are named `test_<unit>_<behavior>`, so that a failure says what is broken.

```python
def test_load_user_returns_none_for_unknown_id():
    assert user_store.load('unknown') is None
```

## Language rules

### Exceptions

Use exceptions for errors.
Use the built-in exception classes when they fit, such as `ValueError` for an invalid argument.

```python
def connect(port: int) -> Connection:
    """Connects to the given port.

    Raises:
        ValueError: If the port is not between 1024 and 65535.
    """
    if not 1024 <= port <= 65535:
        raise ValueError(f'Invalid port: {port}')
    ...
```

- Do not use `assert` to validate arguments or other conditions that must hold, as asserts are removed when Python runs with `-O`.
  Use `assert` in tests and for checks that are only meant for development.
- Define your own exceptions by inheriting from an existing exception class.
- Never use a bare `except:`.
  Do not catch `Exception` unless you re-raise it, or you are at a boundary where errors must not propagate, such as the top of a thread.
- Keep the code in a `try` block as small as possible.
- Use `finally` or a `with` statement for cleanup.
- Use `raise ... from err` when raising a new exception while handling another one, so the original cause is kept.

```python
try:
    config = parse(text)
except json.JSONDecodeError as err:
    raise ConfigError(f'Invalid configuration in {path}') from err
```

### Mutable global state

Avoid mutable global state.
Module-level constants are fine, and are named in `CAPS_WITH_UNDER`.
If mutable global state is needed, make it internal with a leading underscore and access it through functions.

### Nested functions and classes

Nested functions and classes are fine when they close over a local variable.
Do not nest a function or class only to hide it from users of the module.
Give it a leading underscore at module level instead, so that it can be tested.

### Comprehensions and generator expressions

Use comprehensions and generator expressions for simple cases.
Each part must fit on one line, and there may be only one `for` clause and one filter.
Use a loop when it gets more complicated.

```python
# Good:
names = [user.name for user in users if user.is_active]
squares = {x: x * x for x in range(10)}
total = sum(x * x for x in numbers)

# Bad:
cells = [(row, col) for row in range(8) for col in range(8) if row != col]
```

### Default iterators and operators

Use the default iterators and the `in` operator of types that support them, such as lists, dictionaries and files.

```python
# Good:
for key in adict:
    ...
if obj in alist:
    ...
for line in afile:
    ...
for k, v in adict.items():
    ...

# Bad:
for key in adict.keys():
    ...
for line in afile.readlines():
    ...
```

### Generators

Use generators where they make the code clearer, such as when producing a large or infinite sequence.
Document a generator with a `Yields:` section instead of `Returns:`.

### Lambda functions

Lambdas are fine for one-line functions, such as a sort key.
Do not assign a lambda to a name; use `def` instead.
Prefer the functions from the `operator` module, such as `operator.mul`, over lambdas that only apply an operator.

```python
# Good:
users.sort(key=lambda user: user.last_name)


def square(x: int) -> int:
    return x * x


# Bad:
square = lambda x: x * x
```

### Conditional expressions

Conditional expressions are fine for simple cases.
Each part must fit on one line.
Use a full `if` statement when it gets more complicated.

```python
label = 'yes' if predicate(value) else 'no'
```

### Default argument values

Never use a mutable object, such as a list or a dictionary, as a default value.
The default is created once, when the function is defined, and is shared between all calls.

```python
# Good:
def foo(a: int, b: Sequence[int] | None = None) -> None:
    if b is None:
        b = []
    ...


# Bad:
def foo(a: int, b: list[int] = []) -> None:
    b.append(a)
```

Do not use a function call as a default value either, as it is only evaluated once.

### Properties

Use `@property` for values that are cheap to compute and have no side effects.
Do not use properties for expensive work, and do not write trivial getters and setters; use a public attribute instead.

```python
class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    @property
    def area(self) -> float:
        """The area of the square."""
        return self.side * self.side
```

### True and false evaluations

Use the implicit false of empty sequences and collections.

```python
# Good:
if not users:
    print('No users')

# Bad:
if len(users) == 0:
    print('No users')
```

- Compare with `None` using `is` and `is not`, never `==`.
- Write `if x is not None:` when you mean that `x` is not `None`, as `if x:` is also false for `0` and `''`.
- Never compare a boolean with `==`, such as `if greeting == True:`.
- Compare integers with `0` explicitly, as their value is usually what matters: `if i % 10 == 0:`.

### Decorators

Use decorators when there is a clear advantage.
A decorator should be well documented and must not depend on files, sockets or other external state when it is applied, which happens on import.

Do not use `@staticmethod`.
Write a module-level function instead.
Use `@classmethod` only for named constructors and for functions that change class-wide state.

### Data classes and enums

Use `dataclasses.dataclass` for classes that mainly hold data, and `enum.Enum` for a fixed set of values.

```python
@dataclasses.dataclass(frozen=True)
class Point:
    x: float
    y: float


class Color(enum.Enum):
    RED = 'red'
    GREEN = 'green'
```

### Files and other resources

Close files, sockets and other resources explicitly, with a `with` statement.

```python
path = pathlib.Path('hello.txt')
with path.open(encoding='utf-8') as hello_file:
    for line in hello_file:
        print(line)
```

Always pass `encoding` when opening a text file, since the default depends on the operating system.
Use `pathlib.Path` instead of `os.path` and the built-in `open()` for working with files and paths.

### Strings

Use f-strings to format values into strings.
Do not build strings with `+` in a loop; collect the parts in a list and join them.

```python
# Good:
greeting = f'Hello, {name}!'
items = ''.join(f'<li>{item}</li>' for item in items_list)

# Bad:
greeting = 'Hello, ' + name + '!'
items = ''
for item in items_list:
    items += '<li>' + item + '</li>'
```

Use single quotes for strings, and double quotes only when the string contains a single quote.

### Logging

Pass a format string with `%` placeholders and the values as arguments to logging functions, instead of an f-string.
The message is then only formatted when it is logged.

```python
# Good:
logger.info('Loaded %d users from %s', count, path)

# Bad:
logger.info(f'Loaded {count} users from {path}')
```

### Threading and concurrency

Do not rely on the atomicity of built-in types.
Use `queue.Queue` to pass data between threads, and the locks in `threading` to protect shared state.
Prefer `concurrent.futures` for running work in parallel, and `asyncio` for code that waits on a lot of I/O.

### Power features

Avoid metaclasses, access to bytecode, on-the-fly compilation, dynamic inheritance, changes to object parents, import hacks, reflection such as `getattr()` games, and changes to system internals.
They make code hard to read and to debug.
Standard library features that use them internally, such as `abc.ABCMeta`, `dataclasses` and `enum`, are fine.

### Global statements

Do not use the `global` and `nonlocal` statements.

### Function length

Prefer small, focused functions.
If a function is longer than about 40 lines, consider whether it can be split up without harming the structure of the program.

### The main guard

Even a file that is meant to be run directly should be importable, so that it can be tested.
Put the top-level code in a `main()` function, and call it from a main guard.

```python
def main() -> None:
    args = parse_args()
    run(args)


if __name__ == '__main__':
    main()
```

## Type annotations

### Annotate public APIs

Annotate the parameters and return types of all public functions and methods.
Annotating internal functions is encouraged.
Do not annotate `self` and `cls`.

```python
def fetch_users(query: str, limit: int = 10) -> list[User]:
    return store.query(query, limit=limit)
```

Annotate functions that return nothing with `-> None`, including `__init__`.

### Built-in generics and unions

Use the built-in collection types for annotations, such as `list[int]` and `dict[str, int]`, instead of `typing.List` and `typing.Dict`.
Use `X | None` instead of `Optional[X]`, and `X | Y` instead of `Union[X, Y]`.

```python
# Good:
def find(names: list[str], name: str) -> int | None:
    return names.index(name) if name in names else None


# Bad:
def find(names: List[str], name: str) -> Optional[int]:
    return names.index(name) if name in names else None
```

### Abstract parameter types

Use the abstract types from `collections.abc`, such as `Sequence`, `Mapping` and `Iterable`, for parameters, so that callers can pass any matching type.
Use concrete types for return values.

```python
def total_length(names: Sequence[str]) -> int:
    return sum(len(name) for name in names)
```

### Type variables and aliases

Use the type parameter syntax for generic functions and classes, and the `type` statement for type aliases.

```python
type UserId = int


def first[T](items: Sequence[T]) -> T:
    return items[0]
```

### The Any type

Avoid `Any`.
Use `object` when any value is accepted, a `Protocol` when the value needs certain methods, or a type variable when the type of a parameter and the result are connected.

### Forward references

Use a string for a type that is not defined yet, such as a class that refers to itself.
Import modules that are only needed for annotations inside `if TYPE_CHECKING:`, to avoid circular imports.

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lrssn.storage import user_store


class Node:
    def add_child(self, child: 'Node') -> None:
        self.children.append(child)
```

### Ignoring type errors

Only suppress a type error with `# type: ignore[code]`, naming the specific error, and add a comment that explains why.

## Comments and docstrings

### Docstrings

Docstrings use triple double quotes (`"""`).
They start with a one-line summary of at most 80 characters that ends with a period.
If there is more to say, the summary is followed by a blank line and the rest of the docstring.

### Module docstrings

Every file starts with a docstring that describes its contents and usage.

```python
"""A one-line summary of the module, terminated by a period.

Leave one blank line. The rest of this docstring should contain an overall
description of the module, and optionally a usage example.

Typical usage example:

    foo = ClassFoo()
    bar = foo.function_bar()
"""
```

### Function docstrings

Every public function has a docstring, unless it is short and obvious.
The docstring describes what the function does and how to call it, not how it is implemented.
It is written in the descriptive style ("Fetches rows from a table.") rather than the imperative ("Fetch rows from a table.").

Describe the parameters, the return value and the exceptions in sections.
Continuation lines within a section are indented by 4 more spaces.

| Section | Content |
| --- | --- |
| `Args:` | Each parameter by name, followed by a colon and a description |
| `Returns:` | The type and meaning of the return value. Use `Yields:` for generators |
| `Raises:` | Each exception that is part of the interface, and when it is raised |

```python
def fetch_rows(
    table: Table,
    keys: Sequence[str],
    strict: bool = False,
) -> Mapping[str, tuple[str, ...]]:
    """Fetches rows from a table.

    Retrieves the rows for the given keys from the table. Keys that are
    missing from the table are left out of the result.

    Args:
        table: An open table instance.
        keys: The keys of the rows to fetch.
        strict: If True, only rows with values set for all keys are
            returned.

    Returns:
        A dict that maps keys to the row data that was fetched. Each row is
        represented as a tuple of strings.

    Raises:
        OSError: An error occurred while accessing the table.
    """
```

A method that overrides a method of a base class does not need a docstring if it is decorated with `@typing.override`, unless it changes the behavior.

### Class docstrings

Classes have a docstring below the class definition that describes what an instance represents.
Public attributes are documented in an `Attributes:` section.

```python
class SampleClass:
    """A summary of what the class represents.

    Longer class information goes here.

    Attributes:
        likes_tea: Whether the drinker prefers tea over coffee.
        cups: The number of cups poured so far.
    """

    def __init__(self, likes_tea: bool = False) -> None:
        """Creates a drinker with the given preference.

        Args:
            likes_tea: Whether the drinker prefers tea over coffee.
        """
        self.likes_tea = likes_tea
        self.cups = 0
```

### Block and inline comments

Comment tricky, non-obvious, interesting or important parts of the code.
Explain why the code does something, not what it does.

Inline comments are separated from the code by at least two spaces, and start with `#` and a single space.

```python
# Retry with exponential backoff. The delay doubles after each failed
# attempt, up to the cap, so that a struggling server has time to
# recover before the next request reaches it.

if i & (i - 1) == 0:  # True if i is 0 or a power of 2.
    ...
```

### TODO comments

Write `TODO` comments with a link to an issue, such as `TODO(#42)`. If no issue exists yet, open one first.

```python
# TODO(#41): Use a heap instead of sorting the whole list.
# TODO(#42): Handle time zones.
```

## Testing

Write tests with [pytest](https://docs.pytest.org/).

- Put tests in files that end with `_test.py`, next to the code they test.
- Use plain `assert` statements, which pytest turns into detailed failure messages.
- Use `pytest.mark.parametrize` for tests that run the same logic with different inputs.
- Use fixtures such as `tmp_path` for temporary files.

```python
import pytest

from lrssn.util import durations


@pytest.mark.parametrize(
    ('text', 'expected'),
    [
        ('5s', 5),
        ('2m', 120),
        ('1h', 3600),
    ],
)
def test_parse_returns_seconds(text, expected):
    assert durations.parse(text) == expected


def test_parse_rejects_empty_string():
    with pytest.raises(ValueError):
        durations.parse('')
```

## Tooling

### Ruff

Use [Ruff](https://docs.astral.sh/ruff/) to format and lint the code.
Add this configuration to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 80
indent-width = 4
target-version = "py312"

[tool.ruff.format]
quote-style = "single"
docstring-code-format = true

[tool.ruff.lint]
select = [
    "ANN",  # flake8-annotations
    "B",  # flake8-bugbear
    "D",  # pydocstyle
    "E",  # pycodestyle errors
    "F",  # pyflakes
    "I",  # isort
    "N",  # pep8-naming
    "PTH",  # flake8-use-pathlib
    "RUF",  # Ruff-specific rules
    "SIM",  # flake8-simplify
    "UP",  # pyupgrade
    "W",  # pycodestyle warnings
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
force-single-line = true
force-sort-within-sections = true
single-line-exclusions = ["collections.abc", "typing", "typing_extensions"]

[tool.ruff.lint.per-file-ignores]
"*_test.py" = ["ANN", "D"]
```

Format and lint all files with:

```bash
ruff format .
ruff check .
```

Fix the warnings instead of suppressing them.
If a warning really does not apply, suppress it on the line with `# noqa: <code>` and a comment that explains why.

### Type checking

Check the type annotations with [mypy](https://mypy-lang.org/) in strict mode.

```toml
[tool.mypy]
python_version = "3.12"
strict = true
```

```bash
mypy .
```

### Dependencies

Declare dependencies in `pyproject.toml`, and use a virtual environment for every project.
Never install project dependencies into the system Python.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --editable '.[dev]'
```

## See also

- [Google Python style guide](https://google.github.io/styleguide/pyguide.html)
- [PEP 8](https://peps.python.org/pep-0008/)
- [PEP 257](https://peps.python.org/pep-0257/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
