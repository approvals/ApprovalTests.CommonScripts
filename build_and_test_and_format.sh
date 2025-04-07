#! /bin/bash
set -euo pipefail

./format_code.sh
./build-and-test
