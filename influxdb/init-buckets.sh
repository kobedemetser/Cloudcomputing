#!/bin/bash
influx bucket create \
  --name crypto_bucket \
  --org "${DOCKER_INFLUXDB_INIT_ORG}" \
  --token "${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}"
