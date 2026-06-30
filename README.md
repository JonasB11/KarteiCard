# KarteiCard

KarteiCard ist eine kleine Karteikarten-App mit Docker, Flask und MySQL. Sie ist besonders für IT-Themen gedacht: Du kannst zu jeder Karte neben Frage und Antwort auch Beispiele wie Commands, Code-Snippets oder Praxisfälle speichern.

## Funktionen

- Karteikarten mit Frage, Antwort, Beispiel und Kategorie erstellen
- Karten dauerhaft in MySQL speichern
- Lernmodus mit Antwort-Aufdecken und Statistik
- Quizmodus mit gemischten Antwortoptionen
- CSV-Import und CSV-Export für Karteikarten
- Docker-Compose-Setup für App und Datenbank

## Starten

```bash
cp .env.example .env
docker compose up --build
```

Danach ist die App unter `http://localhost:5001` erreichbar.

## Konfiguration

Die wichtigsten Variablen stehen in `.env.example`:

- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_ROOT_PASSWORD`
- `DATABASE_URL`
- `FLASK_SECRET_KEY`

## Entwicklung

Die Datenbanktabellen werden beim Start der App automatisch angelegt. Die MySQL-Daten bleiben im Docker-Volume `mysql_data` erhalten.

## CSV-Format

Für den Import braucht die CSV-Datei mindestens diese Spalten:

```csv
question,answer,examples,category
"Was macht chmod +x?","Macht eine Datei ausführbar.","chmod +x deploy.sh","Linux"
```

`examples` und `category` sind optional. Wenn `category` fehlt oder leer ist, wird `Allgemein` verwendet.
