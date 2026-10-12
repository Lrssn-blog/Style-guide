# Go Style Guide

A style guide for the Go language.
It is heavily based on the [Google Go style guide](https://google.github.io/styleguide/go/), [Effective Go](https://go.dev/doc/effective_go) and the [Go code review comments](https://go.dev/wiki/CodeReviewComments).

Deviations from the house rules:

- Go code is indented with tabs, not 4 spaces, because `gofmt` decides the formatting of all Go code and it uses tabs.
  The examples in this guide are shown with 4 spaces so that they display the same everywhere.
- Lines should stay within 80 columns, but `gofmt` does not wrap lines, so this is a soft limit.
  Prefer refactoring a long line over splitting it in an awkward place.

## Table of contents

[TOC]

## Principles

When the rules in this guide do not cover a situation, write the code that best serves these goals, in order of importance:

1. **Clarity**: the purpose and the reasoning of the code are clear to the reader.
1. **Simplicity**: the code does what it needs to in the simplest way possible.
1. **Concision**: the code has a high signal to noise ratio.
1. **Maintainability**: the code is easy to change correctly.
1. **Consistency**: the code looks like the code around it and the rest of the code base.

Code is read far more often than it is written, so optimize for the reader.

## Source files

### File names

File names are lowercase, with underscores between words, and have the `.go` extension.

```text
user_service.go
user_service_test.go
```

Some suffixes have a special meaning to the Go tool:

| Suffix | Meaning |
| --- | --- |
| `_test.go` | Test code, only compiled by `go test` |
| `_linux.go`, `_windows.go` | Only compiled for that operating system |
| `_amd64.go`, `_arm64.go` | Only compiled for that architecture |

Use the operating system suffixes instead of build constraints when a whole file is specific to one platform.

### File encoding: UTF-8

Source files are encoded in UTF-8, which the Go specification requires.

### Formatting is not optional

All Go code is formatted with `gofmt`.
There is no discussion about formatting in code review: if `gofmt` produces it, it is correct.
Configure your editor to run `gofmt` or `goimports` when a file is saved.

## Packages

### Package names

Package names are short, lowercase, single words.
Do not use underscores or mixed caps.

```go
// Good:
package user
package httputil

// Bad:
package user_service
package httpUtil
```

The package name is part of every reference to its contents, so choose a name that reads well when used: `bytes.Buffer`, `http.Server`, `json.Marshal`.

Avoid meaningless package names such as `util`, `common`, `helper`, `misc`, `base` or `types`.
They attract unrelated code and say nothing about what the package does.
Split the code into packages named after what they provide.

### Package size and layout

A package groups code that belongs together.
Do not split a package into many tiny packages, and do not put unrelated code into one big package.
A good test is whether a user of the package needs to import several packages to do one thing.

A typical module looks like this:

```text
mymodule/
├── cmd/
│   └── mytool/
│       └── main.go
├── internal/
│   └── storage/
│       ├── storage.go
│       └── storage_test.go
├── user/
│   ├── doc.go
│   ├── user.go
│   └── user_test.go
├── go.mod
└── go.sum
```

- Each command is a `main` package in its own folder under `cmd`.
- Packages that should not be imported by other modules go under `internal`, which the Go tool enforces.
- Keep the structure flat.
  Add folders when there is code to put in them, not in advance.

### Source file structure

A file consists of the following, in order:

1. License or copyright information, if present.
1. The package comment, in only one file of the package.
1. The `package` clause.
1. The imports.
1. The declarations.

Order the declarations so that the file reads from top to bottom.
Put a type first, followed by its constructor functions and its methods.
Constants and variables that belong together are grouped in a single `const` or `var` block.

### Imports

Imports are grouped into blocks separated by a blank line, in this order:

1. The standard library.
1. Third-party packages.
1. Packages from the same module.

```go
import (
    "context"
    "fmt"
    "os"

    "github.com/google/go-cmp/cmp"
    "golang.org/x/sync/errgroup"

    "example.com/mymodule/internal/storage"
)
```

`goimports` sorts the imports within each block and adds or removes imports as needed.

#### Import renaming

Do not rename imports unless the name collides with another import or is unclear.
When renaming, use a name that follows the rules for package names.

```go
import (
    "net/url"

    urlpb "example.com/mymodule/proto/url"
)
```

#### Blank imports

Blank imports (`import _ "..."`) import a package only for its side effects.
Only use them in `main` packages and tests, so that the dependency is visible where the program is put together.

```go
import (
    "database/sql"

    _ "github.com/lib/pq" // Registers the PostgreSQL driver.
)
```

#### Dot imports

Do not use dot imports (`import . "..."`).
They make it unclear where a name comes from.

## Formatting

`gofmt` handles indentation, alignment and spacing.
This section covers what `gofmt` leaves to you.

### Line length

There is no hard line length limit, but aim for 80 columns.
If a line is too long, it is usually better to refactor the code than to wrap the line.
Long string literals and URLs may exceed the limit.

Do not split a line before an indentation change, such as a function declaration or a conditional, if the result would make the continuation look like the body.

### Function signatures

Keep function signatures on one line when they fit.
When they do not fit, put each parameter group on its own line with a trailing comma, and the closing parenthesis on a line of its own.

```go
func (s *Server) HandleUpload(
    ctx context.Context,
    user *User,
    files []File,
    opts UploadOptions,
) (*Receipt, error) {
    // …
}
```

If a signature has many parameters, consider grouping them in an options struct.

### Function calls

Keep calls on one line when they fit.
Otherwise, break after the opening parenthesis, or factor arguments out into local variables.

```go
// Good:
receipt, err := s.HandleUpload(ctx, user, files, opts)

// Good:
receipt, err := s.HandleUpload(
    ctx, user, files, UploadOptions{Overwrite: true, Notify: false})
```

### Conditionals

Do not break the condition of an `if` statement over several lines.
Move parts of a long condition into well-named local variables instead.

```go
// Good:
inTransaction := db.CurrentStatus() == db.InTransaction
keysMatch := db.ValuesEqual(db.TransactionKey(), row.Key())
if inTransaction && keysMatch {
    return db.Error(db.TransactionError, "key mismatch")
}

// Bad:
if db.CurrentStatus() == db.InTransaction &&
    db.ValuesEqual(db.TransactionKey(), row.Key()) {
    return db.Error(db.TransactionError, "key mismatch")
}
```

### Composite literals

Use field names in struct literals for types from other packages.
Positional fields break when the type gets a new field.

```go
// Good:
r := csv.Reader{
    Comma:   ',',
    Comment: '#',
}

// Bad:
r := csv.Reader{',', '#', 4, false, false, false, false}
```

Multi-line composite literals have a trailing comma after the last element, and the closing brace on its own line at the indentation of the opening line.

Leave out repeated type names inside slice and map literals.

```go
// Good:
points := []Point{
    {X: 1, Y: 2},
    {X: 3, Y: 4},
}

// Bad:
points := []Point{
    Point{X: 1, Y: 2},
    Point{X: 3, Y: 4},
}
```

### Blank lines

Use blank lines to separate groups of related statements, but do not start or end a block with a blank line.

## Naming

### MixedCaps

Go names use `MixedCaps` or `mixedCaps`, never underscores.
The first letter decides whether a name is exported: `MaxLength` is visible outside the package and `maxLength` is not.

Constants follow the same rule.
Do not use `ALL_CAPS` or a `k` prefix.

```go
// Good:
const MaxPacketSize = 512

// Bad:
const MAX_PACKET_SIZE = 512
const kMaxPacketSize = 512
```

Underscores are only allowed in test function names, generated code and names that interact with the operating system or cgo.

### Initialisms

Initialisms and acronyms such as `URL`, `ID`, `HTTP` and `API` keep a consistent case: all upper case or all lower case.

| Good | Bad |
| --- | --- |
| `URL` | `Url` |
| `userID` | `userId` |
| `ServeHTTP` | `ServeHttp` |
| `xmlHTTPRequest` | `XmlHttpRequest` |

This is different from the TypeScript guide, which treats acronyms as words.
Follow the convention of the language.

### Name length

The length of a name should match the size of its scope.
A loop index used in three lines can be `i`, while a package-level variable needs a descriptive name.

```go
for i, user := range users {
    fmt.Println(i, user.Name)
}
```

Common short names are fine where the meaning is obvious, such as `r` for an `io.Reader`, `w` for an `io.Writer`, `ctx` for a `context.Context` and `err` for an error.

### Avoid repetition

The reader sees the package name, the type and the receiver together with a name.
Do not repeat them in the name.

| Repetitive | Better |
| --- | --- |
| `user.UserService` | `user.Service` |
| `widget.NewWidget` | `widget.New` |
| `db.LoadFromDatabase` | `db.Load` |
| `var userSlice []*User` | `var users []*User` |
| `func (c *Config) WriteConfigTo(w io.Writer)` | `func (c *Config) WriteTo(w io.Writer)` |

### Receiver names

Receiver names are one or two letters that abbreviate the type, and are the same for every method of the type.
Never use `this` or `self`.

```go
// Good:
func (s *Server) Start() error
func (s *Server) Stop() error

// Bad:
func (this *Server) Start() error
func (server *Server) Stop() error
```

### Getters and setters

Do not use a `Get` prefix for getters.
A setter, when needed, uses a `Set` prefix.

```go
func (u *User) Owner() string
func (u *User) SetOwner(owner string)
```

If a function is expensive or has side effects, use a verb that says so, such as `Fetch` or `Compute`.

### Interface names

One-method interfaces are named after the method with an `-er` suffix: `Reader`, `Writer`, `Formatter`, `Stringer`.

Do not give your own methods the names of well-known methods such as `Read`, `Write`, `Close`, `String` or `Error`, unless they have the same signature and meaning.

### Error names

Error variables start with `Err` and error types end with `Error`.

```go
var ErrNotFound = errors.New("not found")

type ValidationError struct {
    Field string
}
```

### Constants

Name constants after their role, not their value.

```go
// Good:
const MaxRetries = 3

// Bad:
const Three = 3
```

## Language features

### Variable declarations

Use `:=` when a variable is declared with a value.
Use `var` when the zero value is what you want, which tells the reader that the variable is filled in later.

```go
// Good:
count := len(items)
var buf bytes.Buffer

// Bad:
var count = len(items)
buf := bytes.Buffer{}
```

Prefer a `nil` slice over an empty slice literal.
A `nil` slice has length zero and works with `append`, `len` and `range`.

```go
// Good:
var names []string

// Bad:
names := []string{}
```

The exception is when the difference is visible, for example when encoding JSON, where a `nil` slice becomes `null` and an empty slice becomes `[]`.

### Size hints

Only give `make` a capacity when the final size is known and the code is performance sensitive.
Most code does not need size hints.

```go
users := make([]*User, 0, len(ids))
for _, id := range ids {
    users = append(users, lookup(id))
}
```

### Enumerations

Use a named type with `iota` for enumerations.
Start at `iota + 1`, or name the zero value `Unknown`, so that a missing value is not mistaken for a valid one.

```go
type Weekday int

const (
    WeekdayUnknown Weekday = iota
    Monday
    Tuesday
    Wednesday
)
```

### The any type

Use `any` instead of `interface{}`.
They are the same type, and `any` is shorter and easier to read.

### Pointers and values

#### Receiver type

Choose between pointer and value receivers with these rules:

- If the method changes the receiver, the receiver must be a pointer.
- If the type contains a `sync.Mutex` or another field that must not be copied, the receiver must be a pointer.
- If the type is a large struct, use a pointer.
- If the type is a map, function or channel, use a value.
- If the type is small and never changed, such as a `time.Time`, use a value.

Use the same kind of receiver for all methods of a type.
When in doubt, use a pointer receiver.

#### Passing pointers

Do not pass pointers to small values such as `string` or interface values only to avoid copying them.
Use pointers when the function needs to change the value, or when the value is large.

### Copying

Be careful when copying a struct from another package.
Types such as `sync.Mutex` and `bytes.Buffer` must not be copied after first use.

```go
// Bad: copies the mutex.
func process(c Counter) {
    c.mu.Lock()
    // …
}
```

### Interfaces

Interfaces belong in the package that uses them, not in the package that implements them.
The implementing package returns concrete types, so it can add methods without breaking anyone.

```go
// Package consumer defines what it needs.
package consumer

type UserStore interface {
    User(ctx context.Context, id string) (*User, error)
}

func Greet(ctx context.Context, store UserStore, id string) (string, error) {
    // …
}
```

- Accept interfaces and return concrete types.
- Keep interfaces small.
  The bigger the interface, the weaker the abstraction.
- Do not define an interface before there is a second implementation or a real need for one.
- Do not export an interface only to make mocking easier in tests.
  Tests can use the real implementation or define their own small interface.

To check at compile time that a type implements an interface, assign it to a blank variable:

```go
var _ io.Writer = (*LogWriter)(nil)
```

### Generics

Use generics when the same code would otherwise be written for several types, such as functions on slices and maps or generic data structures.
Write the code for a single type first, and only make it generic when it is needed.

```go
func Filter[T any](items []T, keep func(T) bool) []T {
    var result []T
    for _, item := range items {
        if keep(item) {
            result = append(result, item)
        }
    }
    return result
}
```

- Do not use generics where an interface does the job.
- Do not build frameworks or domain specific languages with generics.
- Use the `slices`, `maps` and `cmp` packages from the standard library before writing your own helpers.

### Errors

#### Returning errors

Functions that can fail return an `error` as their last result.
Return `nil` for the error when the function succeeds, and do not return a typed `nil` pointer as an error.

```go
func Open(path string) (*File, error) {
    // …
}
```

Do not use in-band values such as `-1`, `""` or `nil` to signal errors.
Return an additional `error` or `bool` instead.

```go
// Good:
func Lookup(key string) (value string, ok bool)

// Bad: the caller cannot tell an empty value from a missing one.
func Lookup(key string) string
```

#### Handling errors

Handle every error.
Do not discard errors with `_`, unless the function is documented to never fail, and then explain it in a comment.

Handle the error first and return early, so that the normal code path stays at the left edge.
Do not use `else` after a block that returns.

```go
// Good:
f, err := os.Open(name)
if err != nil {
    return err
}
defer f.Close()
// Use f.

// Bad:
f, err := os.Open(name)
if err == nil {
    defer f.Close()
    // Use f.
} else {
    return err
}
```

Handle an error once.
Either log it or return it, but not both, as the caller would log it again.

#### Error strings

Error strings start with a lowercase letter and do not end with punctuation, since they are often wrapped in other messages.

```go
// Good:
err := fmt.Errorf("something bad happened")

// Bad:
err := fmt.Errorf("Something bad happened.")
```

#### Adding context

Wrap errors with context that helps the reader find the problem.
Do not add context that the error already contains, and do not start with "failed to", since every error is a failure.

```go
// Good:
if err := os.WriteFile(path, data, 0o644); err != nil {
    return fmt.Errorf("write config %q: %w", path, err)
}

// Bad:
if err := os.WriteFile(path, data, 0o644); err != nil {
    return fmt.Errorf("failed to write file: %v: %w", err, err)
}
```

Use `%w` when callers may need to inspect the original error, and `%v` when the original error is an implementation detail.

#### Inspecting errors

Use `errors.Is` and `errors.As` to inspect errors.
They also find errors that have been wrapped.
Never inspect the text of an error.

```go
if errors.Is(err, fs.ErrNotExist) {
    // …
}

var validationErr *ValidationError
if errors.As(err, &validationErr) {
    fmt.Println(validationErr.Field)
}
```

#### Panics

Do not use `panic` for normal error handling.
Return an error instead.

A panic is acceptable for errors that can only be caused by a bug in the program, such as an impossible state, and in `Must` functions that are only called during initialization.

```go
var validName = regexp.MustCompile(`^[a-z]+$`)
```

Only call `log.Fatal` and `os.Exit` from `main`.
They skip deferred functions and make code impossible to test.

### Control flow

#### If with initialization

Use the short form of `if` when a value is only needed for the condition and the block.

```go
if err := file.Chmod(0o664); err != nil {
    return err
}
```

#### Switch

Prefer a `switch` over a long chain of `if` and `else if`.
Cases do not fall through in Go, so `break` is not needed.
Avoid `fallthrough`.

```go
switch {
case n < 0:
    return "negative"
case n == 0:
    return "zero"
default:
    return "positive"
}
```

#### Loops

Use `range` to iterate over slices, maps, channels and, from Go 1.22, integers.

```go
for i := range 10 {
    fmt.Println(i)
}
```

From Go 1.22, each iteration of a loop has its own copy of the loop variable, so `v := v` inside a loop is no longer needed.

### Defer

Use `defer` to release a resource right after acquiring it, so the release is not forgotten on any return path.

```go
mu.Lock()
defer mu.Unlock()
```

Do not ignore the error from `Close` on files that were written to, as it may report that the data was not saved.

```go
func writeReport(path string, data []byte) (err error) {
    f, err := os.Create(path)
    if err != nil {
        return err
    }
    defer func() {
        if closeErr := f.Close(); err == nil {
            err = closeErr
        }
    }()
    _, err = f.Write(data)
    return err
}
```

Do not use `defer` inside a loop that acquires many resources, as nothing is released until the function returns.
Move the loop body into its own function instead.

### Strings

- Use `+` to join a few strings.
- Use `fmt.Sprintf` to format values into a string.
- Use `strings.Builder` to build a string piece by piece in a loop.
- Use raw string literals (`` ` ``) for regular expressions and text that contains quotes or backslashes.

### Type assertions

Use the two value form of a type assertion, which does not panic when the type is wrong.

```go
s, ok := value.(string)
if !ok {
    return errors.New("value is not a string")
}
```

### Package-level state

Avoid mutable package-level variables.
They make code hard to test and unsafe to use from several goroutines.
Pass dependencies explicitly, usually as fields of a struct.

Avoid `init` functions.
If one is needed, keep it simple, deterministic and free of I/O.

### Embedding

Embed types to reuse their methods.
Do not embed a type in an exported struct if its methods should not be part of the struct's API, and never embed a `sync.Mutex` in an exported struct, as `Lock` and `Unlock` become public.

```go
// Good:
type Cache struct {
    mu    sync.Mutex
    items map[string]string
}
```

### Random numbers

Use `crypto/rand` for keys, tokens and anything else that must not be guessable.
Use `math/rand/v2` for everything else.

## Concurrency

### Context

Functions that do I/O, take a long time or call other services take a `context.Context` as their first parameter, named `ctx`.

```go
func (c *Client) Fetch(ctx context.Context, url string) ([]byte, error)
```

- Do not store a context in a struct.
  Pass it to each method that needs it.
- Do not create custom context types or interfaces.
- Only use `context.Background()` in `main`, in tests and at the top of a request.

### Synchronous functions

Prefer synchronous functions, which return their result directly, over functions that start goroutines and return channels.
The caller can easily run a synchronous function in a goroutine, but cannot easily do the opposite.

### Goroutine lifetimes

When you start a goroutine, make it clear when and how it stops.
Goroutines that never stop leak memory and can block forever on channels.

Use `sync.WaitGroup` or `errgroup.Group` to wait for goroutines to finish, and a context to tell them to stop.

```go
func fetchAll(ctx context.Context, urls []string) error {
    g, ctx := errgroup.WithContext(ctx)
    for _, url := range urls {
        g.Go(func() error {
            return fetch(ctx, url)
        })
    }
    return g.Wait()
}
```

### Channels

- Specify the channel direction in function signatures (`<-chan T` or `chan<- T`).
- The sender closes a channel, never the receiver.
- Channels are unbuffered or have a buffer of one.
  Any other size needs a comment that explains why.

```go
func produce(ctx context.Context, out chan<- int) {
    defer close(out)
    for i := 0; ; i++ {
        select {
        case out <- i:
        case <-ctx.Done():
            return
        }
    }
}
```

### Mutexes

The zero value of `sync.Mutex` is ready to use, so do not initialize it.
Place the mutex directly above the fields it protects.

```go
type Counter struct {
    mu     sync.Mutex
    counts map[string]int
}

func (c *Counter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.counts[key]++
}
```

Run tests with the race detector (`go test -race`) to find data races.

## Comments and documentation

### Doc comments

Every exported name has a doc comment.
Doc comments are full sentences that start with the name they describe.

```go
// Server serves HTTP requests for the user API.
type Server struct {
    // …
}

// Start starts listening on the configured address.
// It returns an error if the address is already in use.
func (s *Server) Start() error {
    // …
}
```

Unexported names should also have a doc comment if their purpose is not obvious.

### Package comments

Every package has a package comment directly before the `package` clause, in only one file.
For large packages, put it in a file named `doc.go`.

```go
// Package user manages user accounts and their permissions.
package user
```

The package comment of a command describes what the program does and how to use it.

### Doc comment syntax

Doc comments support a small set of formatting, which `gofmt` normalizes:

- Paragraphs are separated by blank comment lines.
- Lines that start with `#` and a space are headings.
- Lines indented by an extra space or tab are code blocks.
- Lists start with `-` or a number.
- Names in square brackets, such as `[io.Reader]`, become links.

### Implementation comments

Comments inside functions explain why the code does something, not what it does.
The code already says what it does.

```go
// Good:
// The server returns stale results for up to a minute after a write,
// so read from the primary instead.
user, err := primary.User(ctx, id)

// Bad:
// Get the user from the primary.
user, err := primary.User(ctx, id)
```

### Named results

Name result parameters only when the names document the results, for example when a function returns several values of the same type.

```go
func (f *Foo) Location() (lat, lng float64, err error)
```

Do not use naked returns (a `return` without values) except in very short functions.

### Deprecation

Mark deprecated names with a paragraph that starts with `Deprecated:`, which tools recognize.

```go
// Load reads the configuration from disk.
//
// Deprecated: Use LoadContext instead.
func Load(path string) (*Config, error)
```

### TODO comments

Write `TODO` comments with the user name of the author or a link to an issue.

```go
// TODO(lrssn): Remove this once the API supports pagination.
// TODO(#42): Retry on temporary errors.
```

## Testing

### Test files and packages

Tests live next to the code in `_test.go` files.
Use the same package to test internal details, or the package name with a `_test` suffix to test only the exported API.

### Table-driven tests

Use table-driven tests when several cases share the same logic.
Name each case and run it as a subtest with `t.Run`.

```go
func TestParseDuration(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    time.Duration
        wantErr bool
    }{
        {name: "seconds", input: "5s", want: 5 * time.Second},
        {name: "minutes", input: "2m", want: 2 * time.Minute},
        {name: "empty", input: "", wantErr: true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseDuration(tt.input)
            if (err != nil) != tt.wantErr {
                t.Fatalf("ParseDuration(%q) error = %v, wantErr %v",
                    tt.input, err, tt.wantErr)
            }
            if got != tt.want {
                t.Errorf("ParseDuration(%q) = %v, want %v",
                    tt.input, got, tt.want)
            }
        })
    }
}
```

### Failure messages

Failure messages name the function, its input, the result and the expected result, in that order: `Func(input) = got, want want`.
A reader should understand the failure without reading the test code.

```go
if got != want {
    t.Errorf("Add(%d, %d) = %d, want %d", a, b, got, want)
}
```

Use `t.Errorf` so that the test continues and reports all failures.
Use `t.Fatalf` only when the rest of the test cannot run.

### Comparing values

Use [go-cmp](https://github.com/google/go-cmp) to compare structs, slices and maps, and print the difference.

```go
if diff := cmp.Diff(want, got); diff != "" {
    t.Errorf("LoadUser() mismatch (-want +got):\n%s", diff)
}
```

Do not use assertion libraries.
They hide the context of a failure and make every test look different.

### Test helpers

Test helpers call `t.Helper()`, so that failures are reported at the line that called the helper.
Use `t.Cleanup` to release resources and `t.TempDir` for temporary files.

```go
func newTestServer(t *testing.T) *Server {
    t.Helper()
    s, err := NewServer(Config{Addr: "localhost:0"})
    if err != nil {
        t.Fatalf("NewServer() = %v", err)
    }
    t.Cleanup(s.Stop)
    return s
}
```

### Examples

Write example functions (`ExampleFoo`) for important APIs.
They are shown in the documentation and checked by `go test`.

```go
func ExampleReverse() {
    fmt.Println(Reverse("hello"))
    // Output: olleh
}
```

## Tooling

### EditorConfig

Override the house indentation for Go files, which `gofmt` indents with tabs.

```ini
[{*.go,go.mod,go.work}]
indent_style = tab
indent_size = 4
```

### Formatting and imports

Format code and fix imports with [goimports](https://pkg.go.dev/golang.org/x/tools/cmd/goimports), which runs `gofmt` and also sorts the import blocks.
Pass the module path to `-local` so that the module's own packages get their own block.

```bash
goimports -local example.com/mymodule -w .
```

### Vet and lint

Run `go vet` on every change.
It finds real bugs, such as wrong format strings and copied mutexes.

```bash
go vet ./...
```

Use [golangci-lint](https://golangci-lint.run/) to run `go vet`, [staticcheck](https://staticcheck.dev/) and other linters together.
Add this `.golangci.yml` to the root of the repository:

```yaml
version: "2"
linters:
    default: standard
    enable:
        - errorlint
        - gocritic
        - misspell
        - revive
        - unconvert
        - unparam
formatters:
    enable:
        - gofmt
        - goimports
    settings:
        goimports:
            local-prefixes:
                - example.com/mymodule
```

```bash
golangci-lint run ./...
```

### Tests and vulnerabilities

Run the tests with the race detector, and check the dependencies for known vulnerabilities with [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck).

```bash
go test -race ./...
govulncheck ./...
```

### Modules

Keep `go.mod` and `go.sum` tidy and committed.

```bash
go mod tidy
```

## See also

- [Google Go style guide](https://google.github.io/styleguide/go/)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go code review comments](https://go.dev/wiki/CodeReviewComments)
- [Go doc comments](https://go.dev/doc/comment)
