#!/usr/bin/env bash
set -euo pipefail

# Back up persistent volumes so a new VM can be restored with the same state.
# Includes Grafana users/password hash, dashboards, datasources, Node-RED flows,
# credentials and InfluxDB storage.

BACKUP_DIR="${1:-./backups}"

INFLUX_VOL="${INFLUX_VOL:-cloudopdracht_influxdb_data}"
NODERED_VOL="${NODERED_VOL:-cloudopdracht_node_red_data}"
GRAFANA_VOL="${GRAFANA_VOL:-cloudopdracht_grafana_data}"

mkdir -p "$BACKUP_DIR"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

backup_volume() {
  local volume_name="$1"
  local out_file="$2"
  echo "Backing up ${volume_name} -> ${out_file}"
  docker run --rm \
    -v "${volume_name}:/from" \
    -v "${PWD}/${BACKUP_DIR}:/backup" \
    alpine:3.20 \
    sh -c "tar czf /backup/${out_file} -C /from ."
}

backup_volume "$INFLUX_VOL" "influxdb_data-${TIMESTAMP}.tar.gz"
backup_volume "$NODERED_VOL" "nodered_data-${TIMESTAMP}.tar.gz"
backup_volume "$GRAFANA_VOL" "grafana_data-${TIMESTAMP}.tar.gz"

echo "Done. Backup files created in ${BACKUP_DIR}"
ls -lh "$BACKUP_DIR"
