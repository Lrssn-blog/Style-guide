# Perl Style Guide

A style guide for Perl 5.
It is based on [perlstyle](https://perldoc.perl.org/perlstyle) and [Perl Best Practices](https://www.oreilly.com/library/view/perl-best-practices/0596001738/) by Damian Conway, and is enforced with [perltidy](https://metacpan.org/dist/Perl-Tidy) and [Perl::Critic](https://metacpan.org/dist/Perl-Critic).

Deviations from Perl Best Practices, which was written for Perl 5.8:

- Code uses the features of modern Perl, such as subroutine signatures, `say` and postfix dereferencing, which replace several older recommendations.
- Classes are written with [Moo](https://metacpan.org/pod/Moo) instead of inside-out objects.
- There are no spaces inside parentheses, as in the other guides in this repository.

## Table of contents

[TOC]

## Perl version

Code targets Perl 5.36 or later.
Start every file with `use v5.36;`, which enables `strict`, `warnings`, subroutine signatures, `say` and other modern features, and disables several outdated ones such as bareword filehandles.

```perl
use v5.36;
```

## Source files

### File names

| Kind | Name | Example |
| --- | --- | --- |
| Scripts | Lowercase with hyphens or underscores, `.pl` | `count-lines.pl` |
| Installed commands | Lowercase with hyphens, no extension | `count-lines` |
| Modules | `CamelCase`, `.pm`, with the path matching the package name | `lib/Lrssn/Config.pm` |
| Tests | Lowercase with hyphens or underscores, `.t` | `t/config.t` |

### File encoding: UTF-8

Source files are encoded in UTF-8.
Add `use utf8;` to files that contain non-ASCII characters in the source code, so that Perl reads them as characters instead of bytes.

### Project layout

```text
project/
├── bin/
│   └── count-lines
├── lib/
│   └── Lrssn/
│       └── Config.pm
├── t/
│   └── config.t
├── .perlcriticrc
├── .perltidyrc
└── cpanfile
```

Put the logic in modules under `lib`, and keep the scripts in `bin` small.
The modules can then be tested and reused.

## Source file structure

### Scripts

A script consists of the following, in order:

1. The shebang line.
1. A comment that describes what the script does and how to use it.
1. `use v5.36;` and other pragmas, such as `use autodie;` and `use utf8;`.
1. Modules, in groups separated by a blank line: core modules, CPAN modules and the project's own modules.
1. Constants.
1. A call to `main`.
1. The subroutines, starting with `main`.
1. The documentation, after `__END__`.

```perl
#!/usr/bin/env perl
#
# Count the lines in all text files in a directory.
#
# Usage: count-lines.pl DIRECTORY

use v5.36;
use autodie;

use File::Spec;

use Lrssn::Files qw(text_files);

exit main(@ARGV);

sub main (@args) {
    my ($dir) = @args or die "Usage: $0 DIRECTORY\n";
    my $total = 0;
    for my $file (text_files($dir)) {
        $total += count_lines(File::Spec->catfile($dir, $file));
    }
    say "Total: $total";
    return 0;
}

sub count_lines ($path) {
    open my $fh, '<', $path;
    my $count = () = <$fh>;
    close $fh;
    return $count;
}
```

### Modules

A module consists of the following, in order:

1. The `package` statement, with the version.
1. `use v5.36;` and other pragmas.
1. Modules, grouped as in scripts.
1. Exports.
1. Constants and the subroutines.
1. `1;`, which is required for modules that use a Perl version older than 5.38.
1. The documentation, after `__END__`.

```perl
package Lrssn::Config v1.0.0;

use v5.36;
use autodie;

use Carp     qw(croak);
use Exporter qw(import);

our @EXPORT_OK = qw(load_config);

sub load_config ($path) {
    croak 'No configuration file given' if !defined $path;

    open my $fh, '<:encoding(UTF-8)', $path;
    my %setting_for;
    while (my $line = <$fh>) {
        chomp $line;
        next if $line =~ m/\A \s* (?: [#] | \z)/xms;

        my ($key, $value) = split m/\s* = \s*/xms, $line, 2;
        $setting_for{$key} = $value;
    }
    close $fh;

    return \%setting_for;
}

1;

__END__

=head1 NAME

Lrssn::Config - Load configuration files

=head1 SYNOPSIS

    use Lrssn::Config qw(load_config);

    my $config = load_config('app.conf');
    say $config->{name};

=head1 DESCRIPTION

Reads configuration files with one C<key = value> pair per line.
Empty lines and lines starting with C<#> are ignored.

=head1 FUNCTIONS

=head2 load_config($path)

Returns a hash reference with the settings in the file at C<$path>.
Dies if the file cannot be read.

=cut
```

### Versions

Declare the version of a module in the `package` statement, as a [Semantic Version](./Git.md#versioning) with a leading `v`.

```perl
package Lrssn::Config v1.2.3;
```

## Formatting

Do not format code by hand.
Use perltidy with the configuration in [Tooling](#tooling), and let it decide.
The rules below describe what the formatter produces.

### Indentation and line length

Indent by 4 spaces, never tabs.
Lines are at most 80 characters long.

### Braces

Opening braces go on the same line as the keyword or the subroutine name.
`else` and `elsif` go on their own line, after the closing brace, as perlstyle and Perl Best Practices recommend.
This is different from the other guides in this repository.

```perl
if ($count > $limit) {
    warn "Too many items\n";
}
elsif ($count == 0) {
    warn "No items\n";
}
else {
    process(@items);
}
```

Braces are required for all blocks, as Perl does not allow a block without them.

### Spaces

- Put a space between a keyword and the opening parenthesis: `if (`, `for (`, `while (`.
- Do not put a space between a function name and its opening parenthesis: `process($item)`.
- Put a space between the name of a subroutine and its signature: `sub greet ($name) {`.
- Do not put spaces inside parentheses or square brackets.
- Put spaces inside the braces of an anonymous hash: `{ name => 'Ada' }`.
- Put spaces around binary operators and after commas.

### Long expressions

When an expression does not fit on one line, the formatter breaks it before an operator and indents the continuation lines by 4 spaces.

```perl
if (   exists $setting_for{$key}
    && defined $value
    && length $value > 0
    && $key ne 'name')
{
    $setting_for{$key} = $value;
}
```

When a list does not fit on one line, put each element on its own line, and end the last one with a comma.

```perl
my %color_of = (
    primary   => '#D96C36',
    secondary => '#36D9CB',
    danger    => '#D93636',
);
```

### Blank lines

Separate subroutines with a blank line, and use single blank lines to separate groups of statements within a subroutine.

## Naming

### Rules by identifier type

| Identifier | Style | Example |
| --- | --- | --- |
| Variables and subroutines | `lowercase_with_underscores` | `$line_count`, `load_config()` |
| Packages and classes | `CamelCase`, separated by `::` | `Lrssn::Config` |
| Constants | `UPPERCASE_WITH_UNDERSCORES` | `MAX_RETRIES` |
| Internal subroutines | A leading underscore | `_parse_line()` |

### Descriptive names

Name variables after what they contain, and subroutines after what they do.

- Name arrays in the plural: `@users`.
- Name hashes after how they are looked up, so that the code reads like a sentence: `$title_of{$isbn}`, `$count_for{$word}`.
- Name booleans and subroutines that return them as questions: `$is_valid`, `has_children()`.
- Use single-character names only for short loops, and never `$a` or `$b`, which `sort` uses.

```perl
my %count_for;
for my $word (@words) {
    $count_for{$word}++;
}
```

## Language features

### Strict and warnings

`use v5.36` enables `strict` and `warnings`.
Never turn them off for a whole file.
If a warning must be turned off, do it for the smallest block possible, name the warning, and explain why in a comment.

```perl
{
    # The recursion depth is limited by the size of the input tree.
    no warnings 'recursion';
    walk($tree);
}
```

### Variables

Declare variables with `my`, in the smallest scope possible.
Only use package variables (`our`) for values that Perl or a module requires, such as `@EXPORT_OK`.

Use `local` only to change Perl's special variables temporarily, such as `$/` when reading a whole file.

```perl
my $content = do {
    local $/;
    <$fh>;
};
```

### Subroutines

Use subroutine signatures instead of unpacking `@_`.

```perl
# Good:
sub greet ($name, $greeting = 'Hello') {
    return "$greeting, $name!";
}

# Bad:
sub greet {
    my ($name, $greeting) = @_;
    $greeting //= 'Hello';
    return "$greeting, $name!";
}
```

- End every subroutine with an explicit `return`.
- Return failure with a bare `return;`, never `return undef;`, which returns a list with one element in list context, and that list is true.
- Do not use prototypes.
- Call subroutines with parentheses and without `&`.
- When a subroutine takes more than three arguments, pass a hash reference of named arguments.

```perl
sub create_user ($args) {
    my $name  = $args->{name};
    my $email = $args->{email};
    my $roles = $args->{roles} // [];
    return User->new(name => $name, email => $email, roles => $roles);
}

create_user({ name => 'Ada', email => 'ada@example.com' });
```

### Strings

Use single quotes for strings without interpolation, and double quotes only when the string interpolates variables or contains escapes such as `\n`.

```perl
my $name     = 'style-guide';
my $greeting = "Hello, $name\n";
```

Use `q{}` and `qq{}` for strings that contain quotes.
Use an indented here document (`<<~`) for text that spans several lines.

```perl
my $usage = <<~"END_USAGE";
    Usage: $0 [options] DIRECTORY

    Count the lines in all text files in DIRECTORY.
    END_USAGE
```

Use `say` instead of `print` with a trailing `"\n"`.

### References

Use postfix dereferencing instead of the circumfix form.

```perl
# Good:
for my $user ($users->@*) {
    say $user->{name};
}
my @keys = sort keys $config->%*;

# Bad:
for my $user (@{$users}) {
    say $user->{name};
}
my @keys = sort keys %$config;
```

### Hashes

Use `exists` to check whether a key is present, and `defined` to check whether its value is defined.
Sort the keys when the order of the output matters, as the order of a hash is random.

Do not use `each` to iterate over a hash.
It keeps an iterator in the hash, which breaks when the loop exits early or the hash is iterated elsewhere.

```perl
for my $key (sort keys %count_for) {
    say "$key: $count_for{$key}";
}
```

### Loops

Use `for` with a lexical loop variable to iterate over lists.
Do not use C-style `for` loops, and do not rely on `$_` in loops that are longer than a few lines.

```perl
# Good:
for my $user (@users) {
    notify($user);
}

# Bad:
for (my $i = 0 ; $i < @users ; $i++) {
    notify($users[$i]);
}
```

Use `map` and `grep` with a block to transform and filter lists, and never in void context.

```perl
my @names = map { $_->{name} } grep { $_->{active} } @users;
```

Label loops when using `next` or `last` in a nested loop.

### Conditions

Postfix `if` and `unless` are fine for simple statements that change the flow, such as `return`, `next` and `die`.
Use a full `if` block for anything else.

```perl
return if !@items;
next   if $line =~ m/\A [#]/xms;
```

Use `unless` only for simple conditions, never with `else`, and never with a negation.

Use `eq`, `ne`, `lt` and `gt` to compare strings, and `==`, `!=`, `<` and `>` to compare numbers.

### Regular expressions

- Use the `/x` flag for regular expressions that are longer than a few characters, and use whitespace and comments to make them readable.
- Use `\A` and `\z` to match the start and the end of a string, instead of `^` and `$`.
- Use named captures for patterns with more than one capture.
- Compile patterns that are used several times with `qr//`.

```perl
my $date_pattern = qr{
    (?<year>  \d{4} ) -
    (?<month> \d{2} ) -
    (?<day>   \d{2} )
}xms;

if ($text =~ m/\A $date_pattern \z/xms) {
    say "Year: $+{year}";
}
```

### Files

Open files with three arguments and a lexical filehandle, and set the encoding of text files.
Use `autodie`, so that `open`, `close` and other built-in functions die when they fail.

```perl
use autodie;

open my $fh, '<:encoding(UTF-8)', $path;
my @lines = <$fh>;
close $fh;
```

Close files as soon as you are done with them.

### Error handling

Throw errors with `die` in scripts.
In modules, use `croak` from the `Carp` module, which reports the error at the line that called the module.

Do not use `eval` with a string.
Catch errors with `eval` and a block that ends with `1`, and check its result instead of `$@`, which can be cleared before you read it.

```perl
my $config;
if (!eval { $config = load_config($path); 1 }) {
    my $error = $@ || 'Unknown error';
    warn "Using the default configuration: $error";
    $config = default_config();
}
```

On Perl 5.40 and later, use `try` and `catch` instead.

```perl
use feature 'try';

my $config;
try {
    $config = load_config($path);
}
catch ($error) {
    warn "Using the default configuration: $error";
    $config = default_config();
}
```

### Constants

Declare constants with `use constant`.

```perl
use constant {
    MAX_RETRIES => 3,
    TIMEOUT     => 30,
};
```

### Modules and exports

Export nothing by default.
List the symbols that may be imported in `@EXPORT_OK`, and import them by name.

```perl
use Exporter qw(import);

our @EXPORT_OK = qw(load_config save_config);
```

```perl
use Lrssn::Config qw(load_config);
```

### Classes

Write classes with [Moo](https://metacpan.org/pod/Moo), which provides attributes, constructors and roles with little overhead.
Do not access the internal hash of an object from outside its class.

```perl
package Lrssn::User v1.0.0;

use v5.36;

use Moo;

has name  => (is => 'ro', required => 1);
has email => (is => 'ro', required => 1);
has roles => (is => 'ro', default  => sub { [] });

sub is_admin ($self) {
    return !!grep { $_ eq 'admin' } $self->roles->@*;
}

1;
```

The `class` feature that was added in Perl 5.38 is still experimental.
Do not use it until it is stable.

### Features to avoid

- String `eval`, except to load modules whose names are only known at runtime, and even then prefer `require` with a file name.
- `goto`, except `goto &sub` in `AUTOLOAD` subroutines.
- Formats (`format` and `write`).
- Bareword filehandles, two-argument `open` and `select` for changing the default output.
- Changing `$_` or `@_` in a way that the caller can see.

## Comments and documentation

### POD

Document every module and script with POD after `__END__`.
Include at least these sections:

| Section | Content |
| --- | --- |
| `NAME` | The name and a one-line description |
| `SYNOPSIS` | A short example of how to use it |
| `DESCRIPTION` | What it does |
| `FUNCTIONS` or `METHODS` | Each public subroutine, its arguments and its return value |

Check the documentation with `podchecker`.

### Comments

Comments start with `#` followed by a space.
Explain why the code does something, not what it does.

### TODO comments

Write `TODO` comments with the user name of the author or a link to an issue.

```perl
# TODO(lrssn): Support YAML configuration files.
# TODO(#42): Retry on network errors.
```

## Testing

Write tests with [Test::More](https://perldoc.perl.org/Test::More), which is part of the core distribution.
Put the tests in `t`, and run them with `prove`.

```perl
use v5.36;

use Test::More;

use Lrssn::Config qw(load_config);

my $config = load_config('t/data/app.conf');
is($config->{name}, 'style-guide', 'reads the name');
ok(!exists $config->{comment}, 'skips comments');

done_testing;
```

```bash
prove -lr t
```

## Tooling

### perltidy

Format the code with [perltidy](https://metacpan.org/dist/Perl-Tidy).
Add this `.perltidyrc` to the root of the repository:

```text
# Indent by 4 spaces, and continuation lines by 4 more.
--indent-columns=4
--continuation-indentation=4
--maximum-line-length=80
# No spaces inside parentheses and square brackets.
--paren-tightness=2
--square-bracket-tightness=2
# Put else and elsif on their own line.
--nocuddled-else
```

Format all files in place, without keeping backups:

```bash
find bin lib t -type f | xargs perltidy -b -bext='/'
```

### Perl::Critic

Check the code with [Perl::Critic](https://metacpan.org/dist/Perl-Critic), which enforces most of the rules in Perl Best Practices.
Add this `.perlcriticrc` to the root of the repository:

```ini
severity = 3
verbose = 8
# Treat scripts and tests as programs, not modules.
program-extensions = .pl .t

# `use v5.36` enables subroutine signatures, which Perl::Critic reports as
# prototypes.
[-Subroutines::ProhibitSubroutinePrototypes]

# `use v5.36` is the recommended way to declare the Perl version.
[-ValuesAndExpressions::ProhibitVersionStrings]

# Only require the /x flag on longer regular expressions.
[RegularExpressions::RequireExtendedFormatting]
minimum_regex_length_to_complain_about = 20

# Allow turning off warnings when the category is named.
[TestingAndDebugging::ProhibitNoWarnings]
allow_with_category_restriction = 1
```

```bash
perlcritic bin lib t
```

### Dependencies

List the dependencies in a `cpanfile`, and install them with [cpanm](https://metacpan.org/pod/App::cpanminus) or [Carton](https://metacpan.org/pod/Carton).

```perl
requires 'perl', 'v5.36';
requires 'Moo',  '2.005';

on test => sub {
    requires 'Test::More', '1.302';
};
```

```bash
cpanm --installdeps .
```

## See also

- [perlstyle](https://perldoc.perl.org/perlstyle)
- [Perl Best Practices](https://www.oreilly.com/library/view/perl-best-practices/0596001738/)
- [Perl::Critic policies](https://metacpan.org/dist/Perl-Critic)
- [Modern Perl](https://www.modernperlbooks.com/)
