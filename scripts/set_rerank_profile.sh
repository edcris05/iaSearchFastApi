#!/usr/bin/env bash
set -euo pipefail

PROFILE="${1:-}"
ENV_FILE="${2:-.env}"

if [[ -z "$PROFILE" ]]; then
  echo "Usage: $0 <movistar|generic> [env_file]"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: env file not found: $ENV_FILE"
  exit 1
fi

case "$PROFILE" in
  movistar)
    VERSION="rerank_v1"
    WEIGHTS='{"semantic":0.88,"margin":0.08,"business":0.04}'
    BOOSTS='{"attr::brand":0.02,"attr::storage":0.015,"attr::color":0.005,"brand::samsung":0.03,"brand::apple":0.025,"storage::256":0.03,"storage::512":0.04,"color::133":0.01,"phrase::5g":0.02,"phrase::cuotas":0.015}'
    ;;
  generic)
    VERSION="rerank_v1"
    WEIGHTS='{"semantic":0.78,"margin":0.07,"business":0.15}'
    BOOSTS='{"attr::brand":0.03,"attr::category":0.04,"attr::price_range":0.02,"attr::availability":0.05,"attr::promo":0.06,"phrase::oferta":0.05,"phrase::envio gratis":0.04,"phrase::premium":0.02}'
    ;;
  *)
    echo "Error: unknown profile '$PROFILE'. Use movistar or generic."
    exit 1
    ;;
esac

set_env_line() {
  local key="$1"
  local value="$2"

  if grep -q "^${key}=" "$ENV_FILE"; then
    sed -i "s|^${key}=.*|${key}='${value}'|" "$ENV_FILE"
  else
    echo "${key}='${value}'" >> "$ENV_FILE"
  fi
}

set_env_line "RETRIEVAL_RERANK_VERSION" "$VERSION"
set_env_line "RETRIEVAL_RERANK_WEIGHTS" "$WEIGHTS"
set_env_line "RETRIEVAL_BUSINESS_BOOSTS" "$BOOSTS"

echo "Applied profile: $PROFILE"
grep -E '^RETRIEVAL_RERANK_VERSION=|^RETRIEVAL_RERANK_WEIGHTS=|^RETRIEVAL_BUSINESS_BOOSTS=' "$ENV_FILE"
