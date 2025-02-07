#!/bin/bash
set -euo pipefail

if ! command -v uv; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
