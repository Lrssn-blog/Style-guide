# Haskell Style Guide

A style guide for Haskell.
It is based on [Johan Tibell's Haskell style guide](https://github.com/tibbe/haskell-style-guide), the [Haskell Language Style Guide of Kowainik](https://kowainik.github.io/posts/2019-02-06-style-guide) and the conventions of the GHC `base` library.

Deviations from these guides:

- Lines are at most 80 characters long instead of 100 or 120, following the house rule in `.editorconfig`.
- Indentation is 4 spaces instead of 2, following the house rule in `.editorconfig`.
- Code is formatted by [Fourmolu](#fourmolu), so the formatting rules below describe what the formatter produces.

## Table of contents

[TOC]

## Toolchain

Install the compiler and the tools with [GHCup](https://www.haskell.org/ghcup/), and build projects with [Cabal](https://cabal.readthedocs.io/).
Use a GHC version that is supported by the latest Haskell Language Server, and declare the versions the project builds with in the `tested-with` field of the `.cabal` file.

```cabal
cabal-version: 3.0
name:          style-check
version:       1.0.0.0
build-type:    Simple
tested-with:   GHC == 9.10.2

library
    hs-source-dirs:   src
    default-language: GHC2021
    build-depends:    base >=4.20 && <5
    exposed-modules:  StyleCheck
```

Use the `GHC2021` language edition for new projects.
It enables the extensions that nearly every project uses, such as `ScopedTypeVariables`, `TypeApplications` and `DeriveFunctor`.

## Source files

### File names

Name a file after the module it contains, with one module per file, and put the file in a directory structure that mirrors the module hierarchy.
The module `Data.UserStore` lives in `src/Data/UserStore.hs`.
File names end in `.hs`.

### File encoding: UTF-8

Source files are encoded in UTF-8.
Avoid non-ASCII characters in identifiers and operators.

### Package names

Package names are lowercase words separated by hyphens, such as `style-check`.
A package that provides one library and one executable uses the same name for both.

### Project layout

```text
style-check/
├── app/
│   └── Main.hs
├── src/
│   └── StyleCheck.hs
├── test/
│   └── Main.hs
├── cabal.project
└── style-check.cabal
```

Keep the logic in the library under `src`, and keep `app/Main.hs` as small as possible so that all the code can be tested.

## Source file structure

A source file consists of the following parts, in this order, separated by one blank line:

1. `LANGUAGE` pragmas and other file-level pragmas.
2. The module header, with an export list.
3. Imports.
4. Top-level declarations.

### Language pragmas

Put each `LANGUAGE` pragma on its own line, sorted alphabetically, and align the closing `#-}`.
Only enable the extensions the module needs, and prefer enabling them for the whole project in the `.cabal` file only when almost every module uses them.

```haskell
{-# LANGUAGE DerivingStrategies #-}
{-# LANGUAGE LambdaCase #-}
{-# LANGUAGE OverloadedStrings #-}
```

### Module header

Every module has an explicit export list.
Put each export on its own line, with a leading comma, and group the exports with a Haddock heading when the list is long.

```haskell
module StyleCheck.User
    ( User (..)
    , UserId
    , mkUser
    , renderUser
    ) where
```

Export only what other modules need.
Export the type of an abstract value without its constructors, and provide smart constructors instead.

### Imports

Put imports after the module header, separated from it by one blank line.
Sort them alphabetically by module name inside each group, and separate the groups with a blank line:

1. Modules from the standard library and from other packages.
2. Modules of the same package.

Import everything that is not a type or a well known operator either qualified or with an explicit import list.
Never import a module without either, apart from `Prelude` and the modules named below.

```haskell
import Data.List.NonEmpty (NonEmpty (..))
import Data.Map.Strict (Map)
import Data.Map.Strict qualified as Map
import Data.Text (Text)
import Data.Text qualified as Text

import StyleCheck.Config (Config (..))
```

Use the `ImportQualifiedPost` style (`import Data.Map qualified as Map`), which is part of `GHC2021`.
Use the same short alias for the same module in every file:

| Module | Alias |
| --- | --- |
| `Data.Map.Strict` | `Map` |
| `Data.Set` | `Set` |
| `Data.Text` | `Text` |
| `Data.ByteString` | `BS` |
| `Data.List.NonEmpty` | `NonEmpty` |
| `Data.Vector` | `Vector` |

## Formatting

Do not format code by hand.
Use Fourmolu with the configuration in [Tooling](#tooling), and let it decide.
The rules below describe what the formatter produces.

### Indentation and line length

Indent by 4 spaces, never tabs.
Lines are at most 80 characters long.

### Blank lines

Separate top-level declarations with a single blank line.
Do not start or end a block with a blank line.
A type signature is directly above its definition, without a blank line.

### Function arguments and signatures

When a type signature does not fit on one line, put each arrow at the start of its own line.

```haskell
createUser
    :: Text
    -> Text
    -> [Role]
    -> Settings
    -> Either UserError User
createUser name email roles settings = ...
```

When the arguments of a call do not fit on one line, put each argument on its own line, indented by 4 spaces.

### Where clauses

Put `where` on its own line, indented by 4 spaces from the start of the definition, and indent the bindings by 4 more.
Order the bindings in the order in which they are first used.

```haskell
area :: Shape -> Double
area shape =
    case shape of
        Circle r -> circleArea r
        Rectangle w h -> w * h
  where
    circleArea r = pi * r * r
```

### Case expressions and guards

Put `case ... of` alternatives on their own lines, indented by 4 spaces.
Put guards on their own lines too, and align the `=` signs when the guards are short.

```haskell
classify :: Int -> Size
classify n
    | n < 10 = Small
    | n < 100 = Medium
    | otherwise = Large
```

Prefer a `case` expression or pattern matching in the function head over `if` when matching on a constructor.
Use `if` only for plain booleans, and write `then` and `else` on their own lines when the expression does not fit on one line.

### Let expressions

Prefer `where` over `let`.
When you use `let`, put the bindings on separate lines and right-align `in` with them.

```haskell
let total = sum prices
    count = length prices
 in total / fromIntegral count
```

### Operators

Put spaces around infix operators, except in sections where the operator is tight against its operand, as in `(+ 1)`.
When an expression with operators does not fit on one line, break it before the operator, and indent the next line by 4 spaces.

```haskell
render user =
    name user
        <> " <"
        <> email user
        <> ">"
```

Use `$` to avoid parentheses only when it makes the code easier to read, and never use it twice in one expression.
Use `.` to chain functions, and `<$>`, `<*>` and `>>=` for applicative and monadic code.

### Records

Declare records with one field per line, with a leading comma, and align the `::` signs.

```haskell
data User = User
    { userId :: !UserId
    , userName :: !Text
    , userEmail :: !Text
    }
    deriving stock (Eq, Show)
```

Create and update records with the same layout.

### Lists and tuples

Put a space after each comma.
When a list does not fit on one line, put each element on its own line with a leading comma.

```haskell
defaultRoles :: [Role]
defaultRoles =
    [ Reader
    , Writer
    , Admin
    ]
```

### Data declarations

Put each constructor on its own line, with a leading `|`, and put `deriving` on its own line below the constructors.

```haskell
data Shape
    = Circle !Double
    | Rectangle !Double !Double
    deriving stock (Eq, Show)
```

### Comments

Use `--` for line comments, followed by a space.
Write comments as full sentences, and put them on the line above the code they describe.
Do not use block comments (`{- ... -}`) to disable code, delete the code instead.

## Naming

### Rules by item type

| Item | Case | Example |
| --- | --- | --- |
| Module | `UpperCamelCase`, one word per level | `Data.UserStore` |
| Type, type class, type family | `UpperCamelCase` | `UserStore`, `ToJSON` |
| Data constructor | `UpperCamelCase` | `Rectangle` |
| Function, value, argument | `lowerCamelCase` | `parseUser` |
| Type variable | Short and lowercase | `a`, `k`, `v`, `m` |
| Record field | `lowerCamelCase`, prefixed with the type name | `userName` |
| Language extension | As in GHC | `LambdaCase` |

### Acronyms

Treat an acronym like any other word: only the first letter is uppercase.
Write `HttpClient` and `parseXml`, not `HTTPClient` and `parseXML`.

### Record fields

Prefix record fields with the name of the type in `lowerCamelCase`, so that they do not clash with the fields of other types, such as `userName` and `groupName`.
Alternatively, enable `DuplicateRecordFields` and `OverloadedRecordDot` and access fields with `user.name`.
Use one of the two approaches in a project, not both.

### Booleans

Name boolean values and functions as a question, with a prefix such as `is`, `has` or `can`.
Write `isEmpty`, `hasPermission`, not `empty`, `permission`.

### Conversions

Name a function that converts between two types `toX` or `fromX`, and one that can fail `parseX`.
Write `toText`, `fromList`, `parseDuration`.

### Type variables

Use short names for type variables, starting with `a`, `b` and `c`, and use a descriptive name when the meaning matters, such as `k` and `v` for keys and values or `m` for a monad.

## Language features

### Type signatures

Write a type signature for every top-level binding, and for every binding with a polymorphic or non-obvious type in a `where` clause.
Do not rely on type inference for exported functions.

```haskell
parseDuration :: Text -> Either ParseError NominalDiffTime
```

### Partial functions

Do not use partial functions, which fail for some inputs:

- `head`, `tail`, `init`, `last` and `!!`.
- `fromJust`.
- `read`, which throws on bad input.
- `undefined` and `error`, except for unreachable code.

Return a `Maybe` or an `Either`, use pattern matching, or use `NonEmpty` when a list cannot be empty.
Use `readMaybe` from `Text.Read` instead of `read`.

```haskell
-- Bad
firstUser :: [User] -> User
firstUser = head

-- Good
firstUser :: [User] -> Maybe User
firstUser users =
    case users of
        [] -> Nothing
        user : _ -> Just user
```

Enable `-Wincomplete-patterns` and treat it as an error, so that a missing case is a compile error.

### Maybe and Either

Use `Maybe` when a value may be absent and there is only one reason for it.
Use `Either` with a descriptive error type when the caller needs to know why an operation failed.
Do not use `Either String`, define an error type.

```haskell
data ParseError
    = EmptyInput
    | InvalidUnit !Char
    deriving stock (Eq, Show)
```

### Newtypes

Use `newtype` to give a distinct type to values that would otherwise share one, such as identifiers.
Derive instances with `deriving newtype` and `deriving stock` instead of writing them by hand.

```haskell
newtype UserId = UserId Int
    deriving stock (Show)
    deriving newtype (Eq, Ord)
```

### Type classes

Give type classes a small interface and laws that are written down in the Haddock comments.
Do not define an instance for a type you do not own, unless it is in the module of the class or the type, to avoid orphan instances.
Prefer ordinary functions over a type class when only one instance exists.

### Strictness

Make the fields of data types strict with a bang (`!`) unless laziness is needed.
Use `foldl'` instead of `foldl`, and `Data.Map.Strict` instead of `Data.Map.Lazy`.
Enable `StrictData` for a module that only holds data types.

### Laziness

Do not use lazy I/O such as `getContents` or `readFile` on large inputs.
Use `Data.Text.IO` with strict reads, or a streaming library.

### Strings

Do not use `String` for text.
Use `Text` from the `text` package for human readable text and `ByteString` for binary data.
Enable `OverloadedStrings` to write `Text` literals.

### Point-free style

Use point-free style when it makes a function shorter and clearer, and name the argument when it does not.
Do not chain more than three functions with `.`.

```haskell
-- Good
countWords :: Text -> Int
countWords = length . Text.words

-- Bad: hard to follow
process = map (uncurry (+)) . filter ((> 0) . fst) . zip [1 ..] . concatMap f
```

### Pattern matching

Match on every constructor of a data type, and do not use a wildcard (`_`) pattern for a type that may grow.
Use `LambdaCase` for short functions that only match on their argument.

```haskell
describe :: Shape -> Text
describe = \case
    Circle _ -> "circle"
    Rectangle _ _ -> "rectangle"
```

### Language extensions

Enable only the extensions that the code needs.
The extensions below are always fine to use:

`BangPatterns`, `DerivingStrategies`, `LambdaCase`, `OverloadedStrings`, `RecordWildCards` (in small scopes), `ScopedTypeVariables` and `TypeApplications`.

Ask for a review before using `TemplateHaskell`, `UndecidableInstances`, `AllowAmbiguousTypes` or `GADTs`-heavy designs.

### Exceptions

Use `Either` for errors that the caller can handle, and exceptions only for I/O failures and for bugs.
Define your own exception types with `Exception` instances, and catch the most specific type possible.
Never catch `SomeException` without rethrowing, except at the top of a program.
Use `bracket` or `finally` to release resources.

### Effects and I/O

Keep I/O at the edge of the program.
Write the logic as pure functions that take and return values, and call them from a thin `IO` layer.
Use `mapM_` and `forM_` for effects, and `traverse` and `for` when the results are needed.

## Comments and documentation

### Haddock comments

Document every exported item with a Haddock comment that starts with `-- |`.
Start with a short summary sentence, and add details after a blank comment line.
Document the arguments of a function and the constructors of a type with `-- ^`.

```haskell
-- | Parses a duration such as @2m@ or @1h30m@.
--
-- Returns an error for empty input.
parseDuration
    :: Text
    -- ^ The text to parse.
    -> Either ParseError NominalDiffTime
```

Write a Haddock comment for the module at the top, after the pragmas and before the `module` keyword.

### Implementation comments

Comment why the code does something, not what it does.
Do not leave commented out code.

### TODO comments

Write `TODO` comments with a link to an issue, such as `TODO(#42)`. If no issue exists yet, open one first.

```haskell
-- TODO(#41): Cache the parsed configuration.
-- TODO(#42): Support TOML files.
```

## Testing

Use [Hspec](https://hspec.github.io/) or [Tasty](https://github.com/UnkindPartition/tasty) for tests, and [QuickCheck](https://hackage.haskell.org/package/QuickCheck) for properties.
Put the tests in the `test` directory, in modules that mirror the modules they test with a `Spec` suffix, such as `StyleCheck.UserSpec`.
Name tests after the behavior they check.

```haskell
spec :: Spec
spec = describe "parseDuration" $ do
    it "accepts minutes" $
        parseDuration "2m" `shouldBe` Right 120

    it "rejects empty input" $
        parseDuration "" `shouldBe` Left EmptyInput

    it "round-trips with renderDuration" $
        property $ \(NonNegative n) ->
            parseDuration (renderDuration n) === Right n
```

Test the pure functions of the library directly, and keep tests that need I/O to a minimum.

## Tooling

### Fourmolu

Format the code with [Fourmolu](https://fourmolu.github.io/).
Add this `fourmolu.yaml` to the root of the repository:

```yaml
indentation: 4
column-limit: 80
function-arrows: leading
comma-style: leading
import-export-style: leading
indent-wheres: false
record-brace-space: false
newlines-between-decls: 1
haddock-style: single-line
let-style: auto
in-style: right-align
unicode: never
respectful: true
```

Format all files in place, and check the formatting in continuous integration:

```bash
fourmolu --mode inplace $(git ls-files '*.hs')
fourmolu --mode check $(git ls-files '*.hs')
```

### HLint

Use [HLint](https://github.com/ndmitchell/hlint) to find code that can be simplified and to ban unsafe functions.
Add this `.hlint.yaml` to the root of the repository:

```yaml
# Suggestions of these groups are enabled in addition to the defaults.
- group: {name: dollar, enabled: true}
- group: {name: generalise, enabled: true}

# Partial functions and unsafe code are banned. See "Partial functions".
- functions:
      - {name: head, within: []}
      - {name: tail, within: []}
      - {name: init, within: []}
      - {name: last, within: []}
      - {name: fromJust, within: []}
      - {name: unsafePerformIO, within: []}
```

```bash
hlint src app test
```

Fix the hints instead of ignoring them.
If a hint really does not apply, disable it on the line with an `{-# ANN ... #-}` annotation and a comment that explains why.

### Compiler warnings

Build with all warnings enabled, and treat warnings as errors in continuous integration.
Add the options to the `common` stanza of the `.cabal` file, and import it in every component.

```cabal
common warnings
    ghc-options:
        -Wall
        -Wcompat
        -Widentities
        -Wincomplete-record-updates
        -Wincomplete-uni-patterns
        -Wmissing-deriving-strategies
        -Wredundant-constraints
        -Wunused-packages
```

Pass `--ghc-options=-Werror` in continuous integration instead of putting `-Werror` in the `.cabal` file, so that a new GHC release does not break the builds of your dependents.

### Dependencies

Commit the `cabal.project` file, and set upper bounds on the versions of dependencies with the Package Versioning Policy (PVP).
Check for outdated dependencies with `cabal outdated`.

### Continuous integration

Check the formatting, the hints and the tests on every pull request.

```bash
fourmolu --mode check $(git ls-files '*.hs')
hlint src app test
cabal build all --ghc-options=-Werror
cabal test all
```

## See also

- [Johan Tibell's Haskell style guide](https://github.com/tibbe/haskell-style-guide)
- [Kowainik Haskell style guide](https://kowainik.github.io/posts/2019-02-06-style-guide)
- [Haskell Package Versioning Policy](https://pvp.haskell.org/)
- [Haddock documentation](https://haskell-haddock.readthedocs.io/)
