# Imposter Game - Django Channels Setup

This project implements a multiplayer party game (Imposter) using Django, Django Channels (Websockets), and Tailwind CSS.

## Features
- Spieler können Räume erstellen und beitreten
- Nach Spielstart erhalten alle bis auf einen Spieler ein Wort (der Imposter bekommt kein Wort)
- Live-Kommunikation über Websockets
- Modernes UI mit Tailwind CSS

## Setup

1. **Installierte Abhängigkeiten:**
   - Django
   - channels
   - channels_redis
   - daphne

2. **Frontend:**
   - Tailwind CSS (wird noch eingerichtet)

3. **Starten des Servers:**
   ```
   E:/Entwicklung/imposter-game/.venv/Scripts/python.exe manage.py runserver
   ```

4. **Starten mit Daphne (für Websockets):**
   ```
   E:/Entwicklung/imposter-game/.venv/Scripts/python.exe -m daphne imposter_game.asgi:application
   ```

## Nächste Schritte
- Django-Projekt und App anlegen
- Channels konfigurieren
- Tailwind CSS einrichten
- Spiel- und Raum-Logik implementieren
