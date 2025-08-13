#!/usr/bin/env bash
set -euo pipefail

python -m app.migrate || true
exec "$@"