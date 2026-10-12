# Rust Style Guide

A style guide for Rust.
It is based on the official [Rust style guide](https://doc.rust-lang.org/style-guide/), the [Rust API guidelines](https://rust-lang.github.io/api-guidelines/) and the lints of [Clippy](https://doc.rust-lang.org/clippy/).

Deviations from the official style guide:

- Lines are at most 80 characters long instead of 100, following the house rule in `.editorconfig`.

## Table of contents

[TOC]

## Edition and toolchain

New crates use the 2024 edition.
Pin the toolchain of a project with a `rust-toolchain.toml` file, so that everyone builds with the same compiler and lints, and set the minimum supported Rust version with `rust-version` in `Cargo.toml`.

```toml
[package]
name = "style-check"
version = "1.0.0"
edition = "2024"
rust-version = "1.85"
```

```toml
[toolchain]
channel = "1.97.0"
components = ["clippy", "rustfmt"]
```

## Source files

### File names

File names are lowercase, with underscores between words, and have the `.rs` extension.
A module named `config` lives in `config.rs`, and its submodules in a folder named `config`.
Do not use `mod.rs` files.

```text
src/
├── config/
│   ├── parser.rs
│   └── validation.rs
├── config.rs
├── lib.rs
└── main.rs
```

### File encoding: UTF-8

Source files are encoded in UTF-8, which the compiler requires.

### Package names

Package names are lowercase, with hyphens between words, such as `style-check`.
Cargo turns the hyphens into underscores in the crate name, so the crate is used as `style_check`.
Do not add `-rs` or `-rust` to the name.

### Crate layout

Follow Cargo's standard layout:

| Path | Content |
| --- | --- |
| `src/lib.rs` | The library crate |
| `src/main.rs` | The main binary |
| `src/bin/*.rs` | Additional binaries |
| `tests/` | Integration tests |
| `examples/` | Example programs |
| `benches/` | Benchmarks |

Put the logic of a program in the library, and keep `main.rs` small.
The library can then be tested and reused.

## Source file structure

A file consists of the following, in order:

1. Inner attributes and the module documentation (`//!`).
1. `mod` declarations.
1. `use` declarations.
1. Constants and statics.
1. Types, each followed by its `impl` blocks.
1. Functions.
1. The unit tests, in a `#[cfg(test)] mod tests` at the end of the file.

```rust
//! Loading and validating the configuration file.

mod parser;

use std::fs;
use std::path::Path;

use serde::Deserialize;

use crate::error::Error;

const DEFAULT_PORT: u16 = 8080;

/// The application configuration.
#[derive(Debug, Deserialize)]
pub struct Config {
    pub port: u16,
}

impl Config {
    /// Reads the configuration from a file.
    pub fn load(path: &Path) -> Result<Self, Error> {
        let text = fs::read_to_string(path)?;
        parser::parse(&text)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_port_is_unprivileged() {
        assert!(DEFAULT_PORT > 1024);
    }
}
```

### Imports

Group the `use` declarations into blocks separated by a blank line, in this order:

1. The standard library: `std`, `core` and `alloc`.
1. External crates.
1. The current crate: `crate`, `super` and `self`.

`rustfmt` sorts the declarations within each block, but does not create the blocks, so add the blank lines yourself.

Import types, traits and macros by name.
Import the parent module of functions, so that it is clear at the call site where a function comes from.

```rust
// Good:
use std::collections::HashMap;
use std::fs;

let text = fs::read_to_string(path)?;
let mut counts = HashMap::new();

// Bad: read_to_string could be a local function.
use std::fs::read_to_string;

let text = read_to_string(path)?;
```

Do not use glob imports (`use foo::*`), except for preludes that are designed for them and `use super::*` in test modules.

Use `crate::` for paths within the crate, and `super::` only for the direct parent module.

### Visibility

Keep items private unless they are needed outside their module.
Use `pub(crate)` for items that are shared within the crate but are not part of its public API.

## Formatting

Do not format code by hand.
Use `rustfmt` with the configuration in [Tooling](#tooling), and let it decide.
The rules below describe what the formatter produces.

### Indentation and line length

Indent by 4 spaces, never tabs.
Lines are at most 80 characters long.

When a list of arguments, parameters or fields does not fit on one line, put each element on its own line, indented by 4 spaces, with a trailing comma and the closing delimiter on a line of its own.

```rust
fn create_user(
    name: &str,
    email: &str,
    roles: &[Role],
    settings: Settings,
) -> Result<User, Error> {
    // …
}
```

### Braces

Opening braces go on the same line as the item or expression they belong to.
Closing braces go on their own line, unless the block is empty.

```rust
if config.verbose {
    println!("Loaded {} users", users.len());
} else {
    log::debug!("Loaded users");
}
```

### Where clauses

When the bounds of a generic item do not fit in the signature, move them to a `where` clause.
`rustfmt` puts each bound on its own line.

```rust
fn print_all<I>(items: I)
where
    I: IntoIterator,
    I::Item: fmt::Display,
{
    for item in items {
        println!("{item}");
    }
}
```

### Blank lines

Separate items with a single blank line.
Do not start or end a block with a blank line.

### Comments

Prefer line comments (`//`) over block comments (`/* … */`).
Put a single space after `//`.

### Attributes

Put each attribute on its own line, directly before the item it applies to.
Combine derives into a single `#[derive]`.

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub struct Version {
    pub major: u64,
    pub minor: u64,
    pub patch: u64,
}
```

## Naming

### Rules by item type

| Item | Style |
| --- | --- |
| Crates and modules | `snake_case` |
| Types: structs, enums, unions, traits and type aliases | `UpperCamelCase` |
| Enum variants | `UpperCamelCase` |
| Functions and methods | `snake_case` |
| Macros | `snake_case!` |
| Local variables and parameters | `snake_case` |
| Constants and statics | `SCREAMING_SNAKE_CASE` |
| Type parameters | Short `UpperCamelCase`, usually one letter: `T` |
| Lifetimes | Short `lowercase`: `'a`, `'de`, `'src` |
| Cargo features | `kebab-case`, without words like `use-` or `with-` |

### Acronyms

Treat acronyms and contractions as one word in `UpperCamelCase` and `snake_case`.

```rust
// Good:
struct HttpServer;
struct Uuid;
fn parse_url() {}

// Bad:
struct HTTPServer;
struct UUID;
```

This matches the TypeScript guide, and differs from the Go guide, which keeps acronyms in one case.

### Constructors

Name the main constructor `new`.
Name other constructors `with_` followed by what is different, and constructors that convert from another type `from_` followed by the type.

```rust
impl Buffer {
    pub fn new() -> Self {
        Self::with_capacity(DEFAULT_CAPACITY)
    }

    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            data: Vec::with_capacity(capacity),
        }
    }
}
```

### Conversions

Name conversion methods after their cost and ownership:

| Prefix | Cost | Ownership | Example |
| --- | --- | --- | --- |
| `as_` | Free | Borrowed to borrowed | `str::as_bytes` |
| `to_` | Expensive | Borrowed to owned, or by value for `Copy` types | `str::to_lowercase` |
| `into_` | Variable | Owned to owned, consumes `self` | `String::into_bytes` |

### Getters

Getters are named after the field, without a `get_` prefix.
A method named `get` is only used when there is one obvious thing to get, such as `Cell::get`.

```rust
impl User {
    pub fn name(&self) -> &str {
        &self.name
    }

    pub fn set_name(&mut self, name: String) {
        self.name = name;
    }
}
```

### Iterators

Methods that return iterators are named `iter`, `iter_mut` and `into_iter`, and the iterator types are named after the method, such as `Iter` and `IntoIter`.

### Booleans

Methods and variables that return or hold a `bool` read as a question: `is_empty`, `has_children`, `can_retry`.

### Error types

Name error types after the operation that fails, in verb-object-error order: `ParseConfigError`, not `ConfigParseError`.
A module with a single error type may call it `Error`.

## Language features

### Borrowing

Take borrowed parameters when a function only reads a value.
Accept the most general borrowed type: `&str` instead of `&String`, `&[T]` instead of `&Vec<T>` and `&Path` instead of `&PathBuf`.

```rust
// Good:
fn count_words(text: &str) -> usize {
    text.split_whitespace().count()
}

// Bad: callers that have a &str must allocate a String first.
fn count_words(text: &String) -> usize {
    text.split_whitespace().count()
}
```

Take ownership when the function stores the value.
Constructors may accept `impl Into<String>` so that callers can pass either a `&str` or a `String`.

Do not add `.clone()` only to satisfy the borrow checker.
First check whether a borrow or a change in ownership solves the problem, and clone explicitly when a copy is really needed.

### Mutability

Declare variables without `mut` unless they change.
Prefer creating a new value over changing an existing one when it keeps the code simple.

Shadowing a variable is fine for a value that is transformed step by step.

```rust
let input = input.trim();
let input = input.to_lowercase();
```

### Error handling

Return `Result` for errors that the caller can handle, and propagate them with `?`.
Use `panic!` only for bugs, such as a broken invariant that cannot happen in a correct program.

- Do not use `unwrap()` outside of tests and examples.
- Use `expect()` only where failure is impossible, and write the message as the reason why it cannot fail.
- Error messages start with a lowercase letter and do not end with punctuation, as they are often wrapped in other messages.
- Do not use `String` as an error type.

```rust
// Good:
let port: u16 = text.parse()?;
let localhost: IpAddr = "127.0.0.1".parse().expect("the literal is valid");

// Bad:
let port: u16 = text.parse().unwrap();
```

Libraries define their own error types, which implement `std::error::Error` and `Display`.
The [thiserror](https://crates.io/crates/thiserror) crate removes most of the boilerplate.

```rust
#[derive(Debug, thiserror::Error)]
pub enum LoadConfigError {
    #[error("read config file")]
    Io(#[from] io::Error),
    #[error("invalid port {0}")]
    InvalidPort(u32),
}
```

Applications may use [anyhow](https://crates.io/crates/anyhow) and add context to each error.

```rust
let config = Config::load(&path)
    .with_context(|| format!("load config from {}", path.display()))?;
```

### Option

Use the methods of `Option` instead of matching on it when they make the code shorter and clearer, such as `map`, `and_then`, `unwrap_or` and `ok_or`.
Use `let else` to return early when a value is missing.

```rust
let Some(user) = users.get(&id) else {
    return Err(Error::UnknownUser(id));
};
```

### Pattern matching

Match exhaustively on enums of your own crate, without a wildcard `_` arm.
When a variant is added, the compiler then points out every `match` that needs to handle it.

```rust
match shape {
    Shape::Circle { radius } => PI * radius * radius,
    Shape::Square { side } => side * side,
}
```

Use `matches!` for a match that only produces a `bool`.

```rust
let is_weekend = matches!(day, Day::Saturday | Day::Sunday);
```

### Iterators

Prefer iterators over index loops.
They cannot go out of bounds and often express the intent better.

```rust
// Good:
for user in &users {
    notify(user);
}

let names: Vec<&str> = users.iter().map(User::name).collect();

// Bad:
for i in 0..users.len() {
    notify(&users[i]);
}
```

Split long iterator chains with one adapter per line, which `rustfmt` does automatically, and give complex closures a name as a function.

### Types

#### Newtypes

Wrap primitive values with a meaning in a newtype, so that the compiler catches mixed-up arguments.

```rust
pub struct UserId(u64);
pub struct OrderId(u64);

fn cancel_order(user: UserId, order: OrderId) {
    // …
}
```

#### Enums instead of booleans

Use an enum instead of a `bool` parameter, so that the call site says what the argument means.

```rust
// Good:
widget.redraw(Redraw::Now);

// Bad: what does true mean?
widget.redraw(true);
```

#### Common traits

Derive the common traits for public types eagerly, as other crates cannot add them later: `Debug`, `Clone`, `PartialEq`, `Eq`, `Hash`, `PartialOrd`, `Ord` and `Default`, where they make sense.
Every public type implements `Debug`.

#### Non-exhaustive types

Mark public structs and enums that may get more fields or variants with `#[non_exhaustive]`, so that adding them is not a breaking change.

#### Numeric conversions

Use `From` and `TryFrom` to convert between numeric types.
Do not use `as` for conversions that can lose information, as it silently truncates the value.

```rust
// Good:
let small = u8::try_from(value)?;
let big = u64::from(small);

// Bad: silently truncates values above 255.
let small = value as u8;
```

### Traits and generics

- Implement the standard traits instead of ad hoc methods: `Display` instead of a `to_string` method, `FromStr` instead of a `parse` function, `From` instead of a conversion function, and `Default` instead of a constructor without arguments.
- Use `impl Trait` in argument position for simple generic parameters, and named type parameters when they need several bounds or appear more than once.
- Use trait objects (`dyn Trait`) when values of different types are stored together.

```rust
fn log_all(messages: impl IntoIterator<Item = impl fmt::Display>) {
    for message in messages {
        println!("{message}");
    }
}
```

### Lifetimes

Leave lifetimes out wherever the elision rules allow it.
When several lifetimes are needed, give them names that say what they refer to.

```rust
struct Parser<'src> {
    input: &'src str,
}
```

### Unsafe code

Avoid `unsafe`.
Crates that do not need it forbid it with `unsafe_code = "forbid"` in their [lints](#lints).

When `unsafe` is needed:

- Keep each `unsafe` block as small as possible.
- Write a `// SAFETY:` comment before every `unsafe` block that explains why the code is sound.
- Document the conditions the caller must uphold in a `# Safety` section on every `unsafe fn`.

```rust
// SAFETY: `index` is less than `self.len`, which is checked above, and the
// buffer always holds `self.len` initialized elements.
let value = unsafe { self.buffer.get_unchecked(index) };
```

### Macros

Prefer functions and generics over macros.
Write a `macro_rules!` macro only when a function cannot do the job, such as for a variable number of arguments of different types.

### Concurrency

- Use scoped threads (`std::thread::scope`) for threads that borrow local data.
- Share data between threads with `Arc`, and protect changing data with a `Mutex` or `RwLock`, or send it over a channel.
- In async code, never block the executor.
  Run blocking work with the runtime's blocking task function, such as `tokio::task::spawn_blocking`.
- Never hold a `MutexGuard` from `std::sync` across an `.await`.

### Suppressing lints

Suppress a lint with `#[expect]` and a reason, instead of `#[allow]`.
`#[expect]` warns when the lint no longer fires, so that stale suppressions are removed.

```rust
#[expect(
    clippy::cast_possible_truncation,
    reason = "the file format limits files to 4 GiB"
)]
let size = metadata.len() as u32;
```

## Comments and documentation

### Documentation comments

Document every public item with a `///` comment, and every crate and public module with a `//!` comment.

- The first line is a one-sentence summary that ends with a period.
- Link to other items with intra-doc links, such as ``[`Config`]``.
- Add the sections that apply, in this order: `# Examples`, `# Errors`, `# Panics` and `# Safety`.

````rust
/// Parses a duration such as `5s` or `2m`.
///
/// # Examples
///
/// ```
/// use std::time::Duration;
///
/// let duration = style_check::parse_duration("5s")?;
/// assert_eq!(duration, Duration::from_secs(5));
/// # Ok::<(), style_check::ParseDurationError>(())
/// ```
///
/// # Errors
///
/// Returns an error if the text is not a number followed by a unit.
pub fn parse_duration(text: &str) -> Result<Duration, ParseDurationError> {
    // …
}
````

Examples in documentation are compiled and run as tests.
Use `?` in examples instead of `unwrap()`, so that they show good error handling.

### Implementation comments

Comments inside functions explain why the code does something, not what it does.

### TODO comments

Write `TODO` comments with a link to an issue, such as `TODO(#42)`. If no issue exists yet, open one first.

```rust
// TODO(#41): Cache the parsed configuration.
// TODO(#42): Support TOML files.
```

## Testing

### Unit tests

Put unit tests in a `tests` module at the end of the file they test, and import the parent module with `use super::*`.
Name tests after the behavior they check.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_duration_accepts_minutes() {
        assert_eq!(parse_duration("2m"), Ok(Duration::from_secs(120)));
    }

    #[test]
    fn parse_duration_rejects_empty_input() {
        assert!(parse_duration("").is_err());
    }
}
```

Tests may return a `Result`, so that they can use `?`.

### Integration tests

Put tests that use only the public API in the `tests` folder.
Each file there is compiled as a separate crate.

## Tooling

### rustfmt

Format the code with `cargo fmt`.
Add this `rustfmt.toml` to the root of the repository:

```toml
max_width = 80
newline_style = "Unix"
```

### Clippy

Run [Clippy](https://doc.rust-lang.org/clippy/) on every change, and treat its warnings as errors in continuous integration.

```bash
cargo clippy --all-targets --all-features -- --deny warnings
```

### Lints

Configure the lints of the compiler and Clippy in the `[lints]` table of `Cargo.toml`, so that they apply to every build.

```toml
[lints.rust]
missing_docs = "warn"
unsafe_code = "forbid"

[lints.clippy]
pedantic = { level = "warn", priority = -1 }
unwrap_used = "warn"
undocumented_unsafe_blocks = "warn"
```

Remove `unsafe_code = "forbid"` in crates that need `unsafe`, and keep `undocumented_unsafe_blocks` to require the `SAFETY:` comments.

### Dependencies

Commit `Cargo.lock` for every crate, so that builds are reproducible.
Check the dependencies for known vulnerabilities with [cargo-audit](https://crates.io/crates/cargo-audit) or [cargo-deny](https://crates.io/crates/cargo-deny).

```bash
cargo audit
```

### Continuous integration

Check the formatting, the lints and the tests on every pull request.

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- --deny warnings
cargo test --all-features
```

## See also

- [The Rust style guide](https://doc.rust-lang.org/style-guide/)
- [Rust API guidelines](https://rust-lang.github.io/api-guidelines/)
- [Clippy lints](https://rust-lang.github.io/rust-clippy/master/)
- [The Rust programming language](https://doc.rust-lang.org/book/)
