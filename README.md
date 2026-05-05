# Smart Sensor Gateway

Cloud computing opdracht — Bachelor Elektronica-ICT, VIVES 2025-2026.

## Architectuur

```
┌─────────────┐     MQTT      ┌───────────────┐     HTTP API    ┌───────────────┐
│   app.py    │ ────────────► │   Mosquitto   │ ◄────────────── │   Node-RED    │
│ (simulator) │               │  (port 1884)  │                 │  (port 1881)  │
└─────────────┘               └───────────────┘                 └───────┬───────┘
                                                                         │ InfluxDB Line Protocol
                                                                         ▼
                                                                ┌───────────────┐
                                                                │   InfluxDB    │
                                                                │  (port 8087)  │
                                                                └───────┬───────┘
                                                                         │ Flux queries
                                                                         ▼
                                                                ┌───────────────┐
                                                                │    Grafana    │
                                                                │  (port 3001)  │
                                                                └───────────────┘

Beheer: Portainer (port 9444) — toont status van alle bovenstaande containers.
Netwerk: alle containers communiceren intern via het Docker-netwerk `gateway_net`.
```

### Services

| Container   | Image                        | Externe poort | Rol                              |
|-------------|------------------------------|--------------|----------------------------------|
| `app`       | custom (Python 3.11)         | —            | Simuleert joystick- en knopdata  |
| `mosquitto` | eclipse-mosquitto:2          | 1884         | MQTT broker                      |
| `nodered`   | nodered/node-red:latest      | 1880         | Dataverwerking en validatie       |
| `influxdb`  | influxdb:2.7                 | 8086         | Tijdreeksdatabase                |
| `grafana`   | grafana/grafana:latest       | 3001         | Dashboard                        |
| `portainer` | portainer/portainer-ce:latest| 9444         | Container management             |

### Dataflow

1. **app.py** publiceert elke 5 seconden JSON naar twee MQTT-topics:
   - `sensor/joystick` → `{"x": int, "y": int}` (waarden -100 tot 100)
   - `sensor/buttons` → `{"btn1": 0|1, "btn2": 0|1}`
2. **Node-RED** leest beide topics in via MQTT-in nodes.
3. Voor elk topic valideert een **function node** de data:
   - Controleer of velden aanwezig en van het juiste type zijn.
   - Waarden buiten bereik worden weggegooid (`return null`).
   - Alleen geldige metingen worden doorgestuurd naar InfluxDB.
4. **InfluxDB** slaat de metingen op in de bucket `sensor_data` (org: `sensors`).
5. **Grafana** visualiseert via Flux-queries:
   - Live tijdreeks van joystick x/y en knopstatus.
   - Gemiddelde waarden over de laatste 1 uur en 24 uur.

---

## Installatie

### Vereisten

- Docker Engine ≥ 24
- Docker Compose plugin (ingebouwd in recente Docker-versies)
- Git

### Opstarten — volledige repo

```bash
git clone <repo-url>
cd CloudOpdracht
docker compose up -d
```

De eerste keer worden images gedownload en de `app`-container gebouwd (~2 min).

### Opstarten — enkel met docker-compose.yml

Als je alleen het `docker-compose.yml`-bestand hebt (geen lokale broncode), gebruik dan de pre-built image van Docker Hub. Maak een `.env`-bestand aan naast de compose-file:

```bash
docker compose up -d
```

De image `kobedm/sensor-app:latest` wordt automatisch opgehaald van Docker Hub. Die image wordt gepusht via GitHub Actions bij elke push naar `main`.

### Toegang

| Service    | URL                        | Credentials          |
|------------|----------------------------|----------------------|
| Grafana    | http://localhost:3001       | admin / adminpassword |
| Node-RED   | http://localhost:1880       | —                    |
| InfluxDB   | http://localhost:8086       | admin / adminpassword |
| Portainer  | https://localhost:9444      | (eerste keer instellen) |
| MQTT       | localhost:1884              | anoniem              |

### Stack stoppen

```bash
docker compose down
```

Data blijft bewaard in Docker volumes (`influxdb_data`, `grafana_data`, `node_red_data`).

---

## CI/CD

### Lokaal uitrollen — deploy.sh

`deploy.sh` automatiseert het bijwerken van de stack op de server:

```bash
./deploy.sh
```

Het script doet achtereenvolgens:
1. `docker compose pull` — haalt de nieuwste versies van publieke images op.
2. `docker compose down` — stopt en verwijdert de draaiende containers.
3. `docker compose up -d --build` — herbouwt de `app`-container en start alles opnieuw.

Gebruik dit script na elke wijziging aan `app.py`, `docker-compose.yml` of configuratiebestanden.

### GitHub Actions — automatische image build

Bij elke push naar `main` (of een `v*`-tag) bouwt de workflow in `.github/workflows/` automatisch een nieuwe Docker-image van de `app`-container en pusht die naar Docker Hub.

```
push naar main
      │
      ▼
GitHub Actions: build & push → Docker Hub
      │
      ▼
Op server: ./deploy.sh  (docker compose pull haalt nieuwe image op)
```

In een volledig geautomatiseerde pipeline zou een tool zoals **Watchtower** of een deployment-hook op de server `./deploy.sh` automatisch aanroepen zodra een nieuwe image beschikbaar is, zonder manuele tussenkomst.

---

## Volume backup en restore

Bij migratie naar een nieuwe VM kan de volledige staat (Grafana-dashboards, InfluxDB-data, Node-RED flows) worden meegenomen.

### Backup (oude VM)

```bash
docker compose down
./scripts/backup-volumes.sh
```

Dit maakt `.tar.gz`-bestanden aan in `./backups/`.

### Restore (nieuwe VM)

```bash
# Zet project + backupbestanden op de nieuwe VM
docker compose down
./scripts/restore-volumes.sh
docker compose up -d
```

---

## Reflectie en samenwerking

| Onderdeel                        | Verantwoordelijke |
|----------------------------------|-------------------|
| Docker Compose en containersetup |              |
| Node-RED flows en validatie      |              |
| InfluxDB configuratie            |              |
| Grafana dashboard                |              |
| CI/CD script en GitHub Actions   |              |
| Documentatie                     |              |
