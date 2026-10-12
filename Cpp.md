# C++ Style Guide

A style guide for C++, heavily based on the [Google C++ style guide](https://google.github.io/styleguide/cppguide.html).

Deviations from the Google guide:

- Code is indented by 4 spaces and continuation lines by 8 spaces, following the house rule in `.editorconfig`.
  Access specifiers are indented by 2 spaces.
- Exceptions are allowed for errors that the caller cannot handle locally.
  See [Exceptions](#exceptions).
- Braces are required for all control structures, even when the body is a single statement, as in the [Javascript style guide](./Javascript.md#braces).
- Function bodies never share a line with the signature, except when they are empty.

## Table of contents

[TOC]

## Goals

Most of the rules in this guide serve one of these goals:

- **Optimize for the reader, not the writer.**
  Code is read far more often than it is written.
- **Be consistent with existing code.**
  Consistency lets readers focus on what the code does instead of how it looks, and makes automated tools possible.
- **Avoid surprising or dangerous constructs.**
  C++ has features that are easy to misuse, and some are restricted here for that reason.
- **Avoid constructs that the average C++ programmer would find tricky.**
  Code that only experts understand is hard to maintain.

## C++ version

Code targets C++20.
Do not use non-standard compiler extensions.

Features from C++23, such as `std::expected` and `std::print`, may be used in projects that are built with C++23.

## Source files

### File names

File names are all lowercase, with underscores between words.

| Extension | Content |
| --- | --- |
| `.h` | Header files |
| `.cc` | Source files |
| `_test.cc` | Test files |

```text
user_service.h
user_service.cc
user_service_test.cc
```

Do not use file names that already exist in `/usr/include`, such as `db.h`.

### File encoding: UTF-8

Source files are encoded in UTF-8.
Use non-ASCII characters only where they are needed, such as in user-facing strings, and prefer escapes such as `é` in code that may be read by tools that do not handle UTF-8.

### Whitespace

Use spaces for indentation, never tabs.
Trailing whitespace is forbidden.

## Header files

In general, every `.cc` file has an associated `.h` file.
Exceptions are unit tests and small `.cc` files that only contain a `main()` function.

### Self-contained headers

Header files are self-contained: they compile on their own, without other headers being included first.
Each header includes everything it needs and has a header guard.

### The #define guard

All header files have `#define` guards to prevent multiple inclusion.
The name of the symbol is `<PROJECT>_<PATH>_<FILE>_H_`, based on the full path in the project's source tree.

```cpp
// The file lrssn/storage/user_store.h:
#ifndef LRSSN_STORAGE_USER_STORE_H_
#define LRSSN_STORAGE_USER_STORE_H_

// …

#endif  // LRSSN_STORAGE_USER_STORE_H_
```

### Include what you use

If a file uses a symbol that is defined somewhere else, it includes the header that declares it.
Do not rely on headers that are included indirectly by other headers.

### Forward declarations

Avoid forward declarations.
Include the header that declares the type instead.
Forward declarations hide dependencies and can break when the library changes.

### Inline functions

Only define functions in a header when they are short, about 10 lines or fewer.
Longer functions belong in the `.cc` file.

### Names and order of includes

Include headers in this order, with a blank line between each group:

1. The header that the `.cc` file implements.
1. C system headers, such as `<unistd.h>`.
1. C++ standard library headers, such as `<string>`.
1. Headers of other libraries.
1. Headers of the project.

Within each group, sort the includes alphabetically.
Use angle brackets for system and library headers, and quotes for the project's own headers.
Project headers are written as paths from the root of the source tree, without `.` or `..`.

```cpp
#include "lrssn/server/user_service.h"

#include <sys/types.h>
#include <unistd.h>

#include <string>
#include <vector>

#include "absl/strings/str_cat.h"
#include "lrssn/base/logging.h"
#include "lrssn/storage/user_store.h"
```

## Scoping

### Namespaces

Place all code in a namespace, except for `main()`.
Namespaces have unique names based on the project name, and possibly the path.

```cpp
namespace lrssn::storage {

class UserStore {
    // …
};

}  // namespace lrssn::storage
```

- Do not indent the contents of a namespace.
- End each namespace with a comment that names it.
- Do not use `using namespace`, such as `using namespace std;`.
  It pulls every name of the namespace into the current scope.
- Do not use inline namespaces.
- Do not declare anything in namespace `std`.

`using` declarations of single names are allowed in `.cc` files, and inside functions and classes in headers.

```cpp
// In a .cc file:
using ::lrssn::storage::UserStore;
```

### Internal linkage

Functions and variables in a `.cc` file that are not used anywhere else have internal linkage.
Put them in an unnamed namespace.
Do not use internal linkage in header files.

```cpp
namespace lrssn {
namespace {

constexpr int kMaxAttempts = 3;

bool IsValidName(std::string_view name) {
    return !name.empty() && name.size() < 64;
}

}  // namespace
}  // namespace lrssn
```

### Nonmember functions

Prefer functions in a namespace over static member functions that do not use the class.
Do not create classes only to group static functions.

### Local variables

Declare local variables in the narrowest scope possible, as close to their first use as possible, and initialize them in the declaration.

```cpp
// Good:
int i = f();
std::vector<int> v = {1, 2};

// Bad:
int j;
j = g();
```

Variables needed by `if`, `while` and `for` statements are declared inside those statements, so that they are limited to that scope.

```cpp
while (const char* p = strchr(str, '/')) {
    str = p + 1;
}
```

### Static and global variables

Objects with static storage duration are forbidden unless they are trivially destructible.
Their constructors and destructors run in an unspecified order, which causes hard to find bugs.

Global and static variables should be `constexpr` or `constinit` where possible.

```cpp
// Good:
constexpr std::string_view kDefaultName = "guest";
constexpr int kMaxUsers = 100;
constexpr std::array<int, 3> kPorts = {80, 443, 8080};

// Bad: std::string and std::map have non-trivial destructors.
const std::string kDefaultName = "guest";
const std::map<int, std::string> kNames = {{1, "one"}};
```

If a non-trivial global object is needed, create it once in a function and never destroy it.

```cpp
const std::map<int, std::string>& Names() {
    static const auto* names =
            new std::map<int, std::string>({{1, "one"}, {2, "two"}});
    return *names;
}
```

### thread_local variables

`thread_local` variables inside functions are allowed.
`thread_local` variables at namespace or class scope must be initialized with a compile-time constant, using `constinit`.

## Classes

### Doing work in constructors

Constructors must not call virtual functions, which do not dispatch to the subclass during construction.

A constructor that can fail either throws an exception, or the class provides a factory function that returns `std::optional` or a pointer instead, and the constructor is made private.

```cpp
class Config {
  public:
    // Returns nullopt if the file cannot be parsed.
    static std::optional<Config> Load(std::string_view path);

  private:
    explicit Config(std::map<std::string, std::string> values);
};
```

### Implicit conversions

Mark constructors that can be called with one argument, and conversion operators, as `explicit`.
Implicit conversions can hide bugs and make overload resolution confusing.

```cpp
class Foo {
  public:
    explicit Foo(int x);
    explicit operator bool() const;
};
```

Copy and move constructors are not marked `explicit`.
Constructors that take a single `std::initializer_list` may be implicit, to allow copy-initialization such as `MyType m = {1, 2};`.

### Copyable and movable types

Make it clear whether a class is copyable, move-only or neither, by declaring or deleting the copy and move operations in the public section.

```cpp
class Copyable {
  public:
    Copyable(const Copyable& other) = default;
    Copyable& operator=(const Copyable& other) = default;
};

class MoveOnly {
  public:
    MoveOnly(MoveOnly&& other) = default;
    MoveOnly& operator=(MoveOnly&& other) = default;
};

class NotCopyableOrMovable {
  public:
    NotCopyableOrMovable(const NotCopyableOrMovable&) = delete;
    NotCopyableOrMovable& operator=(const NotCopyableOrMovable&) = delete;
};
```

Prefer the rule of zero: if the members of a class manage their own resources, such as `std::string` and `std::unique_ptr`, the class needs none of these declarations.
If a class declares any of the destructor, copy operations or move operations, declare all five.

### Structs versus classes

Use a `struct` only for passive objects that carry data, with all fields public and no invariants between them.
Use a `class` for everything else.

```cpp
struct Point {
    double x = 0.0;
    double y = 0.0;
};
```

Prefer a struct with named fields over `std::pair` and `std::tuple`.
`point.x` says more than `pair.first`.

### Inheritance

Prefer composition over inheritance.
When using inheritance, make it `public`.

- Mark overriding functions with `override`, `final`, or both, and do not repeat `virtual` on them.
- Classes that are meant to be used through a base class pointer have a `virtual` destructor.
- Avoid multiple implementation inheritance.
  Inheriting from several pure interfaces is fine.

```cpp
class Shape {
  public:
    virtual ~Shape() = default;
    virtual double Area() const = 0;
};

class Circle : public Shape {
  public:
    explicit Circle(double radius) : radius_(radius) {}

    double Area() const override {
        return std::numbers::pi * radius_ * radius_;
    }

  private:
    double radius_;
};
```

### Operator overloading

Only overload operators when their meaning is obvious and consistent with the built-in operators.
For example, `+` adds, and `==` compares for equality.

- Define binary operators as non-member functions, so that both operands are treated the same.
- Use defaulted comparison operators where possible.
- Do not overload `&&`, `||`, `,` or unary `&`.
- Do not use user-defined literals.

```cpp
struct Version {
    int major = 0;
    int minor = 0;
    int patch = 0;

    friend auto operator<=>(const Version&, const Version&) = default;
};
```

### Access control

Make data members of classes `private`, unless they are constants.
Provide accessor functions where other code needs the data.

### Declaration order

Group the members of a class in the order `public`, `protected` and `private`, and leave out sections that are empty.

Within each section, declare the members in this order:

1. Types and type aliases.
1. Static constants.
1. Factory functions.
1. Constructors and assignment operators.
1. The destructor.
1. All other functions.
1. Data members.

## Functions

### Inputs and outputs

Prefer return values over output parameters.
Return by value, and rely on the compiler to avoid the copy.

```cpp
// Good:
std::vector<User> FindUsers(std::string_view query);

// Bad:
void FindUsers(std::string_view query, std::vector<User>* result);
```

- Pass inputs by value when they are cheap to copy, such as integers, `std::string_view` and `std::span`.
- Pass other inputs by `const` reference.
- Use `std::optional` for optional inputs that are passed by value, and a `const` pointer for optional inputs that would otherwise be passed by reference.
- When an output parameter is unavoidable, use a reference if it is required and a pointer if it is optional.
- Put all input parameters before any output parameters.

### Write short functions

Prefer small, focused functions.
If a function is longer than about 40 lines, consider whether it can be split up without harming the structure of the program.

### Function overloading

Only overload a function when a reader at the call site does not need to know which overload is called.
If the overloads do different things, give them different names.

### Default arguments

Default arguments are allowed on non-virtual functions when the default is always the same value.
Do not use default arguments on virtual functions, as the default depends on the static type of the object.

### Trailing return types

Only use trailing return types where they are required, such as for lambdas, or where they make the declaration much easier to read.

## Ownership and smart pointers

Every dynamically allocated object has a single, clear owner.

- Use `std::unique_ptr` for exclusive ownership, and `std::move` to transfer it.
- Create objects with `std::make_unique` and `std::make_shared`.
- Use `std::shared_ptr` only when ownership is really shared, and prefer sharing immutable objects (`std::shared_ptr<const T>`).
- Raw pointers and references never own the object they point to.
- Never use `new` and `delete` directly, except in the never-destroyed globals described in [Static and global variables](#static-and-global-variables).

```cpp
std::unique_ptr<Storage> CreateStorage(const Config& config);

class UserService {
  public:
    explicit UserService(std::unique_ptr<Storage> storage)
            : storage_(std::move(storage)) {}

  private:
    std::unique_ptr<Storage> storage_;
};
```

## Other C++ features

### Rvalue references

Use rvalue references only to define move constructors and move assignment operators, for forwarding references with `std::forward`, and for overloads that need to handle temporaries for performance.

### Friends

Friend classes and functions are allowed, but should be declared in the same file as the class, so that the reader does not have to look elsewhere.
A common use is a test class or a builder class.

### Exceptions

Exceptions may be used, which is a deviation from the Google guide.
This guide allows exceptions so that an error the caller cannot handle locally can travel up to code that can, without a status check at every level.

- Throw an exception for errors that the caller cannot handle locally, such as a broken invariant or a failed resource that the program depends on.
- Return `std::optional`, or `std::expected` in C++23, for failures that are part of normal operation, such as a lookup that finds nothing or input that does not parse.
- Throw types derived from `std::exception`, usually `std::runtime_error`, `std::invalid_argument` or your own subclasses.
- Throw by value and catch by `const` reference.
- Never let an exception leave a destructor.
- Do not use exceptions for normal control flow.
- Catch all exceptions at boundaries that cannot pass them on, such as callbacks from C code, thread entry functions and `main`.

```cpp
class ParseError : public std::runtime_error {
  public:
    using std::runtime_error::runtime_error;
};

Config ParseConfig(std::string_view text) {
    if (text.empty()) {
        throw ParseError("Configuration is empty");
    }
    // …
}

int main() {
    try {
        Run();
    } catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << '\n';
        return 1;
    }
    return 0;
}
```

### noexcept

Mark functions `noexcept` when they cannot throw and it is useful, especially move constructors and move assignment operators.
When `std::vector` grows, it moves its elements only if their move constructor is `noexcept`, and copies them otherwise, if they can be copied.

### Run-time type information

Avoid `typeid` and `dynamic_cast`.
Needing to know the type of an object at runtime is usually a sign that the class hierarchy should be changed, for example by adding a virtual function.
They may be used in tests.

### Casting

Use C++ casts, never C-style casts such as `(int)x`.

| Cast | Use for |
| --- | --- |
| `static_cast` | Value conversions and explicit up-casts |
| `const_cast` | Removing `const`, which is rarely needed |
| `reinterpret_cast` | Unsafe pointer conversions, only when unavoidable |
| `std::bit_cast` | Reinterpreting the bits of a value as another type |

Use brace initialization for conversions between arithmetic types that cannot lose information, such as `int64_t{x}`.
It does not compile if the conversion would narrow the value.

```cpp
int64_t value = int64_t{1} << 42;
double ratio = static_cast<double>(count) / total;
```

### Streams and formatting

Use streams for reading and writing files and the console.
Use `std::format` to build strings from values, instead of `sprintf` or long chains of `<<`.

```cpp
std::string message = std::format("User {} has {} items", name, count);
```

### Preincrement and predecrement

Use the prefix form (`++i`) of the increment and decrement operators, unless the postfix value is needed.

### Use of const

Use `const` wherever it makes sense.
Mark member functions that do not change the object as `const`, and pass inputs by `const` reference.

Put `const` before the type: `const int* p`, not `int const* p`.

### Use of constexpr, constinit and consteval

Use `constexpr` for constants and for functions that can be evaluated at compile time.
Use `constinit` for non-constant global variables that must be initialized at compile time.
Use `consteval` only for functions that must run at compile time.

```cpp
constexpr int Square(int x) {
    return x * x;
}

constexpr int kArea = Square(5);
```

### Integer types

Use `int` for integers that are known to be small, such as loop counters.
Use the fixed-size types from `<cstdint>`, such as `int32_t` and `int64_t`, when the size matters.
Do not use `short`, `long` or `long long`.

Do not use unsigned types to say that a value is never negative.
Mixing signed and unsigned values causes subtle bugs.
Use unsigned types only for bit patterns and for modular arithmetic.

### Preprocessor macros

Avoid macros.
Use inline functions, `constexpr` variables, enums and templates instead.

If a macro is unavoidable:

- Give it a long name with the project prefix, such as `LRSSN_CHECK`.
- Do not define macros in headers unless they are part of the API.
- `#undef` macros that are only used in one `.cc` file after their last use.

### nullptr

Use `nullptr` for pointers, never `0` or `NULL`.
Use `'\0'` for the null character.

### sizeof

Prefer `sizeof(variable)` over `sizeof(type)`.
It stays correct when the type of the variable changes.

```cpp
MyStruct data;
std::memset(&data, 0, sizeof(data));
```

### Type deduction with auto

Use `auto` when it makes the code clearer, such as when the type is already written on the same line or is an iterator.
Do not use `auto` only to avoid writing a type that the reader needs to know.

```cpp
// Good:
auto widget = std::make_unique<Widget>(arg1, arg2);
auto it = users.find(id);

// Bad: the reader has to look up what Compute returns.
auto result = Compute();
```

In range-based `for` loops, use `const auto&` to avoid copies, or `auto&` to change the elements.

```cpp
for (const auto& [name, user] : users_by_name) {
    Print(name, user);
}
```

### Designated initializers

Designated initializers may be used, in the order that the fields are declared.

```cpp
Point point = {.x = 1.0, .y = 2.0};
```

### Lambda expressions

Use lambdas where they make the code clearer, such as for short callbacks to standard algorithms.

- Use explicit captures when the lambda may outlive the current scope.
- Default capture by reference (`[&]`) is only allowed when the lambda does not outlive the current scope.
- Do not use default capture by value (`[=]`), as it captures `this` implicitly.
- Keep lambdas short.
  Give longer logic a name as a function.

```cpp
// Good: the lambda does not outlive the scope.
auto it = std::find_if(users.begin(), users.end(), [&](const User& user) {
    return user.name() == name;
});

// Good: the callback runs later, so the capture is explicit.
executor->Schedule([request_id, this]() { Complete(request_id); });
```

### Templates and concepts

Avoid complicated template metaprogramming.
It is hard to read and gives poor error messages.

Use concepts and `requires` clauses to constrain templates, instead of `std::enable_if` and other SFINAE techniques.

```cpp
template <typename T>
    requires std::integral<T>
T Gcd(T a, T b) {
    while (b != 0) {
        a = std::exchange(b, a % b);
    }
    return a;
}
```

### Aliases

Use `using` to declare type aliases, never `typedef`.
Do not add aliases to a public header only to save typing, since they become part of the API.

```cpp
using UserMap = std::map<std::string, User>;
```

### Switch statements

`switch` statements on an enum handle every value, and have no `default` case, so that the compiler warns when a new value is added.
Other `switch` statements have a `default` case.

Fall-through between non-empty cases is marked with `[[fallthrough]];`.

```cpp
switch (color) {
    case Color::kRed:
        Paint();
        break;
    case Color::kGreen:
        Prepare();
        [[fallthrough]];
    case Color::kBlue:
        Finish();
        break;
}
```

## Naming

### General naming rules

Use names that describe the purpose of the thing they name.
Do not use abbreviations that are ambiguous or unfamiliar to readers outside your project, and do not abbreviate by deleting letters within a word.

```cpp
// Good:
int price_count_reader;
int num_errors;
int num_dns_connections;

// Bad:
int n;
int nerr;
int pc_reader;
int cstmr_id;
```

The length of a name should match the size of its scope.
A loop index used in three lines can be `i`.

### Type names

Type names use `PascalCase`.
This applies to classes, structs, type aliases, enums, type template parameters and concepts.

```cpp
class UrlTable {};
struct UrlTableProperties {};
using PropertiesMap = std::map<std::string, UrlTableProperties>;
enum class UrlTableError {};
```

### Variable names

Variable names, including function parameters, use `snake_case`.
Data members of classes, but not structs, have a trailing underscore.

```cpp
std::string table_name;

class TableInfo {
  private:
    std::string table_name_;
    static int pool_size_;
};

struct UrlTableProperties {
    std::string name;
    int num_entries;
};
```

### Constant names

Variables declared `constexpr` whose value is fixed for the duration of the program are named with a leading `k` followed by `PascalCase`.

```cpp
constexpr int kDaysInAWeek = 7;
const int kAndroid8_0_0 = 24;  // Android 8.0.0
```

### Function names

Functions use `PascalCase`, including accessors and mutators: `Count()` returns the count, and `SetCount()` changes it.

```cpp
void AddTableEntry();
bool DeleteUrl();

class Counter {
  public:
    int Count() const {
        return count_;
    }
    void SetCount(int count) {
        count_ = count;
    }

  private:
    int count_ = 0;
};
```

### Namespace names

Namespace names use `snake_case`.
The top-level namespace is based on the name of the project.

### Enumerator names

Use scoped enums (`enum class`), and name the enumerators like constants.

```cpp
enum class UrlTableError {
    kOk = 0,
    kOutOfMemory,
    kMalformedInput,
};
```

### Template parameter names

Type template parameters are named like types.
Non-type template parameters are named like variables or constants.

```cpp
template <typename ValueType, int kSize>
class FixedBuffer {};
```

### Macro names

Macros are named in `UPPER_SNAKE_CASE`, with the project prefix.

```cpp
#define LRSSN_ROUND(x) ...
```

## Comments

### Comment style

Use `//` for comments.
`/* */` may be used for comments inside a line, such as argument comments.

### File comments

Start each file with the license, if the project has one.
If a header declares several things that are not obviously related, describe the content of the file after the license.

### Class comments

Every non-obvious class or struct has a comment that describes what it is for and how to use it.
Mention any thread safety guarantees or limitations.

```cpp
// Iterates over the contents of a GargantuanTable.
// Example:
//     std::unique_ptr<GargantuanTableIterator> iter = table->NewIterator();
//     for (iter->Seek("foo"); !iter->done(); iter->Next()) {
//         process(iter->key(), iter->value());
//     }
// This class is not thread-safe.
class GargantuanTableIterator {
    // …
};
```

### Function comments

Comments on a function declaration describe what the function does and how to use it.
They are written in the indicative mood ("Opens the file") rather than the imperative ("Open the file").
Mention:

- What the inputs and outputs are.
- Whether the function keeps references or pointers to its arguments after it returns.
- Whether it allocates memory that the caller must free.
- Whether any argument can be null.
- What it throws, and when.
- Any performance implications.

```cpp
// Returns an iterator for this table, positioned at the first entry
// lexically greater than or equal to `start_word`. The client must not use
// the iterator after the table has been destroyed.
std::unique_ptr<Iterator> GetIterator(std::string_view start_word) const;
```

Comments on a function definition explain how the function works, if that is not obvious.

### Variable comments

Comment class data members whose purpose is not clear from the name and type, including special values.

```cpp
class Table {
  private:
    // Used to bounds-check table accesses. -1 means that we don't yet know
    // how many entries the table has.
    int num_total_entries_;
};
```

### Implementation comments

Comment tricky, non-obvious, interesting or important parts of the code.
Explain why the code does something, not what it does.

When the meaning of a literal argument is not obvious, add an argument comment with the parameter name.
Prefer named constants or enums over literal `bool` arguments where possible.

```cpp
const DecimalNumber product = CalculateProduct(values, /*precision=*/7);
```

### TODO comments

Write `TODO` comments with a link to an issue, such as `TODO(#42)`. If no issue exists yet, open one first.

```cpp
// TODO(#41): Use a heap instead of sorting the whole list.
// TODO(#42): Handle IPv6 addresses.
```

### Deprecation

Mark deprecated interfaces with the `[[deprecated]]` attribute, and say what to use instead.

```cpp
[[deprecated("Use LoadUser instead.")]]
User GetUser(std::string_view id);
```

## Formatting

Do not format code by hand.
Use the clang-format configuration in [Tooling](#tooling), and let the formatter decide.
The rules below describe what the formatter produces.

### Line length

Each line of code is at most 80 characters long.

The exceptions are comments with a URL or a command that cannot be split, string literals that would be hard to search for if split, `#include` statements and header guards.

### Indentation

Indent blocks by 4 spaces and continuation lines by 8 spaces.

### Function declarations and definitions

Put the return type on the same line as the function name, and the parameters on the same line if they fit.
If they do not fit, break after the opening parenthesis and indent the parameters by 8 spaces.

```cpp
ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
    DoSomething();
}

ReturnType ClassName::ReallyLongFunctionName(
        Type par_name1, Type par_name2, Type par_name3, Type par_name4) {
    DoSomething();
}
```

The opening brace is at the end of the last line of the declaration, never on a line of its own.
The body starts on a new line, unless it is empty.

Unused parameters that are obvious from context may be left unnamed.
Otherwise, comment out their names or mark them `[[maybe_unused]]`.

```cpp
void Circle::Rotate(double /*radians*/) {}
```

### Lambda expressions

Format lambda bodies like function bodies.
Short lambdas may be written on one line.

```cpp
std::set<int> to_remove = {7, 8, 9};
std::vector<int> digits = {3, 9, 1, 8, 4, 7, 1};
digits.erase(
        std::remove_if(
                digits.begin(), digits.end(),
                [&to_remove](int i) { return to_remove.contains(i); }),
        digits.end());
```

### Floating-point literals

Floating-point literals always have digits on both sides of the decimal point.

```cpp
// Good:
float f = 1.0f;
double d = 1248.0e6;

// Bad:
float f = 1.f;
double d = 1248e6;
```

### Function calls

Write the call on one line if it fits.
Otherwise, break after the opening parenthesis and indent the arguments by 8 spaces.

```cpp
bool result = DoSomething(
        averyveryveryverylongargument1, argument2, argument3, argument4);
```

If an argument is a complex expression, consider giving it a name with a local variable.

### Braced initializer lists

Format braced initializer lists like function calls.

```cpp
std::vector<std::string> names = {"Alice", "Bob", "Carol"};

SomeType variable{
        some_other_value_that_is_long, another_value_that_is_also_long,
        and_a_third_value};
```

### Conditionals and loops

- Put a space between the keyword and the opening parenthesis, and none inside the parentheses.
- Always use braces, even for a single statement.
- `else` goes on the same line as the closing brace before it.

```cpp
if (condition) {
    DoOneThing();
} else if (other_condition) {
    DoAnotherThing();
} else {
    DoNothing();
}

for (int i = 0; i < kSomeNumber; ++i) {
    Process(i);
}

while (condition) {
    Wait();
}
```

Empty loop bodies have braces and a comment that explains why the body is empty, never a single semicolon.

```cpp
while (condition) {
    // Repeat the test until it returns false.
}
```

### Switch statement format

Indent the cases by 4 spaces, and the statements of each case by another 4 spaces.
A case that needs its own scope wraps its statements in braces.

```cpp
switch (var) {
    case 0: {
        int value = Compute();
        Use(value);
        break;
    }
    default: {
        Fail();
    }
}
```

### Pointers and references

Attach the `*` and `&` to the type, not to the variable name.
There are no spaces around `.` and `->`, or after a unary `*` and `&`.

```cpp
char* c;
const std::string& str;
int* GetPointer();
std::vector<char*> pointers;

x = *p;
p = &x;
x = r.y;
x = r->y;
```

Do not declare more than one variable in a declaration that uses `*` or `&`.

### Boolean expressions

When a boolean expression does not fit on one line, break after an operator.
The formatter aligns the continuation of a condition with the opening parenthesis.

```cpp
if (this_one_thing > this_other_thing && a_third_thing == a_fourth_thing &&
    yet_another && last_one) {
    DoSomething();
}
```

As the continuation then lines up with the body, prefer moving parts of a long condition into well-named variables.

```cpp
const bool things_match = this_one_thing > this_other_thing &&
                          a_third_thing == a_fourth_thing;
if (things_match && yet_another && last_one) {
    DoSomething();
}
```

Use parentheses to make the grouping clear when `&&` and `||` are mixed.

### Return values

Do not put parentheses around the return value.

```cpp
// Good:
return result;
return (some_long_condition && another_condition);

// Bad:
return (value);
```

The parentheses in the second example are fine, as they group a complex expression.

### Variable initialization

Use `=`, `()` or `{}` to initialize variables, whichever is clearest.
Be careful with `{}` on types that have a constructor taking a `std::initializer_list`.

```cpp
int x = 3;
std::string name = "Some Name";

std::vector<int> v(100, 1);  // A vector of 100 ones.
std::vector<int> w{100, 1};  // A vector with the elements 100 and 1.
```

### Preprocessor directives

Preprocessor directives always start at the beginning of the line, even inside indented code.

```cpp
if (lopsided_score) {
#if DISASTER_PENDING
    DropEverything();
#endif
    BackToNormal();
}
```

### Class format

Access specifiers are indented by 2 spaces, and members by 4.
A blank line separates each access section, except the first.

```cpp
class MyClass : public OtherClass {
  public:
    MyClass();
    explicit MyClass(int var);
    ~MyClass() {}

    void SomeFunction();
    void SomeFunctionThatDoesNothing() {}

    void set_some_var(int var) {
        some_var_ = var;
    }
    int some_var() const {
        return some_var_;
    }

  private:
    bool SomeInternalFunction();

    int some_var_;
    int some_other_var_;
};
```

### Constructor initializer lists

Keep the initializer list on the same line as the signature if it fits.
Otherwise, break before the colon, indent by 8 spaces, and put each initializer on its own line.

```cpp
MyClass::MyClass(int var) : some_var_(var) {
    DoSomething();
}

MyClass::MyClass(int var)
        : some_var_(var),
          some_other_var_(var + 1),
          yet_another_var_(var * 2) {
    DoSomething();
}
```

### Namespace formatting

The contents of namespaces are not indented.

```cpp
namespace lrssn {

void Foo() {
    Bar();
}

}  // namespace lrssn
```

### Horizontal whitespace

- Put one space on each side of binary and assignment operators.
- Do not put spaces inside parentheses or angle brackets.
- Put two spaces before an end-of-line comment.
- Trailing whitespace is forbidden.

```cpp
int x = (a + b) * c;
std::vector<std::string> names;
DoSomething();  // A comment.
```

### Vertical whitespace

Use blank lines sparingly to separate logical groups of code.
Do not start or end a block with a blank line, and do not use more than one blank line in a row.

## Tooling

### Formatter

Format code with [clang-format](https://clang.llvm.org/docs/ClangFormat.html).
Add this `.clang-format` to the root of the repository:

```yaml
---
Language: Cpp
BasedOnStyle: Google
IndentWidth: 4
ContinuationIndentWidth: 8
ConstructorInitializerIndentWidth: 8
AccessModifierOffset: -2
ColumnLimit: 80
AlignAfterOpenBracket: AlwaysBreak
DerivePointerAlignment: false
PointerAlignment: Left
AllowShortFunctionsOnASingleLine: Empty
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
InsertBraces: true
PackConstructorInitializers: CurrentLine
```

```bash
clang-format -i src/*.cc src/*.h
```

### Linter

Use [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) to find bugs and enforce the naming rules.
Add this `.clang-tidy` to the root of the repository:

```yaml
---
Checks: >
    bugprone-*,
    cppcoreguidelines-*,
    google-*,
    misc-*,
    modernize-*,
    performance-*,
    readability-*,
    -cppcoreguidelines-avoid-magic-numbers,
    -modernize-use-trailing-return-type,
    -readability-magic-numbers
WarningsAsErrors: "*"
CheckOptions:
    readability-identifier-naming.ClassCase: CamelCase
    readability-identifier-naming.StructCase: CamelCase
    readability-identifier-naming.EnumCase: CamelCase
    readability-identifier-naming.EnumConstantCase: CamelCase
    readability-identifier-naming.EnumConstantPrefix: k
    readability-identifier-naming.FunctionCase: CamelCase
    readability-identifier-naming.NamespaceCase: lower_case
    readability-identifier-naming.VariableCase: lower_case
    readability-identifier-naming.ParameterCase: lower_case
    readability-identifier-naming.PrivateMemberSuffix: _
    readability-identifier-naming.ProtectedMemberSuffix: _
    readability-identifier-naming.ConstexprVariableCase: CamelCase
    readability-identifier-naming.ConstexprVariablePrefix: k
    readability-identifier-naming.MacroDefinitionCase: UPPER_CASE
```

clang-tidy needs to know how the code is compiled, which it reads from a `compile_commands.json` file.
CMake writes this file when `CMAKE_EXPORT_COMPILE_COMMANDS` is on.

```bash
clang-tidy -p build src/*.cc
```

### Compiler warnings

Build with all warnings enabled, and treat warnings as errors.

| Compiler | Flags |
| --- | --- |
| GCC and Clang | `-Wall -Wextra -Wpedantic -Werror` |
| MSVC | `/W4 /WX /permissive-` |

Run the tests with the address and undefined behavior sanitizers (`-fsanitize=address,undefined`) to find memory errors.

### Build system

Use [CMake](https://cmake.org/) to build projects, and set the standard for the whole project.

```cmake
cmake_minimum_required(VERSION 3.25)
project(lrssn_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_library(user_service src/user_service.cc)
if(MSVC)
    target_compile_options(user_service PRIVATE /W4 /WX /permissive-)
else()
    target_compile_options(
        user_service PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()
```

### Testing

Write tests with [GoogleTest](https://github.com/google/googletest).
Test suites and test names use `PascalCase`, and each test checks one behavior.

```cpp
TEST(UserServiceTest, ReturnsCachedUser) {
    UserService service(std::make_unique<FakeStorage>());
    EXPECT_EQ(service.LoadUser("1")->name(), "Alice");
}
```

## See also

- [Google C++ style guide](https://google.github.io/styleguide/cppguide.html)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [cppreference](https://en.cppreference.com/)
