# Ruby Style Guide

A style guide for Ruby.
It is based on the community [Ruby Style Guide](https://rubystyle.guide/) and the rules of [RuboCop](https://rubocop.org/).

Deviations from the community style guide:

- Lines are at most 80 characters long instead of 120, following the house rule in `.editorconfig`.
- Indentation is 4 spaces instead of 2, following the house rule in `.editorconfig`.
- Strings use single quotes unless they need interpolation or escape sequences, which matches the other guides in this repository.
- Multi-line literals and argument lists end with a trailing comma.

## Table of contents

[TOC]

## Ruby version and tooling

New projects use a supported Ruby release.
Pin the version in a `.ruby-version` file, and declare it in the `Gemfile`, so that everyone and the continuous integration use the same interpreter.

```ruby
# frozen_string_literal: true

source 'https://rubygems.org'

ruby '~> 3.3'

gem 'rake'

group :development do
    gem 'rspec'
    gem 'rubocop', require: false
end
```

Manage gems with [Bundler](https://bundler.io/), and commit `Gemfile.lock` for applications.
Do not commit it for gems, which must work with a range of dependency versions.

## Source files

### File names

Name files in `snake_case` after the class or module they define, with one top-level class or module per file.
The class `UserStore` lives in `user_store.rb`, and the module `Billing::Invoice` lives in `billing/invoice.rb`.

### File encoding: UTF-8

Source files are encoded in UTF-8.
Avoid non-ASCII characters in identifiers.

### Project layout

```text
style-check/
├── bin/
│   └── style-check
├── lib/
│   ├── style_check/
│   │   └── user.rb
│   └── style_check.rb
├── spec/
│   ├── style_check/
│   │   └── user_spec.rb
│   └── spec_helper.rb
├── Gemfile
├── Rakefile
└── style-check.gemspec
```

The files in `lib` are named after the gem, with hyphens in the gem name turned into underscores.

## Source file structure

A source file consists of the following parts, in this order, separated by one blank line:

1. The shebang line, for executable scripts only.
2. The `# frozen_string_literal: true` magic comment.
3. `require` statements.
4. The class or module definition.

### Frozen string literals

Start every file with the `frozen_string_literal` magic comment, so that string literals are immutable.

```ruby
# frozen_string_literal: true
```

Use `+''` or `String.new` to get a mutable string, and `dup` to copy a frozen one.

### Requires

Group `require` statements at the top of the file, with the standard library first, then gems, and then the files of the project.
Use `require_relative` for files of the same project.

```ruby
require 'json'
require 'time'

require 'faraday'

require_relative 'user'
```

## Formatting

Do not format code by hand.
Use RuboCop with the configuration in [Tooling](#tooling), and let it decide.
The rules below describe what the formatter produces.

### Indentation and line length

Indent by 4 spaces, never tabs.
Lines are at most 80 characters long.

When the arguments of a method call, the elements of an array or the pairs of a hash do not fit on one line, put each on its own line, indented by 4 spaces, with a trailing comma and the closing delimiter on a line of its own.

```ruby
user = User.new(
    name: 'Ada Lovelace',
    email: 'ada@example.com',
    roles: %i[reader writer],
)
```

### Blank lines

Separate method definitions with a single blank line.
Do not start or end a body with a blank line.
Do not put a blank line after a line that opens a block, such as `class User` or `def name`.

### Whitespace

Put a space around operators, after commas and after colons in hashes, but not inside parentheses or brackets.
Put a space inside the braces of a block and of a hash literal.

```ruby
total = prices.sum { |price| price * 2 }
config = { name: 'style-check', verbose: true }
```

### Method calls

Use parentheses for method calls with arguments, and omit them for methods without arguments.
Omit the parentheses only for keywords such as `puts`, `raise`, `require`, and DSL methods such as those of RSpec and Rake.

```ruby
# Good
user.rename('Ada')
puts user.name

# Bad
user.rename 'Ada'
puts(user.name())
```

### Chained calls

When a chain does not fit on one line, put each call on its own line, starting with the dot, and indent it by 4 spaces.

```ruby
names = users
    .select(&:active?)
    .map(&:name)
    .sort
```

### Conditionals

Use the modifier form of `if` and `unless` only when the whole statement fits on one line.
Do not use `unless` with an `else` branch, or with a complex condition.
Do not use the ternary operator when the expression spans several lines, and never nest ternaries.

```ruby
# Good
return if items.empty?

status = admin? ? 'admin' : 'user'

# Bad
unless user.admin?
    deny
else
    allow
end
```

Use `&&`, `||` and `!` in conditions, and `and`, `or` and `not` never.

### Comments

Write comments as full sentences, with a space after the `#`.
Put a comment on the line above the code it describes.
Do not use block comments (`=begin` and `=end`).

## Naming

### Rules by item type

| Item | Case | Example |
| --- | --- | --- |
| Class, module | `UpperCamelCase` | `UserStore` |
| Method, variable, argument | `snake_case` | `parse_duration` |
| Constant | `SCREAMING_SNAKE_CASE` | `MAX_RETRIES` |
| Symbol | `snake_case` | `:read_only` |
| File, directory | `snake_case` | `user_store.rb` |
| Predicate method | `snake_case` ending in `?` | `admin?` |
| Dangerous method | `snake_case` ending in `!` | `save!` |

### Acronyms

Treat an acronym like any other word in class names: only the first letter is uppercase.
Write `HttpClient` and `XmlParser`, not `HTTPClient` and `XMLParser`.
Keep the acronyms that are common in the standard library, such as `JSON` and `URI`, as they are in the library.

### Predicate methods

Name methods that return a boolean with a trailing `?`, and do not prefix them with `is_`, `has_` or `can_`.
Write `empty?` and `admin?`, not `is_empty` and `is_admin`.

### Bang methods

Only add a `!` to a method when there is a safer method of the same name without it.
The bang method is the one that mutates the receiver or raises an error.
Do not add a bang to every method that changes state.

### Conversions

Use `to_x` for a method that converts to another type, `from_x` for a constructor that converts from another type, and `parse` for a method that can fail on invalid input.

### Unused variables

Prefix the name of an unused variable or argument with an underscore, or use `_` alone.

```ruby
first, _second, third = values
ids.each_with_index.map { |_id, index| index }
```

## Language features

### Classes and modules

Use a module to group methods that do not need state, and a class when you need instances.
Prefer composition over inheritance, and limit inheritance to cases that are true "is a" relationships.
Put `attr_reader` and the other accessors at the top of the class, then the constants, and then the methods.

```ruby
class User
    MAX_NAME_LENGTH = 64

    attr_reader :name, :email

    def initialize(name:, email:)
        @name = name
        @email = email
    end
end
```

Keep the order of the class body consistent: extend and include, constants, accessors, the initializer, public methods, protected methods and private methods.

### Visibility

Put `private` and `protected` on a line of their own, and indent the methods below them at the same level as the other methods.
Do not use `private` followed by `def` on one line, and do not leave a blank line after the keyword.

```ruby
class Greeter
    def greet(name)
        "#{prefix} #{name}"
    end

    private

    def prefix
        'Hello'
    end
end
```

### Keyword arguments

Prefer keyword arguments over positional arguments when a method takes more than two arguments, or when a boolean argument would be unclear at the call site.
Use `required:` keywords for mandatory arguments.

```ruby
# Good
def create_user(name:, email:, admin: false)
    # ...
end

create_user(name: 'Ada', email: 'ada@example.com', admin: true)

# Bad
def create_user(name, email, admin)
    # ...
end
```

### Strings

Use single quotes for strings that need neither interpolation nor escape sequences.
Prefer interpolation over concatenation, and use heredocs for long multi-line text.

```ruby
greeting = "Hello, #{name}!"

message = <<~TEXT
    Dear #{name},

    Your account has been created.
TEXT
```

### Symbols and hashes

Use the `key: value` hash syntax when all keys are symbols, and `'key' => value` otherwise.
Use the shorthand `{ name:, email: }` when the variable has the same name as the key.

```ruby
options = { name: 'Ada', email: 'ada@example.com' }
headers = { 'Content-Type' => 'application/json' }
```

### Collections

Prefer the methods of `Enumerable` over loops that build up a result by hand.
Use `map`, `select`, `reject`, `find`, `sum` and `each_with_object`.
Use `each` instead of `for`.
Use `Array#first` and `Array#last` instead of `[0]` and `[-1]`.

```ruby
# Good
total = items.sum(&:price)
names = users.map(&:name)

# Bad
total = 0
items.each { |item| total += item.price }
```

Use `&:method` for short blocks that call a single method.
Use `{ ... }` for single-line blocks and `do ... end` for multi-line blocks.

### Error handling

Raise exceptions for errors that the caller cannot be expected to handle locally, and return `nil` or a result object when failure is expected.
Raise with a class and a message, such as `raise ArgumentError, 'name is empty'`.
Define your own error classes, which inherit from `StandardError`.
Rescue the most specific class possible, and never rescue `Exception`.

```ruby
class ConfigError < StandardError; end

def load_config(path)
    JSON.parse(File.read(path))
rescue Errno::ENOENT
    raise ConfigError, "no config file at #{path}"
rescue JSON::ParserError => e
    raise ConfigError, "invalid config: #{e.message}"
end
```

Do not use exceptions for flow control, and do not use a bare `rescue` that swallows errors.
Use `ensure` or a block form such as `File.open` to release resources.

### Nil handling

Use the safe navigation operator `&.` to call a method on a value that may be `nil`, but do not chain it more than twice.
Return an empty collection instead of `nil` from methods that return collections.

```ruby
city = user&.address&.city
```

### Metaprogramming

Prefer plain methods over metaprogramming.
Do not use `eval`, and do not use `method_missing` unless you also define `respond_to_missing?`.
Do not monkey patch core classes, use refinements or a wrapper class when you need to extend one.

### Global state

Do not use global variables.
Do not use class variables (`@@name`), use class-level instance variables or constants.

## Comments and documentation

### Documentation comments

Document public classes and methods with comments in the [YARD](https://yardoc.org/) format.
Start with a short summary sentence, and add details after a blank comment line.

```ruby
# Parses a duration such as "2m" or "1h30m".
#
# @param text [String] the text to parse
# @return [Integer] the duration in seconds
# @raise [ArgumentError] if the text is empty
def parse_duration(text)
    raise ArgumentError, 'text is empty' if text.empty?

    # ...
end
```

### Implementation comments

Comment why the code does something, not what it does.
Do not leave commented out code.

### TODO comments

Write `TODO` comments with a link to an issue, such as `TODO(#42)`. If no issue exists yet, open one first.

```ruby
# TODO(#41): Cache the parsed configuration.
# TODO(#42): Support YAML files.
```

## Testing

Use [RSpec](https://rspec.info/) for tests, with the specs in the `spec` directory in a structure that mirrors `lib`.
Name the example groups after the class or method they test, and the examples after the behavior they check.

```ruby
# frozen_string_literal: true

RSpec.describe StyleCheck::Duration do
    describe '.parse' do
        it 'accepts minutes' do
            expect(described_class.parse('2m')).to eq(120)
        end

        it 'rejects empty input' do
            expect { described_class.parse('') }
                .to raise_error(ArgumentError)
        end
    end
end
```

Test the public interface of a class, not its private methods.
Use `let` and `subject` for setup, and keep each example to one expectation where practical.

## Tooling

### RuboCop

Format and lint the code with [RuboCop](https://rubocop.org/).
Add this `.rubocop.yml` to the root of the repository:

```yaml
AllCops:
    NewCops: enable
    SuggestExtensions: false
    TargetRubyVersion: 3.3

Layout/LineLength:
    Max: 80

Layout/IndentationWidth:
    Width: 4

# Indent continuation lines by one level instead of aligning them.
Layout/ArgumentAlignment:
    EnforcedStyle: with_fixed_indentation
Layout/ParameterAlignment:
    EnforcedStyle: with_fixed_indentation
Layout/FirstArgumentIndentation:
    EnforcedStyle: consistent
Layout/FirstArrayElementIndentation:
    EnforcedStyle: consistent
Layout/FirstHashElementIndentation:
    EnforcedStyle: consistent
Layout/MultilineMethodCallIndentation:
    EnforcedStyle: indented

Style/StringLiterals:
    EnforcedStyle: single_quotes
Style/TrailingCommaInArguments:
    EnforcedStyleForMultiline: comma
Style/TrailingCommaInArrayLiteral:
    EnforcedStyleForMultiline: comma
Style/TrailingCommaInHashLiteral:
    EnforcedStyleForMultiline: comma

Metrics/MethodLength:
    Max: 20
Metrics/BlockLength:
    Exclude:
        - spec/**/*
```

Check the code, and let RuboCop fix what it can fix safely:

```bash
bundle exec rubocop
bundle exec rubocop --autocorrect
```

Fix the offenses instead of disabling them.
If an offense really does not apply, disable the cop on the line with `# rubocop:disable Cop/Name` and a comment that explains why.

### Type checking

Add type signatures to larger projects with [Sorbet](https://sorbet.org/) or [RBS](https://github.com/ruby/rbs) and [Steep](https://github.com/soutaro/steep).
Do this for libraries and large applications, where it pays for the effort.

### Continuous integration

Check the style and the tests on every pull request.

```bash
bundle exec rubocop
bundle exec rspec
```

## See also

- [The Ruby Style Guide](https://rubystyle.guide/)
- [RuboCop documentation](https://docs.rubocop.org/)
- [Ruby documentation](https://docs.ruby-lang.org/)
- [YARD documentation](https://rubydoc.info/gems/yard/file/docs/GettingStarted.md)
