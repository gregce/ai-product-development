#!/usr/bin/env bash
# Regenerate every data/*.json payload the slides depend on.
#
# Runs the four stdlib-only Python analyzers in sequence, printing each
# output path as it lands. Safe to re-run; each script overwrites its
# own JSON file. No args — the Python scripts bake in sensible defaults
# pointing at the local Stoa monorepo checkout.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DATA_DIR="${REPO_ROOT}/data"

PY="${PYTHON:-python3}"

echo "--> as-built fingerprints"
"${PY}" "${SCRIPT_DIR}/analyze_as_built.py"
echo "    ${DATA_DIR}/as_built_summary.json"

echo "--> design docs"
"${PY}" "${SCRIPT_DIR}/analyze_design_docs.py"
echo "    ${DATA_DIR}/design_docs_summary.json"

echo "--> implementation docs"
"${PY}" "${SCRIPT_DIR}/analyze_implementation_docs.py"
echo "    ${DATA_DIR}/implementation_docs_summary.json"

echo "--> agentic release workflow"
"${PY}" "${SCRIPT_DIR}/analyze_agentic_release_workflow.py"
echo "    ${DATA_DIR}/release_workflow_summary.json"

echo "done."
