# Cloudcomputing
opdracht cloud computing

## Exacte clone naar nieuwe VM (Grafana + InfluxDB + Node-RED)

Als je op een nieuwe VM exact dezelfde omgeving wil (inclusief Grafana login, dashboards, datasources, Node-RED flows en InfluxDB data), gebruik volume backup/restore.

Gebruik hiervoor:

1. `scripts/backup-volumes.sh` op de oude VM
2. `scripts/restore-volumes.sh` op de nieuwe VM

### Op oude VM

1. `docker compose down`
2. `./scripts/backup-volumes.sh`

Dit maakt tar.gz backups in `./backups`.

### Op nieuwe VM

1. Zet project + backupbestanden op de nieuwe VM
2. `docker compose down`
3. `./scripts/restore-volumes.sh`
4. `docker compose up -d`

## Moet dit via GitHub of in image?

Niet via GitHub commits en niet in de image voor runtime-data.

Reden:

1. Runtime-data bevat gevoelige info (credentials, tokens, gebruikersdata)
2. Images moeten applicatie bevatten, niet veranderlijke productie-data
3. GitHub is goed voor code en build pipelines, niet als data snapshot store

GitHub Actions gebruik je wel voor automatisch build/push van images.
Data migratie blijft via volume backup/restore.
