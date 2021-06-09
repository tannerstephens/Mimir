#!/bin/bash
set -euo pipefail

flask db upgrade

echo "Starting "
