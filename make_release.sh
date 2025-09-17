#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    cat >&2 <<'USAGE'
Usage: make_release.sh [--prepare] <version>

Options:
  --prepare   Generate or refresh release notes draft for <version> and exit.
  --ai_draft  Ask Codex to draft release notes for <version> and prompt before saving.
  -h, --help  Show this help.
USAGE
    exit 64
}

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Required command '$1' not found in PATH." >&2
        exit 69
    fi
}

cleanup_on_error() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        if [[ ${tag_created:-0} -eq 1 && ${tag_pushed:-0} -eq 0 ]]; then
            git tag -d "$tag" >/dev/null 2>&1 || true
        fi
    fi
}

trap cleanup_on_error ERR INT

tag=""
tag_created=0
tag_pushed=0
prepare_only=0
ai_draft=0
version_input=""
version_commit_created=0

generate_release_notes() {
    local previous_tag=""
    if previous_tag=$(git describe --tags --abbrev=0 --match 'v*' 2>/dev/null); then
        echo "Generating draft notes from ${previous_tag}..HEAD." >&2
    else
        echo "No earlier release tag found; generating draft from entire history." >&2
    fi

    local log_range="HEAD"
    if [[ -n $previous_tag ]]; then
        log_range="${previous_tag}..HEAD"
    fi

    mapfile -t commits < <(git log --no-merges --pretty=format:'- %s' "$log_range")

    mkdir -p "$(dirname "$release_notes_path")"

    {
        echo "# Psionics v${version}"
        echo
        echo "## Highlights"
        echo
        if (( ${#commits[@]} )); then
            printf '%s\n' "${commits[@]}"
        else
            echo "- TODO: Summarize key changes."
        fi
        echo
        echo "## Additional Notes"
        echo
        echo "- TODO: Add supplemental context."
    } > "$release_notes_path"

    echo "Draft written to $release_notes_path. Review and edit as needed." >&2
}

run_ai_draft() {
    require_command codex

    local instructions_file="Scripts/release_note_ai_instructions.md"
    if [[ ! -r $instructions_file ]]; then
        echo "AI instructions file missing: $instructions_file" >&2
        exit 78
    fi

    local branch_name
    if ! branch_name=$(git rev-parse --abbrev-ref HEAD); then
        echo "Unable to determine current branch." >&2
        exit 78
    fi

    local previous_tag=""
    if previous_tag=$(git describe --tags --abbrev=0 --match 'v*' --exclude "v${version}" 2>/dev/null); then
        echo "Detected previous release tag: $previous_tag" >&2
    else
        echo "No earlier matching release tag found; using entire history." >&2
        previous_tag=""
    fi

    local log_range="HEAD"
    if [[ -n $previous_tag ]]; then
        log_range="${previous_tag}..HEAD"
    fi

    local commit_log
    if ! commit_log=$(git log --no-merges --pretty=format:'- %s (%h)' "$log_range"); then
        echo "Failed to collect commit messages for $log_range" >&2
        exit 78
    fi
    if [[ -z $commit_log ]]; then
        commit_log="(No commits detected in range.)"
    fi

    local diffstat
    if ! diffstat=$(git diff "$log_range" --stat); then
        echo "Failed to compute diffstat for $log_range" >&2
        exit 78
    fi
    if [[ -z $diffstat ]]; then
        diffstat="(No file changes detected.)"
    fi

    local instructions_payload
    instructions_payload=$(<"$instructions_file")

    local prompt
    prompt=$(cat <<EOF
Use the project instructions below to draft release notes for Psionics version v${version}. Deliver Markdown that a human editor can review before publishing.

<<instructions>>
${instructions_payload}
<</instructions>>

Context:
- Current branch: ${branch_name}
- Target version: v${version}
- Previous release tag: ${previous_tag:-none}

Commits since ${previous_tag:-repository start}:
${commit_log}

Diffstat:
${diffstat}

Remember this is a draft—flag uncertainties for human review when needed.
EOF
)

    local output_tmp
    output_tmp=$(mktemp)

    echo "Requesting draft from Codex..." >&2
    if ! codex exec -- "$prompt" | tee "$output_tmp"; then
        echo "Codex CLI failed to produce a draft." >&2
        rm -f "$output_tmp"
        exit 78
    fi

    local ai_target="release_notes/${version}_AGENT.md"
    echo >&2
    echo "Draft stored at: $output_tmp" >&2
    echo "Proposed destination: $ai_target" >&2

    read -rp "Write draft to ${ai_target}? [y/N]: " save_choice
    if [[ $save_choice =~ ^[Yy]$ ]]; then
        if [[ -e $ai_target ]]; then
            read -rp "${ai_target} exists. Overwrite? [y/N]: " overwrite_choice
            if [[ ! $overwrite_choice =~ ^[Yy]$ ]]; then
                echo "Skipped writing draft." >&2
                rm -f "$output_tmp"
                return
            fi
        fi
        mkdir -p "$(dirname "$ai_target")"
        if cat "$output_tmp" > "$ai_target"; then
            echo "Draft saved to $ai_target." >&2
        else
            echo "Failed to write draft to $ai_target." >&2
        fi
    else
        echo "Skipped writing draft." >&2
    fi

    rm -f "$output_tmp"
}

update_version_reference() {
    local preamble_file="preamble.sty"

    if [[ ! -w $preamble_file ]]; then
        echo "Cannot update version: $preamble_file is not writable." >&2
        exit 73
    fi

    require_command python3

    local current_version
    if ! current_version=$(python3 - "$preamble_file" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
match = re.search(r"Version\s+([0-9]+(?:\.[0-9]+)*)", text)
if not match:
    sys.exit(1)
print(match.group(1))
PY
    ); then
        echo "Failed to detect current version string in $preamble_file." >&2
        exit 78
    fi

    if [[ $current_version == $version ]]; then
        echo "Preamble version already set to $version." >&2
        return
    fi

    if ! python3 - "$preamble_file" "$version" <<'PY'
import sys
from pathlib import Path

path, version = sys.argv[1:]
text = Path(path).read_text()
token = "Version "

idx = text.find(token)
if idx == -1:
    print("Failed to locate version placeholder.", file=sys.stderr)
    sys.exit(1)

end_idx = idx + len(token)
while end_idx < len(text) and (text[end_idx].isdigit() or text[end_idx] == '.'):
    end_idx += 1

new_text = text[:idx] + token + version + text[end_idx:]
Path(path).write_text(new_text)
PY
    then
        echo "Unable to update version string in $preamble_file." >&2
        exit 78
    fi

    if git diff --quiet -- "$preamble_file"; then
        echo "No changes detected in $preamble_file after version update." >&2
        exit 78
    fi

    git add "$preamble_file"
    git commit -m "chore: bump version to v${version}"
    version_commit_created=1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --prepare)
            prepare_only=1
            shift
            ;;
        --ai_draft)
            ai_draft=1
            shift
            ;;
        -h|--help)
            usage
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "Unknown option: $1" >&2
            usage
            ;;
        *)
            if [[ -n $version_input ]]; then
                echo "Multiple version arguments supplied." >&2
                usage
            fi
            version_input="$1"
            shift
            ;;
    esac
