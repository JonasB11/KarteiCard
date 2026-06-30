# KarteiCard

KarteiCard ist eine kleine Karteikarten-App mit Docker, Flask und MySQL. Du kannst Karten erstellen, nach Kategorien sortieren, im Lernmodus wiederholen und im Quizmodus Multiple-Choice-Fragen beantworten.

## Funktionen

- Karteikarten mit Frage, Antwort und Kategorie erstellen
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
question,answer,category
"Was ist 2+2?","4","Mathe"
```

`category` ist optional. Wenn sie fehlt oder leer ist, wird `Allgemein` verwendet.
