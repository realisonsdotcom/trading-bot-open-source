#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [[ "${USE_NATIVE:-0}" == "1" ]]; then
    "${SCRIPT_DIR}/native_down.sh"
    exit 0
fi

COMPOSE_FILES=(
    "-f" "${PROJECT_ROOT}/infra/docker-compose.yml"
)
if [[ -f "${PROJECT_ROOT}/infra/docker-compose.override.yml" ]]; then
    COMPOSE_FILES+=("-f" "${PROJECT_ROOT}/infra/docker-compose.override.yml")
fi

docker compose --project-directory "${PROJECT_ROOT}" "${COMPOSE_FILES[@]}" down -v
echo "-> dev down."
