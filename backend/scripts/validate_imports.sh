#!/usr/bin/env bash
# validate_imports.sh — Knowledge Engine schema import validator
# Resolves the "pydantic not installed" error once and for all.
#
# Usage (run from backend/ directory):
#   bash scripts/validate_imports.sh
#
# On first run: creates .venv and installs schema-critical packages (~10s).
# Subsequent runs: uses existing .venv (<2s).

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
VENV="$BACKEND_DIR/.venv"
PYTHON="$VENV/bin/python3"

echo "=== EverydayHoroscope — Backend Import Validator ==="
echo ""

# Step 1: create venv if absent
if [ ! -f "$PYTHON" ]; then
    echo "[1/3] Creating .venv with Python 3.12..."
    python3.12 -m venv "$VENV"
    echo "      .venv created at $VENV"
else
    echo "[1/3] .venv exists — skipping creation."
fi

# Step 2: ensure schema-critical packages are installed
echo "[2/3] Ensuring schema packages are installed..."
"$VENV/bin/pip" install --quiet \
    "pydantic==2.11.3" \
    "pydantic-core==2.33.1" \
    "pymongo==4.6.3" \
    "motor==3.4.0"
echo "      pydantic, pydantic-core, pymongo, motor — OK"

# Step 3: syntax + import check
echo "[3/3] Running import check..."
cd "$BACKEND_DIR"
"$PYTHON" -m py_compile knowledge_schema.py
echo "      Syntax OK"

"$PYTHON" -c "
import sys
sys.path.insert(0, '.')
from knowledge_schema import (
    InterpretationRuleDocument,
    AuthorVoiceDocument,
    NarrativeBridgeDocument,
    ImportBatchDocument,
    CrossScienceCombinationDocument,
    ScienceRegistryDocument,
    UserArcAngelProfileDocument,
    UserContextProfileDocument,
    CaseStudyDocument,
    KnowledgeRequestContext,
    TensionBlock,
    knowledge_collection_models,
    knowledge_index_models,
    ensure_knowledge_indexes,
)
cols = list(knowledge_collection_models().keys())
print(f'      knowledge_schema OK — {len(cols)} collections registered:')
for c in cols:
    print(f'        · {c}')
"

# Also verify knowledge_engine module-level imports (motor must be present)
"$PYTHON" -c "
import sys
sys.path.insert(0, '.')
import motor.motor_asyncio  # hard import — fallback removed now motor is installed
from knowledge_engine import (
    KnowledgeEngine,
    KnowledgeIndexStore,
    extract_chart_facts,
    configure_default_knowledge_engine,
    get_default_knowledge_engine,
    canonical_key,
    normalize_planet_name,
)
print('      knowledge_engine OK — motor present, hard import confirmed')
"

echo ""
echo "=== All checks passed ==="
echo ""
echo "To activate the venv for interactive work:"
echo "  source $VENV/bin/activate"