done

if [[ $# -gt 0 ]]; then
    echo "Unexpected extra arguments: $*" >&2
    usage
fi

[[ -n "$version_input" ]] || usage

if [[ $prepare_only -eq 1 && $ai_draft -eq 1 ]]; then
    echo "--prepare and --ai_draft cannot be used together." >&2
    usage
fi

if [[ $version_input == v* ]]; then
    echo "Detected leading 'v' in version '$version_input'; normalizing." >&2
    version_input=${version_input#v}
fi

version=$version_input
release_notes_path="release_notes/${version}.md"

require_command git

if [[ $prepare_only -eq 1 ]]; then
    if [[ -e $release_notes_path ]]; then
        echo "Release notes already exist at $release_notes_path; leaving in place." >&2
    else
        generate_release_notes
    fi
    echo "Edit the draft, then rerun without --prepare to publish." >&2
    exit 0
fi

if [[ $ai_draft -eq 1 ]]; then
    run_ai_draft
    exit 0
fi

require_command gh
require_command make

if [[ ! -r $release_notes_path ]]; then
    echo "Release notes missing or unreadable: $release_notes_path" >&2
    echo "Run '$0 --prepare $version' to generate a draft." >&2
    exit 66
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
    echo "Not inside a git repository. Aborting." >&2
    exit 69
fi

if ! git remote get-url origin >/dev/null 2>&1; then
    echo "Remote 'origin' is not configured. Configure it before releasing." >&2
    exit 69
fi

current_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ $current_branch != "main" ]]; then
    echo "Release script must be run from 'main'. Current branch: $current_branch" >&2
    exit 70
fi

if [[ -n $(git status --porcelain) ]]; then
    echo "Working tree has uncommitted changes. Clean it before releasing." >&2
    exit 70
fi

git fetch origin main --quiet
git fetch --tags --quiet

local_head=$(git rev-parse HEAD)
remote_head=$(git rev-parse origin/main)
if [[ $local_head != $remote_head ]]; then
    echo "Local 'main' is not up to date with origin/main. Pull before releasing." >&2
    exit 70
fi

update_version_reference

if [[ $version_commit_created -eq 1 ]]; then
    echo "Pushing version bump commit to origin/main."
    if ! git push origin main; then
        echo "Failed to push version bump commit." >&2
        exit 75
    fi
fi

tag="v${version}"

if git rev-parse "$tag" >/dev/null 2>&1; then
    echo "Tag '$tag' already exists locally." >&2
    exit 70
fi

if git ls-remote --exit-code --tags origin "$tag" >/dev/null 2>&1; then
    echo "Tag '$tag' already exists on origin." >&2
    exit 70
fi

echo "Building project artifacts..."
make clean
make

pdf_path="Psionics.pdf"
if [[ ! -f $pdf_path ]]; then
    echo "Expected PDF '$pdf_path' not found after build." >&2
    exit 74
fi

release_pdf="psionics_v${version//./_}.pdf"
cp "$pdf_path" "$release_pdf"

echo "Tagging latest commit on main as '$tag'."
git tag -a "$tag" -m "Psionics v${version}"
tag_created=1

echo "Pushing tag '$tag' to origin."
git push origin "$tag"
tag_pushed=1

echo "Creating GitHub release for '$tag'."
gh release create "$tag" -F "$release_notes_path" "$release_pdf" --title "Psionics v${version}"

echo "Release '$tag' created successfully."
