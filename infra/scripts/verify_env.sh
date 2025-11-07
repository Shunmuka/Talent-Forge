#!/usr/bin/env bash
set -euo pipefail

missing=()
for var in DATABASE_URL NEXT_PUBLIC_API_BASE_URL OPENAI_API_KEY; do
  if [[ -z "${!var:-}" ]]; then
    missing+=("$var")
  fi
done

if ((${#missing[@]} == 0)); then
  echo "All required env vars are set."
else
  echo "Missing env vars:"
  for var in "${missing[@]}"; do
    echo " - $var"
  done
  echo "Please update your .env file; script exits with success to stay non-blocking."
fi
