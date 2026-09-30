#!/usr/bin/env bash
# Usage: setup-next.sh [repository] [<stage> | --done <stage>] | --self-test
#
# Prints the first setup stage of references/setup.md that is not done in
# <repository> (default: the current directory), or the named stage. A stage is
# done when `--done <stage>` recorded it in the repository's git config
# (guardrails.setupDone), or when a file only that stage writes exists: the
# receipts below. The output names every stage a receipt skipped.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
doc="$here/../references/setup.md"
stages=(survey slots contracts loop guards instructions gate secrets ci)

receipt() {
  case "$1" in
    # Loop is done once _slots.sh is no longer the shipped example.
    loop)   grep -qs 'turn-end-check.sh' "$2/.claude/settings.json" && [ -f "$2/.claude/hooks/_slots.sh" ] \
              && ! cmp -s "$2/.claude/hooks/_slots.sh" "$here/_slots.sh" ;;
    # The contracts stage may write `# owner reads: checks`; only guards writes deps.
    guards) grep -qs '^# owner reads: deps' "$2/CODEOWNERS" "$2/.github/CODEOWNERS" "$2/docs/CODEOWNERS" ;;
    gate)   grep -qs 'red_commit_scope' "$2/.pre-commit-config.yaml" ;;
    *) return 1 ;;
  esac
}

recorded() { git -C "$2" config --get-all guardrails.setupDone 2>/dev/null | grep -qx "$1"; }

# The stage's section: from its `## ` heading, whose first word lowercased is
# the stage name, to the next `## ` heading.
show() { awk -v s="$1" '/^## /{split(substr($0, 4), w, " "); on = (tolower(w[1]) == s)} on' "$doc"; }

next_stage() {
  local repo="$1" s skipped=()
  for s in "${stages[@]}"; do
    recorded "$s" "$repo" && continue
    if receipt "$s" "$repo"; then skipped+=("$s"); continue; fi
    show "$s"
    echo
    [ ${#skipped[@]} -eq 0 ] || echo "Skipped because their files exist: ${skipped[*]}. To redo one: $0 $repo <stage>"
    echo "When this stage is finished, run: $0 $repo --done $s"
    echo "Stages in order: ${stages[*]}. Paths above that start scripts/ or references/ are in"
    echo "$(dirname "$here"), except the repository's scripts/; every other path is in $repo."
    return 0
  done
  echo "Every setup stage is done. To redo one: $0 $repo <stage>"
}

main() {
  # A stage or --done with no repository means the current directory.
  if [[ " ${stages[*]} --done " == *" ${1:-} "* && -n "${1:-}" && ! -d "$1" ]]; then set -- . "$@"; fi
  local repo="${1:-.}"
  git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 \
    || { echo "$repo is not a git repository. Usage: $0 [repository] [<stage> | --done <stage>]" >&2; return 1; }
  case "${2:-}" in
    '') next_stage "$repo" ;;
    --done) [[ " ${stages[*]} " == *" ${3:-} "* ]] || { echo "No stage '${3:-}'. Stages: ${stages[*]}" >&2; return 1; }
            recorded "${3:-}" "$repo" || git -C "$repo" config --add guardrails.setupDone "${3:-}" ;;
    *) [[ " ${stages[*]} " == *" $2 "* ]] || { echo "No stage '$2'. Stages: ${stages[*]}" >&2; return 1; }
       show "$2" ;;
  esac
}

self_test() {
  local d s out; d="$(mktemp -d /tmp/guardrails-setup-XXXXXX)"
  trap 'rm -rf "$d"' RETURN
  git -C "$d" init -q
  for s in "${stages[@]}"; do
    [ -n "$(show "$s")" ] || { echo "FAIL: setup.md has no section for stage $s"; return 1; }
  done
  [ "$(grep -c '^## ' "$doc")" = ${#stages[@]} ] || { echo "FAIL: setup.md has a section no stage prints"; return 1; }
  main "$d" | sed -n 1p | grep -qx '## Survey' || { echo "FAIL: a fresh repository does not start at survey"; return 1; }
  main "$d" --done survey; main "$d" --done survey
  [ "$(git -C "$d" config --get-all guardrails.setupDone | wc -l | tr -d ' ')" = 1 ] || { echo "FAIL: --done recorded twice"; return 1; }
  main "$d" | sed -n 1p | grep -qx '## Slots' || { echo "FAIL: survey done, slots not next"; return 1; }
  main "$d" --done slots; main "$d" --done contracts
  printf '# owner reads: checks\nratchet-baseline.json @me\n\n' > "$d/CODEOWNERS"
  mkdir -p "$d/.claude/hooks"; echo '{"command": "turn-end-check.sh"}' > "$d/.claude/settings.json"
  cp "$here/_slots.sh" "$d/.claude/hooks/_slots.sh"
  main "$d" | sed -n 1p | grep -qx '## Loop' || { echo "FAIL: the shipped _slots.sh example counted as loop done"; return 1; }
  echo 'fast_check() { mine; }' >> "$d/.claude/hooks/_slots.sh"
  out="$(main "$d")"
  printf '%s\n' "$out" | sed -n 1p | grep -qx '## Guards' || { echo "FAIL: with loop done, guards is not next (loop not skipped, or guards skipped)"; return 1; }
  printf '%s\n' "$out" | grep -q 'Skipped because their files exist: loop' || { echo "FAIL: the skip was not named"; return 1; }
  printf '%s\n' "$out" | grep -q 'Skipped because their files exist: loop\.' || { echo "FAIL: a contracts-stage CODEOWNERS heading skipped guards"; return 1; }
  main "$d" loop | sed -n 1p | grep -qx '## Loop' || { echo "FAIL: a named stage was not printed"; return 1; }
  (cd "$d" && main slots) | sed -n 1p | grep -qx '## Slots' || { echo "FAIL: a stage with no repository did not use the current directory"; return 1; }
  { main /nonexistent 2>&1 || true; } | grep -q 'is not a git repository' || { echo "FAIL: no message for a missing repository"; return 1; }
  main "$d" --done bogus 2>/dev/null && { echo "FAIL: an unknown stage was recorded"; return 1; }
  for s in "${stages[@]}"; do main "$d" --done "$s"; done
  main "$d" | grep -q '^Every setup stage is done' || { echo "FAIL: no end"; return 1; }
  echo "setup-next self-test passed"
}

if [ "${1:-}" = --self-test ]; then self_test; else main "$@"; fi
