# Javascript Style Guide

A basic javascript style guide, heavily based on the [Google styleguide](https://google.github.io/styleguide/jsguide.html).

## Table of contents

[TOC]

## Source Files

### File name

File names must be all lowercase and may include underscores (_) or dashes (-), but no additional punctuation. Follow the convention that your project uses. Filenames’ extension must be .js.

### File encoding: UTF-8

Source files are encoded in UTF-8.

### Special characters

#### Whitespace characters

Aside from the line terminator sequence, the ASCII horizontal space character (0x20) is the only whitespace character that appears anywhere in a source file. This implies that

- All other whitespace characters in string literals are escaped, and
- Tab characters are not used for indentation.

#### Special escape sequences

For any character that has a special escape sequence `(\', \", \\, \b, \f, \n, \r, \t, \v)`, that sequence is used rather than the corresponding numeric escape (e.g `\x0a`, `\u000a`, or `\u{a}`). Legacy octal escapes are never used.

#### Non-ASCII characters

For the remaining non-ASCII characters, either the actual Unicode character (e.g. ∞) or the equivalent hex or Unicode escape (e.g. `\u221e`) is used, depending only on which makes the code easier to read and understand.

  ```shell
    /* Best: perfectly clear even without a comment. */
    const units = 'μs';

    /* Allowed: but unnecessary as μ is a printable character. */
    const units = '\u03bcs'; // 'μs'

    /* Good: use escapes for non-printable characters with a comment for clarity. */
    return '\ufeff' + content;  // Prepend a byte order mark.
  ```

## Source file structure

All new source files should be a ECMAScript (ES) module (uses import and export statements).

Files consist of the following, in order:

- License or copyright information
- ES import statements
- The file’s implementation
Exactly one blank line separates each section that is present, except the file's implementation, which may be preceded by 1 or 2 blank lines.

### License or copyright information

If license or copyright information belongs in a file, it belongs here.

### ES modules

ES modules are files that use the import and export keywords.

#### Imports

Import statements must not be line wrapped and are therefore an exception to the 80-column limit.

##### Import paths

ES module files must use the import statement to import other ES module files. Do not goog.require another ES module.

  ```shell
  import './sideeffects.js';

  import * as goog from '../closure/goog/goog.js';
  import * as parent from '../parent.js';

  import {name} from './sibling.js';
  ```

  The .js file extension is not optional in import paths and must always be included.
  
  Do not import the same file multiple times. This can make it hard to determine the aggregate imports of a file.

##### Naming imports

Module import names (`import * as name`) are lowerCamelCase names that are derived from the imported file name.

  ```shell
  import * as fileOne from '../file-one.js';
  import * as fileTwo from '../file_two.js';
  import * as fileThree from '../filethree.js';

  import * as libString from './lib/string.js';
  import * as math from './math/math.js';
  import * as vectorMath from './vector/math.js';
  ```

Some libraries might commonly use a namespace import prefix that violates this naming scheme, but overbearingly common open source use makes the violating style more readable. The only library that currently falls under this exception is threejs, using the THREE prefix.

Default import names are derived from the imported file name.

  ```shell
  import MyClass from '../my-class.js';
  import myFunction from '../my_function.js';
  import SOME_CONSTANT from '../someconstant.js';
  ```

In general symbols imported via the named import (`import {name}`) should keep the same name. Avoid aliasing imports (`import {SomeThing as SomeOtherThing}`). Prefer fixing name collisions by using a module `import (import *)` or renaming the exports themselves.

  ```shell
  import * as bigAnimals from './biganimals.js';
  import * as domesticatedAnimals from './domesticatedanimals.js';

  new bigAnimals.Cat();
  new domesticatedAnimals.Cat();
  ```

If renaming a named import is needed then use components of the imported module's file name or path in the resulting alias

  ```shell
  import {Cat as BigCat} from './biganimals.js';
  import {Cat as DomesticatedCat} from './domesticatedanimals.js';

  new BigCat();
  new DomesticatedCat();
  ```

#### Exports

Symbols are only exported if they are meant to be used outside the module. Non-exported module-local symbols are not declared `@private`. There is no prescribed ordering for exported and module-local symbols.
Use named exports in all code. You can apply the export keyword to a declaration, or use the `export {name};` syntax.

Do not use default exports. Importing modules must give a name to these values, which can lead to inconsistencies in naming across modules.

  ```shell
  // Do not use default exports:
  export default class Foo { ... } // BAD!
  
  // Use named exports:
  export class Foo { ... }
  
  // Alternate style named exports:
  class Foo { ... }
  export {Foo};
  ```

Exported variables must not be mutated outside of module initialization.

There are alternatives if mutation is needed, including exporting a constant reference to an object that has mutable fields or exporting accessor functions for mutable data.

  ```shell
  // Good: Rather than export the mutable variables foo and mutateFoo directly,
  // instead make them module scoped and export a getter for foo and a wrapper for
  // mutateFooFunc.
  let /** number */ foo = 0;
  let /** function(number): number */ mutateFooFunc = (foo) => foo + 1;

  /** @return {number} */
  export function getFoo() {
    return foo;
  }

  export function mutateFoo() {
    foo = mutateFooFunc(foo);
  }

  /** @param {function(number): number} mutateFoo */
  export function setMutateFoo(mutateFoo) {
    mutateFooFunc = mutateFoo;
  }
  ```

export from statements must not be line wrapped and are therefore an exception to the 80-column limit. This applies to both export from flavors.

  ```shell
  export {specificName} from './other.js';
  export * from './another.js';
  ```

Do not create cycles between ES modules, even though the ECMAScript specification allows this. Note that it is possible to create cycles with both the import and export statements.

  ```shell
  // a.js
  import './b.js';
  
  // b.js
  import './a.js';


  // `export from` can cause circular dependencies too!
  export {x} from './c.js';

  // c.js
  import './b.js';
  export let x;
  ```

The actual implementation follows after all dependency information is declared (separated by at least one blank line).

This may consist of any module-local declarations (constants, variables, classes, functions, etc), as well as any exported symbols.

## Formatting

Terminology Note: block-like construct refers to the body of a class, function, method, or brace-delimited block of code. Any array or object literal may optionally be treated as if it were a block-like construct.

### Braces

Braces are required for all control structures (i.e. if, else, for, do, while, as well as any others), even if the body contains only a single statement. The first statement of a non-empty block must begin on its own line.

Braces follow the Kernighan and Ritchie style [Egyptian brackets](https://blog.codinghorror.com/new-programming-jargon/#3) for nonempty blocks and block-like constructs:

- No line break before the opening brace.
- Line break after the opening brace.
- Line break before the closing brace.
- Line break after the closing brace if that brace terminates a statement or the body of a function or class statement, or a class method. Specifically, there is no line break after the brace if it is followed by else, catch, while, or a comma, semicolon, or right-parenthesis.

Example:

  ```shell
  class InnerClass {
    constructor() {}

    /** @param {number} foo */
    method(foo) {
      if (condition(foo)) {
        try {
          // Note: this might fail.
          something();
        } catch (err) {
          recover();
        }
      }
    }
  }
  ```

An empty block or block-like construct may be closed immediately after it is opened, with no characters, space, or line break in between (i.e. {}), unless it is a part of a multi-block statement (one that directly contains multiple blocks: `if/else` or `try/catch/finally`).

Example:

  ```shell
  function doNothing() {}
  ```

### Block indentation: +4 spaces

Each time a new block or block-like construct is opened, the indent increases by two spaces. When the block ends, the indent returns to the previous indent level. The indent level applies to both code and comments throughout the block.
Any array literal may optionally be formatted as if it were a “block-like construct.” For example, the following are all valid (not an exhaustive list):

  ```shell
  const a = [
    0,
    1,
    2,
  ];

  const b =
    [0, 1, 2];
  const c = [0, 1, 2];

  someMethod(foo, [
    0, 1, 2,
  ], bar);
  ```

Other combinations are allowed, particularly when emphasizing semantic groupings between elements, but should not be used only to reduce the vertical size of larger arrays.

Any object literal may optionally be formatted as if it were a “block-like construct.” The same examples apply as Array literals: optionally block-like. For example, the following are all valid (not an exhaustive list):

  ```shell
  const a = {
    a: 0,
    b: 1,
  };

  const b =
    {a: 0, b: 1};
  const c = {a: 0, b: 1};

  someMethod(foo, {
    a: 0, b: 1,
  }, bar);
  ```

Class literals (whether declarations or expressions) are indented as blocks. Do not add semicolons after methods, or after the closing brace of a class declaration (statements—such as assignments—that contain class expressions are still terminated with a semicolon). For inheritance, the extends keyword is sufficient unless the superclass is templatized.

Example:

  ```shell
  /** @template T */
  class Foo {
    /** @param {T} x */
    constructor(x) {
      /** @type {T} */
      this.x = x;
    }
  }

  /** @extends {Foo<number>} */
  class Bar extends Foo {
    constructor() {
      super(42);
    }
  }

  exports.Baz = class extends Bar {
    /** @return {number} */
    method() {
      return this.x;
    }
  };
  ```

When declaring an anonymous function in the list of arguments for a function call, the body of the function is indented four spaces more than the preceding indentation depth.

Example:

  ```shell
  prefix.something.reallyLongFunctionName('whatever', (a1, a2) => {
    // Indent the function body +2 relative to indentation depth
    // of the 'prefix' statement one line above.
    if (a1.equals(a2)) {
      someOtherLongFunctionName(a1);
    } else {
      andNowForSomethingCompletelyDifferent(a2.parrot);
    }
  });

  some.reallyLongFunctionCall(arg1, arg2, arg3)
    .thatsWrapped()
    .then((result) => {
      // Indent the function body +2 relative to the indentation depth
      // of the '.then()' call.
      if (result) {
        result.use();
      }
    });
  ```

As with any other block, the contents of a switch block are indented +4.

After a switch label, a newline appears, and the indentation level is increased +4, exactly as if a block were being opened. An explicit block may be used if required by lexical scoping. The following switch label returns to the previous indentation level, as if a block had been closed.

A blank line is optional between a break and the following case.

Example:

  ```shell
  switch (animal) {
    case Animal.BANDERSNATCH:
      handleBandersnatch();
      break;

    case Animal.JABBERWOCK:
      handleJabberwock();
      break;

    default:
      throw new Error('Unknown animal');
  }
  ```

### Statements

#### One statement per line

Each statement is followed by a line-break.

#### Semicolons are required

Every statement must be terminated with a semicolon. Relying on automatic semicolon insertion is forbidden.

### Column limit: 80

JavaScript code has a column limit of 80 characters. Except as noted below, any line that would exceed this limit must be line-wrapped, as explained in Line-wrapping.

### Line-wrapping

**Terminology Note**: Line wrapping is breaking a chunk of code into multiple lines to obey column limit, where the chunk could otherwise legally fit in a single line.

There is no comprehensive, deterministic formula showing exactly how to line-wrap in every situation. Very often there are several valid ways to line-wrap the same piece of code.

#### Where to break

The prime directive of line-wrapping is: prefer to break at a higher syntactic level.

  ```shell
  // Preferred: 
  currentEstimate =
    calc(currentEstimate + x * currentEstimate) /
        2.0;
  
  // Discouraged:
  currentEstimate = calc(currentEstimate + x *
    currentEstimate) / 2.0;
  ```

In the preceding example, the syntactic levels from highest to lowest are as follows: assignment, division, function call, parameters, number constant.

Operators are wrapped as follows:

1. When a line is broken at an operator the break comes after the symbol. (Note that this is not the same practice used in Google style for Java.) This does not apply to the dot (.), which is not actually an operator.
2. A method or constructor name stays attached to the open parenthesis (() that follows it.
3. A comma (,) stays attached to the token that precedes it.
4. A line break is never added between a return and the return value as this would change the meaning of the code.
5. JSDoc annotations with type names break after {. This is necessary as annotations with optional types (@const, @private, @param, etc) do not scan the next line.

#### Indent continuation lines at least +4 spaces

When line-wrapping, each line after the first (each continuation line) is indented at least +4 from the original line, unless it falls under the rules of block indentation.

When there are multiple continuation lines, indentation may be varied beyond +4 as appropriate. In general, continuation lines at a deeper syntactic level are indented by larger multiples of 4, and two lines use the same indentation level if and only if they begin with syntactically parallel elements.

### Whitespace

#### Vertical whitespace

A single blank line appears:

1. Between consecutive methods in a class or object literal
Exception: A blank line between two consecutive properties definitions in an object literal (with no other code between them) is optional. Such blank lines are used as needed to create logical groupings of fields.
2. Within method bodies, sparingly to create logical groupings of statements. Blank lines at the start or end of a function body are not allowed.
3. Optionally before the first or after the last method in a class or object literal (neither encouraged nor discouraged).
4. As required by other sections of this document (e.g. 3.6 goog.require and goog.requireType statements).

Multiple consecutive blank lines are permitted, but never required (nor encouraged).

#### Horizontal whitespace

Use of horizontal whitespace depends on location, and falls into three broad categories: leading (at the start of a line), trailing (at the end of a line), and internal. Leading whitespace (i.e., indentation) is addressed elsewhere. Trailing whitespace is forbidden.

Beyond where required by the language or other style rules, and apart from literals, comments, and JSDoc, a single internal ASCII space also appears in the following places only.

1. Separating any reserved word (such as if, for, or catch) except for function and super, from an open parenthesis (() that follows it on that line.
2. Separating any reserved word (such as else or catch) from a closing curly brace (}) that precedes it on that line.
3. Before any open curly brace ({), with two exceptions:
    - Before an object literal that is the first argument of a function or the first element in an array literal (e.g. foo({a: [{c: d}]})).
    - In a template expansion, as it is forbidden by the language (e.g. valid: `ab${1 + 2}cd`, invalid: `xy$ {3}z`).
4. On both sides of any binary or ternary operator.
5. After a comma (`,`) or semicolon (`;`). Note that spaces are never allowed before these characters.
6. After the colon (`:`) in an object literal.
7. On both sides of the double slash (`//`) that begins an end-of-line comment. Here, multiple spaces are allowed, but not required.
8. After an open-block comment character and on both sides of close characters (e.g. for short-form type declarations, casts, and parameter name comments: `this.foo = /** @type {number} \*/ (bar);` or `function(/** string \*/ foo) {;` or `baz(/* buzz= */ true))`.

#### Horizontal alignment: discouraged

**Terminology Note**: Horizontal alignment is the practice of adding a variable number of additional spaces in your code with the goal of making certain tokens appear directly below certain other tokens on previous lines.

This practice is permitted, but it is generally discouraged. It is not even required to maintain horizontal alignment in places where it was already used.

Here is an example without alignment, followed by one with alignment. Both are allowed, but the latter is discouraged:

  ```shell
  {
    tiny: 42, // this is great
    longer: 435, // this too
  };

  {
    tiny:   42,  // permitted, but future edits
    longer: 435, // may leave it unaligned
  };
  ```

#### Function arguments

Prefer to put all function arguments on the same line as the function name. If doing so would exceed the 80-column limit, the arguments must be line-wrapped in a readable way. To save space, you may wrap as close to 80 as possible, or put each argument on its own line to enhance readability. Indentation should be four spaces. Aligning to the parenthesis is allowed, but discouraged. Below are the most common patterns for argument wrapping:

  ```shell
  // Arguments start on a new line, indented four spaces. Preferred when the
  // arguments don't fit on the same line with the function name (or the keyword
  // "function") but fit entirely on the second line. Works with very long
  // function names, survives renaming without reindenting, low on space.
  doSomething(
      descriptiveArgumentOne, descriptiveArgumentTwo, descriptiveArgumentThree) {
    // …
  }

  // If the argument list is longer, wrap at 80. Uses less vertical space,
  // but violates the rectangle rule and is thus not recommended.
  doSomething(veryDescriptiveArgumentNumberOne, veryDescriptiveArgumentTwo,
      tableModelEventHandlerProxy, artichokeDescriptorAdapterIterator) {
    // …
  }

  // Four-space, one argument per line.  Works with long function names,
  // survives renaming, and emphasizes each argument.
  doSomething(
      veryDescriptiveArgumentNumberOne,
      veryDescriptiveArgumentTwo,
      tableModelEventHandlerProxy,
      artichokeDescriptorAdapterIterator) {
    // …
  }
  ```

### Grouping parentheses: recommended

Optional grouping parentheses are omitted only when the author and reviewer agree that there is no reasonable chance that the code will be misinterpreted without them, nor would they have made the code easier to read. It is not reasonable to assume that every reader has the entire operator precedence table memorized.

Do not use unnecessary parentheses around the entire expression following `delete, typeof, void, return, throw, case, in, of, or yield`.

Parentheses are required for type casts: `/** @type {!Foo} */ (foo)`.

### Comments

#### Block comment style

Block comments are indented at the same level as the surrounding code. They may be in `/* … */` or `//`-style. For multi-line `/* … */` comments, subsequent lines must start with `*` aligned with the `*` on the previous line, to make comments obvious with no extra context.

  ```shell
  /*
   * This is
   * okay.
   */

  // And so
  // is this.

  /* This is fine, too. */
  ```

Comments are not enclosed in boxes drawn with asterisks or other characters.

#### Parameter Name Comments

“Parameter name” comments should be used whenever the value and method name do not sufficiently convey the meaning, and refactoring the method to be clearer is infeasible . Their preferred format is before the value with "=":

  ```shell
  someFunction(obviousParam, /* shouldRender= */ true, /* name= */ 'hello');
  ```

For consistency with surrounding code you may put them after the value without "=":

  ```shell
  someFunction(obviousParam, true /* shouldRender */, 'hello' /* name */);
  ```

## Language features

JavaScript includes many dubious (and even dangerous) features. This section delineates which features may or may not be used, and any additional constraints on their use.

Language features which are not discussed in this style guide may be used with no recommendations of their usage.

### Local variable declarations

Declare all local variables with either const or let. Use const by default, unless a variable needs to be reassigned. The var keyword must not be used. Every local variable declaration declares only one variable: declarations such as `let a = 1, b = 2;` are not used.

### Array literals

Include a trailing comma whenever there is a line break between the final element and the closing bracket.

Example:

  ```shell
  const values = [
    'first value',
    'second value',
  ];
  ```

Do not use the variadic Array constructor
The constructor is error-prone if arguments are added or removed. Use a literal instead.

Disallowed:

  ```shell
  const a1 = new Array(x1, x2, x3);
  const a2 = new Array(x1, x2);
  const a3 = new Array(x1);
  const a4 = new Array();
  ```

This works as expected except for the third case: if x1 is a whole number then a3 is an array of size x1 where all elements are undefined. If x1 is any other number, then an exception will be thrown, and if it is anything else then it will be a single-element array.

Instead, write:

  ```shell
  const a1 = [x1, x2, x3];
  const a2 = [x1, x2];
  const a3 = [x1];
  const a4 = [];
  ```

Explicitly allocating an array of a given length using new Array(length) is allowed when appropriate.
Do not define or use non-numeric properties on an array (other than length). Use a Map (or Object) instead.

## Object literals

Include a trailing comma whenever there is a line break between the final property and the closing brace.
While `Object` does not have the same problems as `Array`, it is still disallowed for consistency. Use an object literal `({} or {a: 0, b: 1, c: 2})` instead.

### Method shorthand

Methods can be defined on object literals using the method shorthand ({method() {… }}) in place of a colon immediately followed by a function or arrow function literal.

Example:

  ```shell
  return {
    stuff: 'candy',
    method() {
      return this.stuff;  // Returns 'candy'
    },
  };
  ```

Note that `this` in a method shorthand or `function` refers to the object literal itself whereas `this` in an arrow function refers to the scope outside the object literal.

Example:

  ```shell
  class {
    getObjectLiteral() {
      this.stuff = 'fruit';
      return {
        stuff: 'candy',
        method: () => this.stuff,  // Returns 'fruit'
      };
    }
  }
  ```

### Classes

Constructors are optional. Subclass constructors must call `super()` before setting any fields or otherwise accessing `this`. Interfaces should declare non-method properties in the constructor.

### Functions

Top-level functions may be defined directly on the `exports` object, or else declared locally and optionally exported.

Examples:

  ```shell
  /** @param {string} str */
  exports.processString = (str) => {
    // Process the string.
  };

  /** @param {string} str */
  const processString = (str) => {
    // Process the string.
  };

  exports = {processString};
  ```

#### Arrow functions

Arrow functions provide a concise function syntax and simplify scoping `this` for nested functions. Prefer arrow functions over the function keyword for nested functions
Prefer arrow functions over other `this` scoping approaches such as `f.bind(this)` and `const self = this`. Arrow functions are particularly useful for calling into callbacks as they permit explicitly specifying which parameters to pass to the callback whereas binding will blindly pass along all parameters.
The left-hand side of the arrow contains zero or more parameters. Parentheses around the parameters are optional if there is only a single non-destructured parameter. When parentheses are used, inline parameter types may be specified.
The right-hand side of the arrow contains the body of the function. By default the body is a block statement (zero or more statements surrounded by curly braces). The body may also be an implicitly returned single expression if either: the program logic requires returning a value, or the `void` operator precedes a single function or method call (using `void` ensures `undefined` is returned, prevents leaking values, and communicates intent). The single expression form is preferred if it improves readability (e.g., for short or simple expressions).

Examples:

  ```shell
  /**
  * Arrow functions can be documented just like normal functions.
  * @param {number} numParam A number to add.
  * @param {string} strParam Another number to add that happens to be a string.
  * @return {number} The sum of the two parameters.
  */
  const moduleLocalFunc = (numParam, strParam) => numParam + Number(strParam);

  // Uses the single expression syntax with `void` because the program logic does
  // not require returning a value.
  getValue((result) => void alert(`Got ${result}`));

  class CallbackExample {
    constructor() {
      /** @private {number} */
      this.cachedValue_ = 0;

      // For inline callbacks, you can use inline typing for parameters.
      // Uses a block statement because the value of the single expression should
      // not be returned and the expression is not a single function call.
      getNullableValue((/** ?number */ result) => {
        this.cachedValue_ = result == null ? 0 : result;
      });
    }
  }
  ```

### String literals

Ordinary string literals are delimited with single quotes (`'`), rather than double quotes (`"`).
Ordinary string literals may not span multiple lines.
Do not use line continuations (that is, ending a line inside a string literal with a backslash) in either ordinary or template string literals. Even though ES5 allows this, it can lead to tricky errors if any trailing whitespace comes after the slash, and is less obvious to readers.

#### Template literals

Use template literals (delimited with `) over complex string concatenation, particularly if multiple string literals are involved. Template literals may span multiple lines.
If a template literal spans multiple lines, it does not need to follow the indentation of the enclosing block, though it may if the added whitespace does not matter.

Example:

  ```shell
  function arithmetic(a, b) {
    return `Here is a table of arithmetic operations:
  ${a} + ${b} = ${a + b}
  ${a} - ${b} = ${a - b}
  ${a} * ${b} = ${a * b}
  ${a} / ${b} = ${a / b}`;
  }
  ```
  
### Number literals

Numbers may be specified in decimal, hex, octal, or binary. Use exactly `0x`, `0o`, and `0b` prefixes, with lowercase letters, for hex, octal, and binary, respectively. Never include a leading zero unless it is immediately followed by `x`, `o`, or `b`.

### Control structures

#### For loops

With ES6, the language now has three different kinds of for loops. All may be used, though `for-of` loops should be preferred when possible.

#### Exceptions

Exceptions are an important part of the language and should be used whenever exceptional cases occur. Always throw `Errors` or subclasses of `Error:` never throw string literals or other objects. Always use `new` when constructing an `Error`.
This treatment extends to `Promise` rejection values as `Promise.reject(obj)` is equivalent to `throw obj;` in async functions.
Custom exceptions provide a great way to convey additional error information from functions. They should be defined and used wherever the native `Error` type is insufficient.
Prefer throwing exceptions over ad-hoc error-handling approaches (such as passing an error container reference type, or returning an object with an error property).

#### Switch statements

Each statement group consists of one or more switch labels (either `case FOO:` or `default:`), followed by one or more statements.
Within a switch block, each statement group either terminates abruptly (with a `break`, `return` or `throw` exception), or is marked with a comment to indicate that execution will or might continue into the next statement group. Any comment that communicates the idea of fall-through is sufficient (typically `// fall through`). This special comment is not required in the last statement group of the switch block.

Example:

  ```shell
  switch (input) {
    case 1:
    case 2:
      prepareOneOrTwo();
    // fall through
    case 3:
      handleOneTwoOrThree();
      break;
    default:
      handleLargeNumber(input);
  }
  ```

Each switch statement includes a `default` statement group, even if it contains no code. The `default` statement group must be last.

### this

Only use `this` in class constructors and methods, in arrow functions defined within class constructors and methods, or in functions that have an explicit `@this` declared in the immediately-enclosing function’s JSDoc.

Never use `this` to refer to the global object, the context of an `eval`, the target of an event, or unnecessarily `call()` or `apply()` functions.

### Equality Checks

Use identity operators (`===`/`!==`) except in the cases documented below.
Catching both null and undefined values:

  ```shell
  if (someObjectOrPrimitive == null) {
    // Checking for null catches both null and undefined for objects and
    // primitives, but does not catch other falsy values like 0 or the empty
    // string.
  }
  ```
