#!/bin/bash

set -euo pipefail

TORCH_BASE_URL="${TORCH_BASE_URL:-http://localhost:8086}"
TARGET_SERVER="${TARGET_SERVER:-http://localhost:8082/fhir}"
EXPORT_ID=""
TRANSFER_FOLDER="extraction-transfer"

while getopts "e:" opt; do
  case $opt in
    e) EXPORT_ID="$OPTARG" ;;
    *) echo "Usage: $0 -e <export_id>" >&2; exit 1 ;;
  esac
done

if [[ -z "$EXPORT_ID" ]]; then
  echo "❌ Export ID is required (-e)" >&2
  exit 1
fi

process_file() {
  local url="$1"
  local filename="$TRANSFER_FOLDER/$(basename "$url")"

  echo "➡️  Processing: $filename"

  if curl -s -o "$filename" "$url"; then
    echo "⬆️  Uploading $filename with blazectl..."
    if blazectl upload --server "$TARGET_SERVER" "$TRANSFER_FOLDER"; then
      echo "🗑️  Deleting $filename..."
      rm -f "$filename"
    else
      echo "❌ Upload failed for $filename" >&2
      echo "🗑️  Deleting $filename..."
      rm -f "$filename"
    fi
  else
    echo "❌ Download failed for $filename" >&2
  fi
}

EXPORT_STATUS_URL="${TORCH_BASE_URL%/}/fhir/__status/${EXPORT_ID#/}"
echo "Using export status URL: $EXPORT_STATUS_URL"

export_json=$(curl -s "$EXPORT_STATUS_URL")

urls=()
while IFS= read -r url; do
  urls+=("$url")
done < <(echo "$export_json" | jq -r '.output[].url')

if [[ ${#urls[@]} -eq 0 ]]; then
  echo "⚠️  No NDJSON URLs found in export metadata." >&2
  exit 1
fi



for url in "${urls[@]}"; do
  if [[ "$url" == *core.ndjson ]]; then
    process_file "$url"
    break
  fi
done

# Then process all remaining files
for url in "${urls[@]}"; do
  if [[ "$url" != *core.ndjson ]]; then
    process_file "$url"
  fi
done

echo "✅ Extraction transfer to fhir server completed"
