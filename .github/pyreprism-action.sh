#!/usr/bin/env bash
# Entry point for the "PyReprism Clone Gate" composite action (see action.yml).
# Installs PyReprism from the action's own checked-out source (so the CLI matches
# the pinned ref), runs `pyreprism clones` with the configured inputs, writes the
# report, and propagates the duplication-gate exit code.
set -euo pipefail

action_path="${GITHUB_ACTION_PATH:-$(cd "$(dirname "$0")/.." && pwd)}"

extras="accurate"
if [ "${INPUT_SEMANTIC:-false}" = "true" ]; then
  extras="accurate,ast,semantic"
fi

venv="${RUNNER_TEMP:-/tmp}/pyreprism-venv"
echo "::group::Install PyReprism [${extras}]"
python3 -m venv "$venv"
"$venv/bin/python" -m pip install --quiet --upgrade pip
"$venv/bin/python" -m pip install --quiet "${action_path}[${extras}]"
"$venv/bin/pyreprism" --version
echo "::endgroup::"

# Build the `pyreprism clones` argument list from the inputs.
args=(clones)
# Intentionally word-split PATHS and EXTRA_ARGS (space-separated inputs).
# shellcheck disable=SC2206
args+=(${INPUT_PATHS:-.})
args+=(--reporter "${INPUT_REPORTER:-sarif}")
args+=(--min-tokens "${INPUT_MIN_TOKENS:-50}" --min-lines "${INPUT_MIN_LINES:-5}")
[ -n "${INPUT_LANG:-}" ] && args+=(--lang "$INPUT_LANG")
[ "${INPUT_NEAR:-false}" = "true" ] && args+=(--near)
[ "${INPUT_SEMANTIC:-false}" = "true" ] && args+=(--semantic)
[ -n "${INPUT_MAX_DUPLICATION:-}" ] && args+=(--max-duplication "$INPUT_MAX_DUPLICATION")
# shellcheck disable=SC2206
[ -n "${INPUT_EXTRA_ARGS:-}" ] && args+=(${INPUT_EXTRA_ARGS})

out="${INPUT_OUTPUT:-}"
echo "::group::pyreprism ${args[*]}"
set +e
if [ -n "$out" ]; then
  "$venv/bin/pyreprism" "${args[@]}" > "$out"
  code=$?
  cat "$out"
else
  "$venv/bin/pyreprism" "${args[@]}"
  code=$?
fi
set -e
echo "::endgroup::"

if [ -n "$out" ]; then
  echo "report=$out" >> "${GITHUB_OUTPUT:-/dev/null}"
fi

if [ "$code" -ne 0 ]; then
  echo "::error::PyReprism duplication gate failed (exit ${code})."
fi
exit "$code"
