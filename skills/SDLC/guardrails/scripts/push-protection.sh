#!/usr/bin/env bash
# Usage: push-protection.sh [owner/repo] | --self-test
#
# Prints whether GitHub secret push protection is on for the repository
# (default: the one `gh` sees in the current directory). It only reads the
# setting; turning it on is the user's call. For GitLab, read the project's
# secret push protection setting instead.
set -euo pipefail

verdict() {
  case "$1" in
    enabled) echo "on" ;;
    disabled) echo "off; tell the user to turn it on under Settings, Code security (Push protection)" ;;
    # No security_and_analysis block: the token cannot see it, which is not "off".
    *) echo "unknown: the token lacks admin permission; ask the user to read Settings, Code security" ;;
  esac
}

if [ "${1:-}" = --self-test ]; then
  [ "$(verdict enabled)" = on ] || { echo "FAIL: enabled"; exit 1; }
  case "$(verdict disabled)" in off*) ;; *) echo "FAIL: disabled"; exit 1 ;; esac
  case "$(verdict '')" in unknown*) ;; *) echo "FAIL: missing block"; exit 1 ;; esac
  echo "push-protection self-test passed"; exit 0
fi

repo="${1:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
verdict "$(gh api "repos/$repo" --jq '.security_and_analysis.secret_scanning_push_protection.status // ""')"
