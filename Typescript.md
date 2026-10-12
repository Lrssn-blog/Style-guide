# TypeScript Style Guide

A style guide for TypeScript, heavily based on the [Google TypeScript style guide](https://google.github.io/styleguide/tsguide.html).
TypeScript is a superset of JavaScript, so everything in the [Javascript style guide](./Javascript.md) applies unless this guide says otherwise.
This guide covers what is specific to TypeScript.

Deviations from the Google guide:

- Blocks are indented by 4 spaces and continuation lines by 8 spaces, following the house rule in `.editorconfig`.
- Return types of exported functions and public methods are always annotated.
- Relative import paths include the `.js` extension, as in the Javascript style guide.

## Table of contents

[TOC]

## Source files

### File name

File names are all lowercase and may include underscores (`_`) or dashes (`-`), but no other punctuation.
Follow the convention that your project uses.

| Extension | Content |
| --- | --- |
| `.ts` | TypeScript source |
| `.tsx` | TypeScript source that contains JSX |
| `.d.ts` | Type declarations for code that is not written in TypeScript |

Test files are named after the file they test, with a `_test` or `.test` suffix, for example `user_service_test.ts`.

### File encoding: UTF-8

Source files are encoded in UTF-8.

### Special characters

The rules for whitespace characters, escape sequences and non-ASCII characters are the same as in the [Javascript style guide](./Javascript.md#special-characters).

## Source file structure

Files consist of the following, in order:

1. License or copyright information, if present.
1. A `@fileoverview` JSDoc, if present.
1. Imports, if present.
1. The file's implementation.

Exactly one blank line separates each section that is present.

### License or copyright information

If license or copyright information belongs in a file, it belongs at the top.

### @fileoverview JSDoc

A file may have a `@fileoverview` JSDoc that describes the content of the file.
It is optional, and is most useful for files whose purpose is not obvious from their name.

```typescript
/**
 * @fileoverview Helpers for formatting dates in the user's time zone.
 */
```

### Imports

There are four variants of import statements in ES6 and TypeScript:

| Import type | Example | Use for |
| --- | --- | --- |
| Module | `import * as foo from '...';` | TypeScript imports |
| Named | `import {SomeThing} from '...';` | TypeScript imports |
| Default | `import SomeThing from '...';` | Only for external code that requires them |
| Side effect | `import '...';` | Only to load libraries for their side effects |

```typescript
import 'jasmine';
import '@polymer/paper-button';

import * as ng from '@angular/core';
import Button from 'Button';

import {Foo} from './foo.js';
```

Let the formatter sort the imports and separate the groups with blank lines.

#### Import paths

Use relative imports (`./foo.js`) for files within the same project, and module names (`@angular/core`) for packages.
Limit the number of parent steps (`../../../`), as they make the module structure hard to follow.

Include the `.js` extension in relative import paths.
With `"module": "nodenext"`, TypeScript resolves `./foo.js` to `foo.ts` at compile time, and the path stays correct in the compiled JavaScript.

```typescript
import {Foo} from '../foo/foo.js';

import {Bar} from './bar.js';
```

#### Namespace versus named imports

Use named imports for symbols that are used often in a file, or that have clear names.
Use a module import for large APIs, where the module name gives useful context.

```typescript
// Good: the names are clear on their own.
import {describe, expect, it} from 'vitest';

// Good: `tableView.Model` reads better than an imported `Model`.
import * as tableView from './tableview.js';

let model: tableView.Model;
```

```typescript
// Bad: the module name adds nothing.
import * as testing from 'vitest';

testing.describe('foo', () => {
    testing.it('bar', () => {
        testing.expect(1).toBe(1);
    });
});
```

#### Renaming imports

Only rename imports to avoid a name collision, when the imported name is generated or unclear, or when the name is clearer in the context of the importing file.
Use components of the imported module's path in the new name, as described in the [Javascript style guide](./Javascript.md#naming-imports).

```typescript
import {Cat as BigCat} from './biganimals.js';
```

#### Type only imports

Use `import type` when a symbol is only used as a type.
Type only imports are removed from the compiled JavaScript, which makes it clear that the import has no side effects.

```typescript
import type {User} from './user.js';
import {UserService} from './user_service.js';
```

Enable `verbatimModuleSyntax` in `tsconfig.json` so that the compiler enforces this rule.

#### Do not use require

Do not use `require()` or `import x = require('...')`.
Use ES module imports for everything.

### Exports

Use named exports in all code.
Do not use default exports, because importing modules then choose their own names, which leads to inconsistent names across a code base.

```typescript
// Good:
export class Foo {}

// Bad:
export default class Foo {}
```

The only exception is configuration files for tools that require a default export, such as `eslint.config.js`.

#### Export visibility

Only export symbols that are used outside the module.
Every exported symbol becomes part of the module's API, and is harder to change later.

#### Mutable exports

Do not export mutable bindings with `export let`.
If other modules need to read a changing value, export a getter function.

```typescript
// Bad:
export let count = 0;

// Good:
let count = 0;

export function getCount(): number {
    return count;
}
```

#### Container classes

Do not create classes with only static methods or properties to group things together.
Export the individual constants and functions instead.

```typescript
// Bad:
export class Container {
    static FOO = 1;
    static bar(): number {
        return 1;
    }
}

// Good:
export const FOO = 1;

export function bar(): number {
    return 1;
}
```

#### Type only exports

Use `export type` when re-exporting a type, so that the export is removed from the compiled JavaScript.

```typescript
export type {User} from './user.js';
```

### Do not use namespaces

Do not use `namespace Foo { ... }` to organize code.
Use files and ES modules instead.
`declare namespace` may be used in `.d.ts` files to describe external code that uses namespaces.

## Formatting

TypeScript follows the [formatting rules of the Javascript style guide](./Javascript.md#formatting).
In short:

- Blocks are indented by 4 spaces.
- Continuation lines are indented by at least 8 spaces.
- The column limit is 80.
- Braces follow the K&R style and are required for all control structures.
- Every statement ends with a semicolon.
- Strings use single quotes.

Do not format code by hand.
Use the formatter configuration in [Tooling](#tooling), and let the formatter decide.

### Type annotations

Put a single space after the colon of a type annotation, and no space before it.

```typescript
const name: string = getName();

function add(a: number, b: number): number {
    return a + b;
}
```

### Union and intersection types

Write union and intersection types without spaces around `|` and `&`.
This is the formatter's output and keeps type expressions compact.

```typescript
let value: string|undefined;
type Point3d = Point&{z: number};
```

When a union does not fit on one line, break after a `|` and indent the continuation lines by 8 spaces, as with any other operator.

```typescript
type UiEvent = ClickEvent|KeyboardEvent|ScrollEvent|TouchEvent|WheelEvent|
        DragEvent|FocusEvent|InputEvent;
```

### Generics

Do not put spaces inside the angle brackets of type arguments and type parameters.

```typescript
const users = new Map<string, User>();

function first<T>(items: readonly T[]): T|undefined {
    return items[0];
}
```

### Object types and interfaces

Put each member of an interface or a multi-line object type on its own line, and end each member with a semicolon.

```typescript
interface User {
    readonly id: string;
    name: string;
    email?: string;
}
```

Short inline object types may stay on one line, separated by commas.

```typescript
function move(point: {x: number, y: number}): void {
    // …
}
```

### Function signatures

When a signature does not fit on one line, break after the opening parenthesis and indent the parameters by 8 spaces.

```typescript
export async function loadUser(
        id: string, options: LoadOptions): Promise<User|undefined> {
    // …
}

export class UserService {
    constructor(
            private readonly http: HttpClient,
            private readonly logger: Logger) {}
}
```

## Naming

### Identifiers

Identifiers use only ASCII letters, digits and, in the cases below, underscores.

### Rules by identifier type

| Style | Category |
| --- | --- |
| `UpperCamelCase` | Class, interface, type, enum, decorator, type parameter, component function in TSX |
| `lowerCamelCase` | Variable, parameter, function, method, property, module alias |
| `CONSTANT_CASE` | Global constant values, including enum values |

### Abbreviations

Treat abbreviations and acronyms as whole words.

```typescript
// Good:
loadHttpUrl();
let userId: string;

// Bad:
loadHTTPURL();
let userID: string;
```

### No decorations

Do not decorate names with type information or visibility:

- Do not use a leading or trailing underscore for private members.
  Use the `private` modifier instead.
- Do not prefix interfaces with `I` (`IUser`) or suffix them with `Interface`.
- Do not use Hungarian notation (`strName`, `nCount`).

```typescript
// Good:
interface User {}

class Foo {
    private count = 0;
}

// Bad:
interface IUser {}

class Foo {
    private _count = 0;
}
```

### Descriptive names

Names should be descriptive and clear to a new reader.
Do not use ambiguous abbreviations, and do not abbreviate by deleting letters within a word.

```typescript
// Good:
let errorCount = 0;
let dnsConnectionIndex = 0;
const referrerUrl = '';

// Bad:
let n = 0;
let nErr = 0;
let cstmrId = '';
```

Short names such as `i` or `x` are fine for variables whose scope is ten lines or less, such as a loop index.

### Constants

`CONSTANT_CASE` marks values that are meant to never change, at module level or as `static readonly` class properties.
Local variables declared with `const` use `lowerCamelCase`, since `const` only means the binding is not reassigned.

```typescript
const MAX_RETRIES = 3;

class Request {
    static readonly DEFAULT_TIMEOUT_MS = 5000;
}

function retry(): void {
    const startTime = Date.now();
    // …
}
```

### Type parameters

Type parameters use a single upper case letter, such as `T`, or `UpperCamelCase`.

```typescript
function identity<T>(value: T): T {
    return value;
}

class Cache<KeyType, ValueType> {}
```

### Test names

Names of test suites and test cases are written as readable sentences.

```typescript
describe('UserService', () => {
    it('returns the cached user when one exists', () => {
        const user = service.load('1');
        expect(user).toBe(cachedUser);
    });
});
```

## Language features

### Local variable declarations

Declare all local variables with `const` or `let`.
Use `const` by default, and `let` only when the variable is reassigned.
Never use `var`.

Declare one variable per statement.

```typescript
// Good:
const a = 1;
const b = 2;

// Bad:
const a = 1, b = 2;
```

### Array literals

Do not use the `Array()` constructor.
Use array literals instead, as in the [Javascript style guide](./Javascript.md#array-literals).

#### Array types

Use `T[]` for simple types made of letters, digits and dots.
Use `Array<T>` for more complex types, such as unions and object literals.
The same rule applies to `readonly T[]` and `ReadonlyArray<T>`.

```typescript
let names: string[];
let rows: readonly Row[];
let ids: Array<string|number>;
let points: Array<{x: number, y: number}>;
```

#### Destructuring

Array destructuring is allowed, and elements that are not needed can be left out.
Default values go on the left hand side.

```typescript
const [a, b, c, ...rest] = generateResults();
let [, b2, , d] = someArray;

function destructured([a = 4, b = 2] = []): void {
    // …
}
```

#### Spread

Use the spread operator to copy or concatenate arrays, instead of `Array.prototype.concat` or `slice`.

```typescript
const combined = [...first, ...second];
const copy = [...original];
```

### Object literals

Do not use the `Object()` constructor.
Use object literals instead.

#### Iterating objects

Do not use `for (... in ...)` to iterate over objects, as it also visits inherited properties.
Use `Object.keys()`, `Object.values()` or `Object.entries()` with `for (... of ...)`.

```typescript
for (const [key, value] of Object.entries(settings)) {
    applySetting(key, value);
}
```

#### Spread and shorthand

Use the spread operator to make shallow copies of objects.
Use shorthand properties and methods where possible.

```typescript
const name = 'candy';
const updated = {
    ...defaults,
    name,
    timeoutMs: 100,
};
```

#### Destructuring parameters

Object destructuring may be used in function parameters.
Keep it shallow, use only unquoted shorthand properties, and give defaults on the left side.

```typescript
interface Options {
    num?: number;
    str?: string;
}

function destructured({num, str = 'default'}: Options = {}): void {
    // …
}
```

### Classes

Class declarations are not followed by a semicolon, and neither are methods.

#### Class members

Do not use private fields (`#field`).
Use TypeScript's `private` and `protected` modifiers instead, which are easier to read and to test.

Mark properties that are never reassigned outside the constructor with `readonly`.

```typescript
class Counter {
    private readonly startValue: number;
    private count = 0;

    constructor(startValue: number) {
        this.startValue = startValue;
    }
}
```

#### Parameter properties

Use parameter properties instead of declaring a property and assigning it from a constructor parameter.

```typescript
// Good:
class Foo {
    constructor(private readonly barService: BarService) {}
}

// Bad:
class Foo {
    private readonly barService: BarService;

    constructor(barService: BarService) {
        this.barService = barService;
    }
}
```

#### Field initializers

Initialize properties where they are declared when possible, instead of in the constructor.

```typescript
// Good:
class Foo {
    private readonly userList: string[] = [];
}

// Bad:
class Foo {
    private readonly userList: string[];

    constructor() {
        this.userList = [];
    }
}
```

#### Visibility

Limit the visibility of members as much as possible.
Do not write the `public` modifier, since members are public by default.
The exception is parameter properties, which need a modifier to become properties.

```typescript
// Good:
class Foo {
    bar = new Bar();

    constructor(public baz: Baz) {}
}

// Bad:
class Foo {
    public bar = new Bar();
}
```

#### Getters and setters

Getters and setters may be used, but a getter must not change observable state.
At least one of a getter and setter pair must do more than read or write a backing property, otherwise use a public property.

```typescript
class Foo {
    private wrappedBar = '';

    get bar(): string {
        return this.wrappedBar || 'bar';
    }

    set bar(value: string) {
        this.wrappedBar = value.trim();
    }
}
```

#### Static methods

Static methods are called on the class itself (`Foo.method()`), never on an instance or a subclass.
Do not use `this` inside a static method.

#### Constructors

Always call constructors with parentheses, even when there are no arguments: `new Foo()`.

Do not write empty constructors, or constructors that only call `super()` with the same arguments.

```typescript
// Bad:
class Bar extends Foo {
    constructor() {
        super();
    }
}
```

Separate the constructor from other members with a blank line.

#### Prototypes

Do not modify prototypes directly.
Use classes, and never change the prototypes of built-in objects.

### Functions

#### Function declarations

Use function declarations for named functions, instead of assigning an arrow function to a variable.

```typescript
// Good:
function foo(): void {
    // …
}

// Bad:
const foo = (): void => {
    // …
};
```

Arrow functions may be assigned to a variable when the type of the variable is needed, for example when implementing a function type.

```typescript
const handler: EventHandler = (event) => {
    // …
};
```

#### Arrow functions in expressions

Use arrow functions for callbacks and other function expressions.
Do not use `function` expressions.

```typescript
// Good:
bar(() => {
    this.doSomething();
});

// Bad:
bar(function() {
    // …
});
```

Only use the concise body form (without braces) when the return value is used.

```typescript
// Good: the return value is used.
const doubled = numbers.map((n) => n * 2);

// Good: the block body makes it clear nothing is returned.
myPromise.then((value) => {
    console.log(value);
});

// Bad: the return value of console.log leaks to the caller.
myPromise.then((value) => console.log(value));
```

#### Rebinding this

Do not use `function` expressions or `.bind()` to control `this`.
Use arrow functions, which keep the `this` of the surrounding scope.

#### Arrow functions as properties

Classes should not use properties initialized to arrow functions.
Call an instance method from an arrow function at the call site instead.
The exception is event handlers that must be uninstalled later, which need a stable reference.

```typescript
class DelayHandler {
    constructor() {
        setTimeout(() => {
            this.patienceTracker();
        }, 5000);
    }

    private patienceTracker(): void {
        // …
    }
}
```

#### Parameter initializers

Default parameter values may be used, but keep them simple and free of side effects.

```typescript
function process(name: string, extraContext: string[] = []): void {
    // …
}
```

#### Rest and spread

Use rest parameters instead of `arguments`, and the spread operator instead of `Function.prototype.apply`.

```typescript
function variadic(array: number[], ...numbers: number[]): void {
    // …
}

variadic(...myArray);
```

#### Generators

Attach the `*` to the `function` keyword, and separate it from the name with a space.
When delegating to another generator, attach the `*` to `yield`.

```typescript
function* generator(): Generator<number> {
    yield 1;
    yield* otherGenerator();
}
```

### this

Only use `this` in class constructors and methods, and in arrow functions defined within them.
Never use `this` to refer to the global object, the context of an `eval` or the target of an event.

### Primitive literals

#### String literals

Use single quotes for ordinary string literals and template literals for interpolation, as in the [Javascript style guide](./Javascript.md#string-literals).
Do not use line continuations.

#### Number literals

Numbers may be written in decimal, hex, octal or binary.
Use lowercase `0x`, `0o` and `0b` prefixes, and never use a leading zero otherwise.

#### Type coercion

Use `String()` and `Boolean()` (or `!!`) to convert values.
Do not use string concatenation or the unary `+` operator to convert values.

```typescript
const bool = Boolean(false);
const str = String(aNumber);
const bool2 = !!str;
const str2 = `result: ${bool2}`;
```

Use `Number()` to parse numbers, and check the result for `NaN` unless failing to parse is impossible from context.

```typescript
const aNumber = Number('123');
if (!isFinite(aNumber)) {
    throw new Error('Expected a number');
}
```

Do not use `parseInt()` or `parseFloat()` for decimal numbers, since they silently ignore trailing characters.
`parseInt(text, radix)` may be used for other bases, after checking that the input only contains valid digits.

Implicit coercion to boolean is fine in conditions, except for enums.
Compare enum values explicitly, since the first enum member is `0` and therefore falsy.

```typescript
enum SupportLevel {
    NONE,
    BASIC,
    ADVANCED,
}

const level: SupportLevel = getLevel();

// Good:
if (level !== SupportLevel.NONE) {
    // …
}

// Bad: this is false for SupportLevel.NONE, which is easy to miss.
if (level) {
    // …
}
```

### Control structures

#### Braces

Braces are required for all control structures, even when the body is a single statement.

#### For loops

Prefer `for (... of ...)` to iterate over arrays.
Use `Array.prototype.forEach` and plain `for` loops only when the index is needed or the loop is performance critical.
Never use `for (... in ...)` on arrays, as it iterates over the indexes as strings.

```typescript
for (const user of users) {
    notify(user);
}

for (const [index, user] of users.entries()) {
    console.log(index, user);
}
```

#### Exceptions

Always throw `Error` or a subclass of `Error`, and always create them with `new`.
Never throw strings or other values, as they have no stack trace.

```typescript
// Good:
throw new Error('Something went wrong');

// Bad:
throw 'Something went wrong';
```

Catch variables have the type `unknown`.
Narrow the type before using the error.

```typescript
try {
    doSomething();
} catch (e: unknown) {
    if (e instanceof NetworkError) {
        retry();
        return;
    }
    throw e;
}
```

Keep `try` blocks focused on the code that may throw.
Empty `catch` blocks are only allowed with a comment that explains why the error is ignored.

```typescript
try {
    return handleNumericResponse(response);
} catch (e: unknown) {
    // Response is not numeric. Continue to handle as text.
}
return handleTextResponse(response);
```

#### Switch statements

Every `switch` statement has a `default` group, and it comes last.
Non-empty case groups must not fall through to the next group.
Empty groups may fall through, to share code between several labels.

```typescript
switch (x) {
    case X.ITEM_1:
    case X.ITEM_2:
        doSomething();
        break;
    default:
        doSomethingElse();
}
```

#### Equality checks

Always use `===` and `!==`.
The only exception is `== null` and `!= null`, which match both `null` and `undefined`.

```typescript
if (foo == null) {
    // foo is null or undefined.
}
```

### Type and non-null assertions

Type assertions (`x as Foo`) and non-null assertions (`y!`) are unsafe, as they are not checked at runtime.
Do not use them without a good reason, and add a comment that explains why the assertion is safe.

```typescript
// Good: check the type, so the compiler can narrow it.
if (x instanceof Foo) {
    x.foo();
}

// Allowed, with an explanation:
// The element is created in the template, so it always exists.
const button = document.querySelector('#submit') as HTMLButtonElement;
```

Use the `as` syntax, not angle brackets (`<Foo>x`).

Use a type annotation instead of a type assertion for object literals, so the compiler checks the object against the type.

```typescript
// Good:
const foo: Foo = {
    bar: 123,
    bam: 'abc',
};

// Bad: misspelled or missing properties are not reported.
const foo = {
    bar: 123,
    bam: 'abc',
} as Foo;
```

### Decorators

Do not define new decorators.
Only use the decorators defined by frameworks, such as Angular.
Place decorators directly before the symbol they decorate, with no blank line between them.

```typescript
@Component({
    selector: 'user-card',
    template: '<p>{{name}}</p>',
})
class UserCard {
    @Input() name = '';
}
```

### Disallowed features

#### Wrapper objects

Do not create wrapper objects for primitives with `new String()`, `new Boolean()` or `new Number()`.

#### Automatic semicolon insertion

Do not rely on automatic semicolon insertion.
End every statement with a semicolon.

#### Const enums

Do not use `const enum`.
Use a plain `enum` instead, which behaves the same way in all build tools.

#### Debugger statements

Do not commit `debugger` statements.

#### with, eval and Function

Do not use `with`, `eval()` or the `Function(...string)` constructor.

#### Non-standard features

Do not use non-standard language features, such as features that are only supported by one runtime or proposals that have not reached stage 4.

#### Modifying built-in objects

Never modify built-in types, either by adding methods to their constructors or prototypes, or by adding symbols to the global object.

#### Suppressing compiler errors

Do not use `@ts-ignore` or `@ts-nocheck`.
They hide every error on the line or in the file, including errors added later.
Fix the type error instead.

`@ts-expect-error` may be used in tests to check that invalid code is rejected, with a comment that explains which error is expected.

## Type system

### Type inference

Rely on type inference for local variables whose type is obvious from the value.
Do not annotate variables initialized with a literal or a `new` expression.

```typescript
// Good:
const count = 15;
const users = new Set<User>();

// Bad:
const count: number = 15;
const users: Set<User> = new Set<User>();
```

Annotate a variable when the inferred type is too wide or not obvious to the reader.

```typescript
// The type of an empty array or object cannot be inferred.
const ids: string[] = [];
```

### Return types

Annotate the return types of exported functions and public methods.
The annotation documents the API, and an accidental change in the implementation becomes a compile error instead of a change to the API.
Return types of local functions and private methods may be left to inference.

```typescript
export function parseUser(json: string): User {
    return JSON.parse(json) as User;
}
```

### Undefined and null

TypeScript supports both `undefined` and `null`.
Neither is preferred in general, but follow the conventions of the APIs you use.
For example, the DOM uses `null`, while optional properties use `undefined`.

#### Nullable type aliases

Do not include `|null` or `|undefined` in a type alias.
Add them where the alias is used, so the reader can see that the value may be missing.

```typescript
// Bad:
type CoffeeResponse = Latte|Americano|undefined;

// Good:
type CoffeeResponse = Latte|Americano;

function getCoffee(): CoffeeResponse|undefined {
    // …
}
```

#### Optional versus undefined

Prefer optional parameters and properties (`?`) over `|undefined`.

```typescript
// Good:
interface CoffeeOrder {
    sugarCubes: number;
    milk?: Whole|LowFat|HalfHalf;
}

function pourCoffee(volume?: Milliliter): void {
    // …
}
```

### Interfaces versus type aliases

Use interfaces to declare object types, not type aliases.
Interfaces give clearer error messages, are faster to type check and can be extended.

```typescript
// Good:
interface User {
    firstName: string;
    lastName: string;
}

// Bad:
type User = {
    firstName: string,
    lastName: string,
};
```

Use type aliases for everything an interface cannot express, such as unions, tuples, function types and mapped types.

### Structural typing

TypeScript's type system is structural, so any object with the right shape is accepted.
Annotate object literals with their type where they are declared, so that errors are reported where the object is created and not where it is used.

```typescript
// Good:
const foo: Foo = {
    a: 123,
    b: 'abc',
};

// Bad: an error in the object only shows up where foo is used.
const foo = {
    a: 123,
    b: 'abc',
};
```

When a class implements an interface, declare it with `implements` so the compiler checks the class.

### The any type

Avoid `any`.
It turns off type checking for everything it touches, including values derived from it.
Use, in order of preference:

1. A more specific type, such as an interface or a union.
1. A generic type parameter.
1. `unknown`, and narrow it before use.

```typescript
// Good: the value must be checked before use.
function handle(value: unknown): void {
    if (typeof value === 'string') {
        console.log(value.toUpperCase());
    }
}

// Bad: nothing is checked.
function handle(value: any): void {
    console.log(value.toUpperCase());
}
```

If `any` is really needed, for example in tests, add a lint suppression with a comment that explains why.

### The {} type

Do not use `{}` as a type.
It accepts every value except `null` and `undefined`, which is rarely the intent.
Use `unknown` for any value, `Record<string, T>` for a dictionary, or `object` for any non-primitive.

### Wrapper types

Never use the wrapper types `String`, `Boolean`, `Number`, `Symbol`, `BigInt` or `Object` in type annotations.
Use the lowercase primitive types instead.

```typescript
// Good:
let name: string;

// Bad:
let name: String;
```

### Maps and dictionaries

Use `Map` and `Set` for collections whose keys are not known in advance.
If an object is used as a dictionary, type it with `Record<string, T>` or an index signature with a meaningful key name.

```typescript
const fileSizes = new Map<string, number>();

const users: {[userName: string]: number} = {};
```

### Enums versus union types

Prefer a union of string literal types for a simple set of values.
Union types need no runtime code and are easy to read in error messages.

```typescript
type Direction = 'up'|'down'|'left'|'right';
```

Use an `enum` when the values need to be iterated over or are numbers that must be compared.
Write enum members in `CONSTANT_CASE`.

### Tuple types

Use tuple types instead of interfaces for small pairs of values where the meaning is obvious, such as function results that are destructured right away.
Use an interface with named properties when the meaning of the elements is not obvious.

```typescript
function splitInHalf(input: string): [string, string] {
    const middle = Math.floor(input.length / 2);
    return [input.slice(0, middle), input.slice(middle)];
}

const [leftHalf, rightHalf] = splitInHalf('my string');
```

### Generics

Use generics when a function or class works with several types and the types of its parameters and results are connected.
Do not use generics where a union or an overload is clearer.

Do not write functions whose type parameter is only used in the return type, since the caller then makes an unchecked assertion.

```typescript
// Bad: the caller chooses T, but nothing checks it.
function fetchJson<T>(url: string): Promise<T> {
    // …
}
```

### Mapped and conditional types

Mapped and conditional types are powerful, but hard to read and to debug.
Use the simplest type that works, and prefer an explicit interface over a complex type expression.

```typescript
// Good: easy to read.
interface UserSummary {
    name: string;
    email: string;
}

// Discouraged: the reader has to look up User to know the shape.
type UserSummary = Pick<User, 'name'|'email'>;
```

## Comments and documentation

### JSDoc versus comments

There are two kinds of comments:

- Documentation comments (`/** … */`) describe what a symbol is and how to use it, and are read by users of the code and by tools.
- Implementation comments (`// …`) explain how the code works, and are read by people changing it.

### Document exported symbols

Write a JSDoc comment for every exported symbol, unless its name and type say everything there is to say.

```typescript
/**
 * Loads a user from the server.
 *
 * Users are cached, so repeated calls with the same ID only make one request.
 *
 * @param id The ID of the user to load.
 * @return The user, or undefined if no user exists with the ID.
 */
export async function loadUser(id: string): Promise<User|undefined> {
    // …
}
```

### Do not repeat types

Do not declare types in JSDoc tags, such as `@param {string}`, `@type` or `@return {number}`.
The types are already in the TypeScript code.

Only write `@param` and `@return` tags when they add information beyond the name and the type.

### JSDoc format

Multi-line JSDoc comments start with `/**` on its own line, and every following line starts with `*` aligned with the first `*`.
Single-line JSDoc comments are allowed for short descriptions.

```typescript
/** The default timeout for requests, in milliseconds. */
export const DEFAULT_TIMEOUT_MS = 5000;
```

JSDoc is written in Markdown.

### Parameter properties

Document parameter properties with `@param` on the constructor.

```typescript
class ParamProps {
    /**
     * @param percolator The percolator used for brewing.
     * @param beans The beans to brew.
     */
    constructor(
            private readonly percolator: Percolator,
            private readonly beans: CoffeeBean[]) {}
}
```

### Comments before decorators

Place JSDoc comments before decorators, not between the decorator and the symbol.

```typescript
/** A component that shows a user's name. */
@Component({selector: 'user-card', template: '<p>{{name}}</p>'})
class UserCard {
    @Input() name = '';
}
```

### Parameter name comments

Use parameter name comments when the meaning of an argument is not clear from the call, as described in the [Javascript style guide](./Javascript.md#parameter-name-comments).

```typescript
someFunction(obviousParam, /* shouldRender= */ true, /* name= */ 'hello');
```

### TODO comments

Write `TODO` comments with the user name of the author or a link to an issue, so that it is clear who to ask.

```typescript
// TODO(lrssn): Remove this workaround when the API returns sorted results.
// TODO(#42): Support pagination.
```

## Tooling

### Compiler

Enable strict type checking in `tsconfig.json`.
This is a good starting point for a Node.js project:

```json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "nodenext",
        "moduleResolution": "nodenext",
        "strict": true,
        "noFallthroughCasesInSwitch": true,
        "noImplicitOverride": true,
        "noImplicitReturns": true,
        "noUncheckedIndexedAccess": true,
        "verbatimModuleSyntax": true,
        "forceConsistentCasingInFileNames": true,
        "skipLibCheck": true,
        "declaration": true,
        "sourceMap": true,
        "rootDir": "src",
        "outDir": "dist"
    },
    "include": ["src"]
}
```

Check the types in continuous integration without writing any output:

```bash
npx tsc --noEmit
```

### Formatter

Format TypeScript and JavaScript with [clang-format](https://clang.llvm.org/docs/ClangFormat.html), which is the formatter used for Google's guide.
Add this `.clang-format` to the root of the repository:

```yaml
---
Language: JavaScript
BasedOnStyle: Google
IndentWidth: 4
ContinuationIndentWidth: 8
ColumnLimit: 80
JavaScriptQuotes: Single
```

The `JavaScript` language setting covers both `.js` and `.ts` files.
Format all files in place with:

```bash
clang-format -i src/*.ts
```

### Linter

Use [ESLint](https://eslint.org/) with [typescript-eslint](https://typescript-eslint.io/) to catch the rules the compiler does not check.
Add this `eslint.config.js` to the root of the repository:

```javascript
import eslint from '@eslint/js';
import {defineConfig} from 'eslint/config';
import tseslint from 'typescript-eslint';

export default defineConfig(
        eslint.configs.recommended,
        tseslint.configs.strictTypeChecked,
        tseslint.configs.stylisticTypeChecked,
        {
            languageOptions: {
                parserOptions: {
                    projectService: true,
                    tsconfigRootDir: import.meta.dirname,
                },
            },
            rules: {
                '@typescript-eslint/consistent-type-imports': 'error',
                '@typescript-eslint/explicit-module-boundary-types': 'error',
                'no-restricted-syntax': ['error', 'ExportDefaultDeclaration'],
            },
        },
);
```

Leave formatting rules to clang-format, and do not enable ESLint's formatting rules.

Run the linter on the source files with:

```bash
npx eslint src
```

## See also

- [Google TypeScript style guide](https://google.github.io/styleguide/tsguide.html)
- [Javascript style guide](./Javascript.md)
- [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
