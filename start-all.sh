COMPOSE_PROJECT=${DSE_EXAMPLE_COMPOSE_PROJECT:-dse-example}
BASE_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 || exit 1 ; pwd -P )"

COMPOSE_IGNORE_ORPHANS=True docker compose -p "$COMPOSE_PROJECT" -f "$BASE_DIR"/vfps/docker-compose.yml up -d
COMPOSE_IGNORE_ORPHANS=True docker compose -p "$COMPOSE_PROJECT" -f "$BASE_DIR"/fhir-pseudonymizer/docker-compose.yml up -d
COMPOSE_IGNORE_ORPHANS=True docker compose -p "$COMPOSE_PROJECT" -f "$BASE_DIR"/fhir-server/docker-compose.yml up -d
COMPOSE_IGNORE_ORPHANS=True docker compose -p "$COMPOSE_PROJECT" -f "$BASE_DIR"/torch/docker-compose.yml up -d
