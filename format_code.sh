#! /bin/bash
set -euo pipefail
SOURCE_FILE="$(basename "${0%.*}").txt"
sh -c "$(cat "${SOURCE_FILE}")"
