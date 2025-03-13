# Javascript Style Guide
A basic javascript style guide, heavily based on the [Google styleguide](https://google.github.io/styleguide/jsguide.html).

# Table of contents
[TOC]

# Source Files
## File name
File names must be all lowercase and may include underscores (_) or dashes (-), but no additional punctuation. Follow the convention that your project uses. Filenames’ extension must be .js.

## File encoding: UTF-8
Source files are encoded in UTF-8.

## Special characters

### Whitespace characters
Aside from the line terminator sequence, the ASCII horizontal space character (0x20) is the only whitespace character that appears anywhere in a source file. This implies that
- All other whitespace characters in string literals are escaped, and
- Tab characters are not used for indentation.

### Special escape sequences
For any character that has a special escape sequence (\', \", \\, \b, \f, \n, \r, \t, \v), that sequence is used rather than the corresponding numeric escape (e.g \x0a, \u000a, or \u{a}). Legacy octal escapes are never used.

### Non-ASCII characters
For the remaining non-ASCII characters, either the actual Unicode character (e.g. ∞) or the equivalent hex or Unicode escape (e.g. \u221e) is used, depending only on which makes the code easier to read and understand.

  ```shell
    /* Best: perfectly clear even without a comment. */
    const units = 'μs';

    /* Allowed: but unnecessary as μ is a printable character. */
    const units = '\u03bcs'; // 'μs'

    /* Good: use escapes for non-printable characters with a comment for clarity. */
    return '\ufeff' + content;  // Prepend a byte order mark.
  ```
# Source file structure
All new source files should either be a ECMAScript (ES) module (uses import and export statements).

Files consist of the following, in order:

- License or copyright information 
- @fileoverview JSDoc
- ES import statements
- The file’s implementation
Exactly one blank line separates each section that is present, except the file's implementation, which may be preceded by 1 or 2 blank lines.

### License or copyright information
If license or copyright information belongs in a file, it belongs here.

### @fileoverview JSDoc
See [Top/file-level](#top/file-level) comments for formatting rules.

## ES modules
ES modules are files that use the import and export keywords.

### Imports
Import statements must not be line wrapped and are therefore an exception to the 80-column limit.

#### Import paths
ES module files must use the import statement to import other ES module files. Do not goog.require another ES module.
  ```shell
  import './sideeffects.js';

  import * as goog from '../closure/goog/goog.js';
  import * as parent from '../parent.js';

  import {name} from './sibling.js';
  ```
  The .js file extension is not optional in import paths and must always be included.
  
  Do not import the same file multiple times. This can make it hard to determine the aggregate imports of a file.

#### Naming imports
Module import names (import * as name) are lowerCamelCase names that are derived from the imported file name.
  ```shell
  import * as fileOne from '../file-one.js';
  import * as fileTwo from '../file_two.js';
  import * as fileThree from '../filethree.js';

  import * as libString from './lib/string.js';
  import * as math from './math/math.js';
  import * as vectorMath from './vector/math.js';
  ```
Some libraries might commonly use a namespace import prefix that violates this naming scheme, but overbearingly common open source use makes the violating style more readable. The only library that currently falls under this exception is threejs, using the THREE prefix.

Default import names are derived from the imported file name and follow the rules in 6.2 Rules by identifier type.
  ```shell
  import MyClass from '../my-class.js';
  import myFunction from '../my_function.js';
  import SOME_CONSTANT from '../someconstant.js';
  ```
In general symbols imported via the named import (import {name}) should keep the same name. Avoid aliasing imports (import {SomeThing as SomeOtherThing}). Prefer fixing name collisions by using a module import (import *) or renaming the exports themselves.
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

### Exports
Symbols are only exported if they are meant to be used outside the module. Non-exported module-local symbols are not declared @private. There is no prescribed ordering for exported and module-local symbols.
Use named exports in all code. You can apply the export keyword to a declaration, or use the export {name}; syntax.

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
