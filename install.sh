#!/usr/bin/env bash
# =============================================================================
# FDE Harness + BMAD Automated Installer for Existing Client Repositories
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/valuefirst/fde-harness/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/valuefirst/fde-harness/main/install.sh | bash -s -- --client "ClientName"
# =============================================================================

set -e

CLIENT_NAME="Enterprise-Client"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --client|-c) CLIENT_NAME="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "🚀 Installing FDE Harness & BMAD into current repository for: $CLIENT_NAME"

# 1. Ensure Python 3.10+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is required but not installed."
    exit 1
fi

# 2. Install fde-harness package
echo "📦 Installing fde-harness from GitHub..."
python3 -m pip install --quiet --upgrade git+https://github.com/valuefirst/fde-harness.git

# 3. Run automated project bootstrapping
echo "⚙️  Bootstrapping agent governance, BMAD skills, and telemetry..."
fde-harness init --client "$CLIENT_NAME"

echo ""
echo "🎉 FDE Harness successfully provisioned in $(pwd)!"
echo "👉 Now commit the files: git add .agent _bmad AGENTS.md .gitignore && git commit -m 'feat: install FDE Harness + BMAD'"
