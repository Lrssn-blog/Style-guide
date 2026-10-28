# JavaScript Style Guide

A style guide for JavaScript.
The rules are based on the [Google JavaScript style guide](https://google.github.io/styleguide/jsguide.html), and the text and the examples are our own.

Deviations from the Google guide:

- Blocks are indented by 4 spaces and continuation lines by 8 spaces, following the house rule in `.editorconfig`.
- All code is written as ES modules.
  The guide has nothing on `goog.module`, `exports` or other module systems.

## Table of contents

[TOC]

## Source files

### File names

File names are all lowercase and may include underscores (`_`) or dashes (`-`), but no other punctuation.
Follow the convention that your project uses.
JavaScript files have the extension `.js`.

### File encoding: UTF-8

Source files are encoded in UTF-8.

### Special characters

#### Whitespace characters

Outside of line breaks, the only whitespace character in a source file is the ASCII space (0x20).
This has two consequences:

- Tabs are never used for indentation.
- A whitespace character other than a space inside a string literal is written as an escape sequence.

#### Escape sequences

If a character has a short escape sequence (`\'`, `\"`, `\\`, `\b`, `\f`, `\n`, `\r`, `\t` or `\v`), use it instead of a numeric escape such as `\x0a`, `\u000a` or `\u{a}`.
Never use legacy octal escapes.

#### Non-ASCII characters

For any other non-ASCII character, write the character itself or a Unicode escape, whichever is easier to read.
A printable character needs no escape.
Escape characters that are invisible or easy to mistake for another one, and add a comment that says what the escape is.

```javascript
// Good: the symbol is printable and speaks for itself.
const currency = '€';

// Allowed, but the escape only makes the line harder to read.
const currency = '€';

// Good: a zero-width space cannot be seen, so it is escaped and explained.
const separator = 'a​b'; // Zero-width space between the letters.
```

## Source file structure

Write new files as ES modules, which use `import` and `export`.

A file has these parts, in this order:

1. License or copyright information, if the file needs it
1. `import` statements
1. The implementation

Separate the parts that are present with one blank line.
Before the implementation, one or two blank lines are fine.

### License or copyright information

If a file carries a license or copyright notice, it comes first in the file.

### ES modules

#### Imports

Never wrap an `import` statement.
It is exempt from the 80 column limit, because a wrapped import is harder to search for.

##### Import paths

Use `import` to load an ES module, and never `require()`.
Always write the `.js` extension in the path.
Import each file once, in a single statement, so that a reader finds everything the file depends on in one place.

```javascript
import './polyfills.js';

import * as config from '../config.js';

import {render} from './render.js';
```

##### Naming imports

A namespace import (`import * as name`) is named in lowerCamelCase after the file that it imports.

```javascript
import * as userStore from './user-store.js';
import * as retryPolicy from './retry_policy.js';
import * as httpclient from './httpclient.js';

import * as dateUtil from './date/util.js';
import * as stringUtil from './string/util.js';
```

A library may be better known under a name that breaks this rule.
Use the well-known name in that case, for example `THREE` for three.js.

Name a default import after the file as well, in the case that fits what the import is.

```javascript
import Logger from './logger.js';
import parseArgs from './parse_args.js';
import DEFAULT_PORT from './defaultport.js';
```

Keep the original name of a named import (`import {name}`), and do not alias it.
When two modules export the same name, import the modules as namespaces, or rename one of the exports.

```javascript
import * as csvReader from './csvreader.js';
import * as jsonReader from './jsonreader.js';

csvReader.open(path);
jsonReader.open(path);
```

If an alias cannot be avoided, build it from the name of the module or its path.

```javascript
import {open as openCsv} from './csvreader.js';
import {open as openJson} from './jsonreader.js';

openCsv(path);
openJson(path);
```

#### Exports

Export only what other modules need.
Do not mark the rest as private, because leaving it out of the exports already does that.
The order of exported and local declarations is up to you.

Use named exports only.
You can put `export` in front of a declaration, or list the names in an `export {name};` statement.

Default exports are not allowed.
Every importing file picks its own name for a default export, and the names drift apart across the code base.

```javascript
// Bad: a default export.
export default class Cache {}

// Good: a named export.
export class Cache {}

// Good: a list of exports.
class Cache {}
export {Cache};
```

A module does not change an exported variable after it is initialized.
If other code must be able to change a value, keep the value inside the module and export a function that changes it.
You can also export a constant reference to an object whose fields change.

```javascript
// Good: the counter is local, and the module controls how it changes.
let count = 0;

export function getCount() {
    return count;
}

export function increment() {
    count += 1;
}
```

```javascript
// Bad: importers see a value that the module may change at any time.
export let count = 0;
```

Never wrap an `export ... from` statement.
Like an import, it is exempt from the column limit.

```javascript
export {parse} from './parser.js';
export * from './tokens.js';
```

Do not let modules depend on each other in a cycle, even though the language permits it.
Both `import` and `export ... from` can close a cycle.

```javascript
// a.js imports b.js, and b.js imports a.js: a cycle.
import './b.js';

// c.js re-exports from d.js, and d.js imports c.js: also a cycle.
export {value} from './d.js';
```

After the imports comes the implementation, with at least one blank line in between.
It holds the declarations of the module, such as constants, variables, classes and functions, whether they are exported or not.

## Formatting

**Terminology note**: A block-like construct is the body of a class, a function, a method or any other pair of braces.
You may treat an array literal or an object literal as a block-like construct.

### Braces

Use braces for every control structure (`if`, `else`, `for`, `do`, `while` and the others), even if the body is one statement.
The body starts on a new line.

Braces on non-empty blocks and block-like constructs follow the K&R style:

- The opening brace stays on the line of its statement.
- A line break follows the opening brace.
- A line break precedes the closing brace.
- A line break follows the closing brace when it ends a statement, or the body of a function, a class or a method.
  No line break follows it when the next token is `else`, `catch`, `while`, a comma, a semicolon or a closing parenthesis.

```javascript
class Queue {
    push(item) {
        if (this.isFull()) {
            try {
                this.grow();
            } catch (error) {
                this.reject(item);
            }
        } else {
            this.items.push(item);
        }
    }
}
```

An empty block may be written as `{}`, with nothing between the braces.
The exception is a statement with several blocks, such as `if`/`else` or `try`/`catch`/`finally`, where the empty block gets its own lines.

```javascript
function noop() {}
```

### Block indentation: +4 spaces

Every new block or block-like construct indents its content by four spaces.
The indentation goes back when the block ends.
Comments are indented like the code around them.

An array literal may be formatted like a block-like construct.
All of these are valid:

```javascript
const primes = [
    2,
    3,
    5,
];

const evens =
        [2, 4, 6];
const odds = [1, 3, 5];

register(name, [
    'read', 'write',
], options);
```

Choose a layout that groups related elements.
Do not choose one only to save lines in a long array.

The same holds for an object literal:

```javascript
const point = {
    x: 1,
    y: 2,
};

const origin =
        {x: 0, y: 0};
const unit = {x: 1, y: 1};

draw(canvas, {
    x: 1, y: 2,
}, style);
```

A class body is indented like any other block.
Do not put a semicolon after a method or after the closing brace of a class declaration.
A statement that contains a class expression, such as an assignment, still ends with a semicolon.

```javascript
class Shape {
    constructor(name) {
        this.name = name;
    }
}

class Circle extends Shape {
    constructor(radius) {
        super('circle');
        this.radius = radius;
    }
}

const Square = class extends Shape {
    area() {
        return this.side ** 2;
    }
};
```

The body of a function that is passed as an argument is indented by four spaces relative to the line where the call starts.

```javascript
items.forEach((item) => {
    // Four spaces deeper than `items`.
    if (item.isReady()) {
        process(item);
    } else {
        skip(item);
    }
});

fetchUsers(query)
        .then(filterActive)
        .then((users) => {
            // Four spaces deeper than `.then(`.
            for (const user of users) {
                greet(user);
            }
        });
```

The content of a `switch` is indented by four spaces, and so is the content of each `case` and `default` group.
The next label returns to the indentation of the previous one.
A blank line between a `break` and the next `case` is optional.
You may wrap the group in braces when a declaration needs its own scope.

```javascript
switch (command) {
    case Command.START:
        start();
        break;

    case Command.STOP:
        stop();
        break;

    default:
        throw new Error(`Unknown command: ${command}`);
}
```

### Statements

#### One statement per line

Put every statement on a line of its own.

#### Semicolons are required

End every statement with a semicolon.
Do not rely on automatic semicolon insertion.

### Column limit: 80

A line of code has at most 80 characters.
Wrap a longer line as described in [Line-wrapping](#line-wrapping).
The exceptions are `import` and `export ... from` statements, long URLs and long shell commands in comments, and lines that cannot be wrapped.

### Line-wrapping

**Terminology note**: Line-wrapping is splitting code that would fit on one line over several lines because it is too long for the column limit.

No formula gives the right wrapping for every case, and the same code can often be wrapped well in several ways.
A formatter makes these choices for you, so prefer to use one.

#### Where to break

Break at the highest syntactic level that gets the line short enough.

```javascript
// Good: breaks at the assignment.
const averageResponseTime =
        totalResponseTime / numberOfResponses;

// Bad: breaks inside the call and leaves the reader to find the end.
const averageResponseTime = computeAverage(totalResponseTime,
        numberOfResponses);
```

When the code is broken at an operator, the operator ends the line, not the next one.
This differs from Google's Java style.
The dot of a member access is not an operator, so it starts the continuation line.

These rules apply as well:

- The name of a function or constructor stays on the same line as its opening parenthesis.
- A comma stays on the line of the token before it.
- Never break between `return` and the returned value, as this changes the meaning of the code.

#### Indent continuation lines at least +8 spaces

A continuation line is indented by at least eight spaces relative to the first line.
Block indentation takes precedence where it applies.

If there are several continuation lines, you can indent them further.
Use multiples of four for each deeper syntactic level.
Two lines have the same indentation only if they start with parallel elements.

### Whitespace

#### Vertical whitespace

Use a single blank line:

1. Between two methods of a class or an object literal.
   A blank line between plain properties of an object literal is optional, and groups them.
1. Inside a function body, to separate groups of statements.
   Do this sparingly, and never at the start or the end of a body.
1. Before the first or after the last method of a class or object literal, if you like.
   Neither is encouraged or discouraged.
1. Where another section of this guide asks for one, such as around imports.

Several blank lines in a row are allowed, but never required.

#### Horizontal whitespace

Trailing whitespace is forbidden.
Indentation is covered in [Block indentation: +4 spaces](#block-indentation-4-spaces).

Beyond what the language requires, and apart from literals and comments, put a single space in these places and nowhere else:

1. Between a keyword such as `if`, `for` or `catch` and the parenthesis after it.
   `function` and `super` are the exceptions.
1. Between a closing brace and a keyword such as `else` or `catch` after it.
1. Before an opening brace, except when:
    - The brace opens an object literal that is the first argument of a call or the first element of an array, as in `foo({a: [{b: c}]})`.
    - The brace follows `$` in a template literal, where a space is a syntax error.
1. On both sides of a binary or ternary operator.
1. After a comma or a semicolon, and never before them.
1. After the colon in an object literal.
1. On both sides of the `//` that starts a comment at the end of a line.
   More than one space is fine.
1. Inside block comments that sit in code, such as a comment with a parameter name: `connect(host, /* secure= */ true)`.

#### Horizontal alignment: discouraged

**Terminology note**: Horizontal alignment is padding lines with extra spaces so that tokens line up in a column.

Alignment is allowed but discouraged, and you do not have to keep existing alignment.
It makes diffs larger, because adding a longer name means re-padding the other lines.

```javascript
// Good:
const sizes = {
    small: 8,
    medium: 16,
    extraLarge: 32,
};

// Allowed, but discouraged:
const sizes = {
    small:      8,
    medium:     16,
    extraLarge: 32,
};
```

#### Function arguments

Keep the arguments on the line of the function name when they fit.
When they do not, wrap them so that they stay readable.
Continuation lines are indented by eight spaces.
Lining them up with the opening parenthesis is allowed but discouraged.

These are the usual patterns:

```javascript
// The arguments fit on one continuation line.
const total = addAll(
        firstDescriptiveValue, secondDescriptiveValue, thirdDescriptiveValue);

// Many arguments: fill each line up to the limit.
const total = addAll(firstDescriptiveValue, secondDescriptiveValue,
        thirdDescriptiveValue, fourthDescriptiveValue, fifthDescriptiveValue);

// One argument per line puts the emphasis on each of them.
const total = addAll(
        firstDescriptiveValue,
        secondDescriptiveValue,
        thirdDescriptiveValue,
        fourthDescriptiveValue);
```

The first pattern is the one to prefer.
It survives a rename of the function and uses little space.
Filling lines to the limit saves lines, but it hides where each argument starts, so use it with care.

### Grouping parentheses: recommended

Leave out optional parentheses only if both the author and the reviewer agree that nobody can misread the expression without them.
Do not expect readers to know the whole precedence table.

Do not wrap the whole operand of `delete`, `typeof`, `void`, `return`, `throw`, `case`, `in`, `of` or `yield` in parentheses.

### Comments

#### Block comment style

A block comment has the indentation of the code around it.
It can use `/* ... */` or consecutive `//` lines.
In a `/* ... */` comment, each line after the first starts with an asterisk that lines up with the first one.

Do not draw boxes around comments with asterisks or other characters.

```javascript
/*
 * A comment on
 * several lines.
 */

// Or the same
// with slashes.

/* A short one. */
```

#### Parameter name comments

Add a comment with the parameter name when the argument alone does not say what it means and renaming or restructuring the function is not an option.
Put the comment before the value and end the name with `=`.

```javascript
connect(host, /* timeoutSeconds= */ 30, /* secure= */ true);
```

To match the code around it, you may write the comment after the value, without the `=`.

```javascript
connect(host, 30 /* timeoutSeconds */, true /* secure */);
```

## Language features

JavaScript has a number of features that are confusing or dangerous.
This section lists which of them you can use and under which conditions.

A feature that this guide does not mention is allowed without further rules.

### Local variable declarations

Declare local variables with `const` or `let`, and never with `var`.
Use `const` unless the variable is reassigned.
Declare one variable per statement, so `let a = 1, b = 2;` is not allowed.

### Array literals

Put a trailing comma after the last element when the closing bracket is on its own line.

```javascript
const weekend = [
    'saturday',
    'sunday',
];
```

Do not call the `Array` constructor with elements.
Its meaning depends on the number and the type of the arguments, so a change to the arguments can silently change what it does.
With a single numeric argument it creates an empty array of that length, and with a non-integer number it throws.

```javascript
// Bad:
const none = new Array();
const one = new Array(item);
const two = new Array(first, second);

// Good:
const none = [];
const one = [item];
const two = [first, second];
```

Creating an array with a fixed length by `new Array(length)` is fine when that is what you want.

Do not add properties to an array other than its elements and `length`.
Use a `Map` or an object for named values.

### Object literals

Put a trailing comma after the last property when the closing brace is on its own line.

Do not call the `Object` constructor, because the literal does the same and is shorter.
Use `{}` or `{a: 1, b: 2}`.

### Method shorthand

In an object literal, write a method with the shorthand `name() {...}` rather than `name: function() {...}` or `name: () => {...}`.

```javascript
const counter = {
    value: 0,
    next() {
        this.value += 1;
        return this.value;
    },
};
```

In a shorthand method, and in a `function`, `this` is the object literal.
In an arrow function, `this` is whatever it was outside of the literal.

```javascript
class Widget {
    describe() {
        this.label = 'widget';
        return {
            label: 'object',
            // `this.label` here is 'widget', the label of the Widget.
            getLabel: () => this.label,
        };
    }
}
```

### Classes

A class does not need a constructor.
In a subclass, call `super()` before anything that sets a field or reads `this`.

### Functions

Declare a top-level function in one of two ways.
Either declare it with `function`, or assign an arrow function to a `const`.
Export it with `export` when other modules use it.

```javascript
export function slugify(text) {
    return text.trim().toLowerCase().replaceAll(' ', '-');
}

const isBlank = (text) => text.trim() === '';
```

#### Arrow functions

Arrow functions are short, and they keep the `this` of the code around them.
Prefer them to `function` expressions for nested functions.
Prefer them to `bind(this)` and to saving `this` in a variable such as `self`.
They are also a good fit for callbacks, because they let you decide which arguments reach the callee, where `bind` forwards all of them.

You may leave out the parentheses around a single parameter that is not destructured.

The body is a block by default.
Use a single expression as the body, which is then returned, in two cases:

- The code needs the value.
- The expression is a call that is preceded by `void`, because `void` makes sure that the function returns `undefined` and no value leaks out.

Prefer the single expression when it is short and simple.

```javascript
// The value is needed.
const total = prices.reduce((sum, price) => sum + price, 0);

// The value is not needed, so `void` drops it.
button.addEventListener('click', () => void save(form));

// A block, because the body has more than a call.
button.addEventListener('click', () => {
    form.disabled = true;
    save(form);
});
```

### String literals

Use single quotes (`'`) for ordinary strings, not double quotes (`"`).
An ordinary string stays on one line.

Do not end a line inside a string with a backslash to continue it on the next line, in an ordinary string or in a template literal.
A space after the backslash breaks the code, and readers do not expect the feature.

#### Template literals

Use a template literal (written with backticks) instead of concatenation when the result is built from several parts.
A template literal may span several lines.
The continuation lines do not need to follow the indentation of the block, because their leading spaces are part of the string.

```javascript
function describe(user) {
    return `${user.name} (${user.email}) joined on ${user.joinedAt}.
They have ${user.posts.length} posts.`;
}
```

### Number literals

Write numbers in decimal, hexadecimal, octal or binary form.
The prefixes are `0x`, `0o` and `0b`, in lowercase.
A number never has a leading zero, unless the zero is part of one of these prefixes.

### Control structures

#### For loops

The language has three kinds of `for` loop, and you can use any of them.
Prefer `for ... of` when it does the job.

#### Exceptions

Use exceptions to report exceptional cases.
Throw `Error` or a subclass of it, create it with `new`, and never throw a string or another value.
A promise is rejected with the same rule, because `Promise.reject(value)` works like `throw value` in an `async` function.

Define your own subclass of `Error` when callers need information that `Error` cannot carry.

Throw an exception instead of using an ad-hoc scheme, such as an out parameter that receives the error or a result object with an `error` field.

#### Switch statements

A `switch` consists of statement groups.
Each group has one or more labels (`case x:` or `default:`) followed by one or more statements.

A group must not run into the next one by accident.
It either ends with `break`, `return` or `throw`, or it has a comment that says it falls through.
Any comment that gets the point across will do, and `// fall through` is the usual one.
The last group does not need such a comment.

```javascript
switch (level) {
    case 0:
    case 1:
        warnLow();
    // fall through
    case 2:
        logLevel(level);
        break;
    default:
        warnUnknown(level);
}
```

Every `switch` has a `default` group, even if it is empty, and it comes last.

### this

Use `this` only in class constructors and methods, and in arrow functions inside them.
You may also use it in a function that is called with an explicit `this`, if a comment documents that.

Never use `this` to refer to the global object, to the context of `eval` or to the target of an event.
Do not use `call()` or `apply()` when there is no need for them.

### Equality checks

Compare with the strict operators `===` and `!==`.

The one exception is a comparison with `null`.
`x == null` is true for both `null` and `undefined`, and false for the other falsy values such as `0` and the empty string.

```javascript
if (value == null) {
    // No value was given: `null` or `undefined`.
}
```

## See also

- [Google JavaScript style guide](https://google.github.io/styleguide/jsguide.html)
- [TypeScript style guide](../typescript/Typescript.md)
- [MDN JavaScript reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference)
