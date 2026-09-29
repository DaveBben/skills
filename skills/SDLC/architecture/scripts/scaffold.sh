#!/usr/bin/env bash
# Usage: scaffold.sh <template repo or path> <name> <directory> <test command...> | self-test
#
# Stands up a new repository from a language template, committing each step:
#   1. copies the template into <directory> without its git history, beside any
#      files already there (docs/adr/ from the architecture skill), running
#      git init -b main when <directory> is not a repository yet
#   2. renames example_project, ExampleProject and EXAMPLE_PROJECT to <name> in
#      file contents and paths, and fails when any occurrence remains
#   3. runs the test command, and fails before any removal when it fails
set -euo pipefail
die() { echo "$*" >&2; exit 1; }
commit() { git add -A && { git diff --cached --quiet || git commit -q -m "$1"; }; }

scaffold() {
  local tpl="$1" name="$2" dir="$3"; shift 3
  local scratch; scratch="$(mktemp -d)"
  git clone -q --depth 1 "$tpl" "$scratch/t" 2>/dev/null || git clone -q "$tpl" "$scratch/t" || die "Could not clone $tpl."
  rm -rf "$scratch/t/.git"
  mkdir -p "$dir"
  [ -d "$dir/.git" ] || git -C "$dir" init -q -b main
  cp -R "$scratch/t/." "$dir/"
  rm -rf "$scratch"
  cd "$dir"
  commit "chore: import template"

  local snake="${name//-/_}"
  local camel; camel="$(printf '%s' "$snake" | awk -F_ '{for(i=1;i<=NF;i++) printf "%s", toupper(substr($i,1,1)) substr($i,2)}')"
  local upper; upper="$(printf '%s' "$snake" | tr '[:lower:]' '[:upper:]')"
  git ls-files -z | xargs -0 grep -Il 'example_project\|ExampleProject\|EXAMPLE_PROJECT' 2>/dev/null \
    | while IFS= read -r f; do
        sed -i.bak -e "s/example_project/$snake/g" -e "s/ExampleProject/$camel/g" -e "s/EXAMPLE_PROJECT/$upper/g" "$f" && rm -f "$f.bak"
      done
  find . -depth -name '*example_project*' -not -path './.git/*' | while IFS= read -r p; do
    mv "$p" "$(dirname "$p")/$(basename "$p" | sed "s/example_project/$snake/g")"
  done
  if git grep -qi 'example_project\|exampleproject' -- . 2>/dev/null; then die "The template name remains after the rename."; fi
  commit "chore: rename example_project to $name"

  "$@" || die "The template's tests fail before any change. Stop here."
  commit "chore: verify default state passes"
  echo "$PWD"
}

case "${1:-}" in
self-test)
  me="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  t="$(mktemp -d)"; trap 'rm -rf "$t"' EXIT
  export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
  mkdir -p "$t/tpl/src/example_project" && cd "$t/tpl" && git init -q -b main
  echo 'NAME = "example_project"  # ExampleProject EXAMPLE_PROJECT' > src/example_project/__init__.py
  git add -A && git commit -q -m tpl
  mkdir -p "$t/app/docs/adr" && echo adr > "$t/app/docs/adr/lang.md"
  out="$("$me" "$t/tpl" my-app "$t/app" true)"
  [ -f "$t/app/src/my_app/__init__.py" ] || { echo "FAIL rename paths"; exit 1; }
  grep -q 'NAME = "my_app"  # MyApp MY_APP' "$t/app/src/my_app/__init__.py" || { echo "FAIL rename contents"; exit 1; }
  [ -f "$t/app/docs/adr/lang.md" ] || { echo "FAIL kept existing files"; exit 1; }
  [ "$(git -C "$t/app" log --oneline | wc -l | tr -d ' ')" -ge 2 ] || { echo "FAIL commits"; exit 1; }
  [ "$out" = "$(cd "$t/app" && pwd)" ] || { echo "FAIL printed path"; exit 1; }
  if "$me" "$t/tpl" other "$t/other" false >/dev/null 2>&1; then echo "FAIL passed a failing test command"; exit 1; fi
  echo "self-test passed"
  ;;
""|-h|--help) sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
*) [ $# -ge 4 ] || die "Usage: scaffold.sh <template> <name> <directory> <test command...>"; scaffold "$@" ;;
esac
