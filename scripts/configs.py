#!/usr/bin/env python3
"""Keeps the config files in src/ identical to the code blocks in the guides.

Usage:
    scripts/configs.py          Check that every config matches its guide.
    scripts/configs.py --write  Regenerate the config files from the guides.
"""

import difflib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Each config is the concatenation of one or more code blocks of a guide.
# A block is selected by its info string and the start of its first line.
CONFIGS = {
    'src/bash/.editorconfig': [('bash/Bash.md', 'ini', '[*.sh]')],
    'src/cpp/.clang-format': [('cpp/Cpp.md', 'yaml', '---\nLanguage: Cpp')],
    'src/cpp/.clang-tidy': [('cpp/Cpp.md', 'yaml', '---\nChecks:')],
    'src/docker/.hadolint.yaml': [('docker/Docker.md', 'yaml', 'failure-threshold')],
    'src/go/.editorconfig': [('go/Go.md', 'ini', '[{*.go')],
    'src/go/.golangci.yml': [('go/Go.md', 'yaml', 'version: "2"')],
    'src/haskell/fourmolu.yaml': [('haskell/Haskell.md', 'yaml', 'indentation: 4')],
    'src/haskell/.hlint.yaml': [('haskell/Haskell.md', 'yaml', '# Suggestions of')],
    'src/latex/.chktexrc': [('latex/Latex.md', 'text', 'CmdLine')],
    'src/latex/.latexindent.yaml': [('latex/Latex.md', 'yaml', 'defaultIndent')],
    'src/markdown/.markdownlint.json': [('markdown/Markdown.md', 'json', '{')],
    'src/perl/.perlcriticrc': [('perl/Perl.md', 'ini', 'severity')],
    'src/perl/.perltidyrc': [('perl/Perl.md', 'text', '# Indent by 4')],
    'src/python/pyproject.toml': [
        ('python/Python.md', 'toml', '[tool.ruff]'),
        ('python/Python.md', 'toml', '[tool.mypy]'),
    ],
    'src/rust/rustfmt.toml': [('rust/Rust.md', 'toml', 'max_width')],
    'src/typescript/.clang-format': [
        ('typescript/Typescript.md', 'yaml', '---\nLanguage: JavaScript')],
    'src/typescript/eslint.config.js': [
        ('typescript/Typescript.md', 'javascript', 'import eslint')],
    'src/typescript/tsconfig.json': [
        ('typescript/Typescript.md', 'json', '{')],
}

FENCE = re.compile(r'^```(\w*)\n(.*?)^```$', re.MULTILINE | re.DOTALL)


def find_block(guide, lang, start):
    text = (ROOT / 'src' / guide).read_text()
    matches = [body for info, body in FENCE.findall(text)
               if info == lang and body.startswith(start)]
    if len(matches) != 1:
        raise SystemExit(
            f'{guide}: expected 1 {lang} block starting with {start!r}, '
            f'found {len(matches)}')
    return matches[0]


def main():
    write = '--write' in sys.argv[1:]
    failed = False
    for path, blocks in CONFIGS.items():
        want = '\n'.join(find_block(*block) for block in blocks)
        target = ROOT / path
        have = target.read_text() if target.exists() else ''
        if have == want:
            continue
        if write:
            target.write_text(want)
            print(f'wrote {path}')
            continue
        failed = True
        diff = difflib.unified_diff(
            have.splitlines(), want.splitlines(), path, f'{path} (guide)',
            lineterm='')
        print('\n'.join(diff))
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
