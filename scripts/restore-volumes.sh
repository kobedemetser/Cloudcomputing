#!/usr/bin/env bash
set -euo pipefail

# Restore persistent volumes on a new VM from backup tar files.
# This reproduces Grafana login, dashboards, datasources, Node-RED flows,
# credentials and InfluxDB storage.

BACKUP_DIR="${1:-./backups}"

INFLUX_VOL="${INFLUX_VOL:-cloudopdracht_influxdb_data}"
NODERED_VOL="${NODERED_VOL:-cloudopdracht_node_red_data}"
GRAFANA_VOL="${GRAFANA_VOL:-cloudopdracht_grafana_data}"

INFLUX_FILE="${INFLUX_FILE:-}"
NODERED_FILE="${NODERED_FILE:-}"
GRAFANA_FILE="${GRAFANA_FILE:-}"

pick_latest() {
  local pattern="$1"
  ls -1t "$BACKUP_DIR"/$pattern 2>/dev/null | head -n 1 || true
}

if [[ -z "$INFLUX_FILE" ]]; then
  INFLUX_FILE="$(pick_latest 'influxdb_data-*.tar.gz')"
fi
if [[ -z "$NODERED_FILE" ]]; then
  NODERED_FILE="$(pick_latest 'nodered_data-*.tar.gz')"
fi
if [[ -z "$GRAFANA_FILE" ]]; then
  GRAFANA_FILE="$(pick_latest 'grafana_data-*.tar.gz')"
fi

if [[ -z "$INFLUX_FILE" || -z "$NODERED_FILE" || -z "$GRAFANA_FILE" ]]; then
  echo "Missing backup files."
  echo "Expected in $BACKUP_DIR:"
  echo "- influxdb_data-*.tar.gz"
  echo "- nodered_data-*.tar.gz"
  echo "- grafana_data-*.tar.gz"
  exit 1
fi

create_volume_if_missing() {
  local volume_name="$1"
  if ! docker volume inspect "$volume_name" >/dev/null 2>&1; then
    docker volume create "$volume_name" >/dev/null
  fi
}

restore_volume() {
  local volume_name="$1"
  local backup_file="$2"

  echo "Restoring ${backup_file} -> ${volume_name}"
  create_volume_if_missing "$volume_name"

  docker run --rm \
    -v "${volume_name}:/to" \
    -v "${PWD}/${BACKUP_DIR}:/backup" \
    alpine:3.20 \
    sh -c "rm -rf /to/* /to/.[!.]* /to/..?* 2>/dev/null || true; tar xzf /backup/$(basename "$backup_file") -C /to"
}

restore_volume "$INFLUX_VOL" "$INFLUX_FILE"
restore_volume "$NODERED_VOL" "$NODERED_FILE"
restore_volume "$GRAFANA_VOL" "$GRAFANA_FILE"

echo "Restore complete. Start stack with: docker compose up -d"
