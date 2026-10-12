#!/usr/bin/env bash
#
# Copies the Markdown files of this repository into a checkout of its GitHub
# wiki. README.md becomes the wiki home page and relative links to other
# Markdown files are rewritten to wiki page links.
#
# Usage: scripts/sync-wiki.sh <wiki-checkout>

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: ${0} <wiki-checkout>" >&2
    exit 1
fi

readonly wiki_dir="${1}"
readonly repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Remove pages from a previous sync so deleted guides disappear from the wiki.
find "${wiki_dir}" -maxdepth 1 -type f \( -name '*.md' -o -name '*.jpeg' \) \
    -delete

for file in "${repo_dir}"/*.md; do
    name="$(basename "${file}" .md)"
    if [[ "${name}" == "README" ]]; then
        name="Home"
    fi
    sed -E 's#\]\((\./)?([A-Za-z_-]+)\.md(\#[^)]*)?\)#](\2\3)#g' "${file}" \
        | sed -E 's#\]\(README(\#[^)]*)?\)#](Home\1)#g' \
        > "${wiki_dir}/${name}.md"
done

cp "${repo_dir}"/*.jpeg "${wiki_dir}/"
