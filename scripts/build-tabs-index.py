#!/usr/bin/env python3
"""Buduje tabs.sqlite z listą plików Guitar Pro znajdujących się w katalogu tabs/.

Plik zawiera indeks (ścieżka względem tabs/, rozmiar, gatunek, pewność gatunku i rok),
a nie zawartość plików, bo katalog ma kilkadziesiąt tysięcy plików. Przeglądarka wczytuje
indeks na starcie, a pojedynczy utwór pobiera dopiero po wybraniu.

Gatunek przypisany jest zespołowi, a rok plikowi. Obie wartości pochodzą z opcjonalnego pliku
tabs-meta.json w katalogu głównym, w postaci:
    {"bands": {"Metallica": {"genre": "Metal", "confidence": "high"}},
     "years": {"Guitar Pro Tabs/M/Metallica/Metallica - Fade To Black.gp3": 1984}}
Brak pliku oznacza puste wartości.

Użycie (z katalogu głównego projektu):
    python3 scripts/build-tabs-index.py
"""

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABS_DIR = ROOT / "tabs"
DB_PATH = ROOT / "tabs.sqlite"
META_PATH = ROOT / "tabs-meta.json"

# Te same rozszerzenia i ukrywanie plików co w index.html (GP_EXTENSIONS, isHidden)
GP_EXTENSIONS = (".gp", ".gp3", ".gp4", ".gp5", ".gpx")

# Dozwolone gatunki; wartości spoza listy są odrzucane, żeby filtr w przeglądarce był spójny
GENRES = (
    "Rock", "Metal", "Punk", "Pop", "Jazz", "Blues", "Folk/Country", "Klasyczna",
    "Latin/World", "Elektroniczna", "Hip-hop/R&B", "Reggae", "Soundtrack", "Inne",
)
CONFIDENCE = ("high", "medium", "low")

# Nazwa pliku ma zwykle postać „Zespół - Tytuł”
BAND_TITLE = re.compile(r"^(.*?) - (.*)$")


def is_hidden(name: str) -> bool:
    return name.startswith(".") or name == "__MACOSX"


def iter_gp_files(base: Path):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if not is_hidden(d))
        for filename in sorted(filenames):
            if is_hidden(filename) or not filename.lower().endswith(GP_EXTENSIONS):
                continue
            full = Path(dirpath) / filename
            yield full.relative_to(base).as_posix(), full.stat().st_size


def band_of(path: str):
    """Zespół z ścieżki: w układzie Kolekcja/Litera/Zespół/plik to nazwa folderu,
    w płaskim układzie to część nazwy pliku przed ' - '. Ta sama logika jest w index.html."""
    parts = path.split("/")
    fname = parts[-1].rsplit(".", 1)[0]
    if len(parts) == 4:
        return parts[2]
    m = BAND_TITLE.match(fname)
    return m.group(1) if m else None


def load_meta():
    if not META_PATH.is_file():
        return {}, {}

    data = json.loads(META_PATH.read_text(encoding="utf-8"))
    return data.get("bands", {}), data.get("years", {})


def main() -> int:
    if not TABS_DIR.is_dir():
        print(f"Brak katalogu {TABS_DIR}", file=sys.stderr)
        return 1

    songs = list(iter_gp_files(TABS_DIR))
    bands, years = load_meta()

    rows = []
    for path, size in songs:
        info = bands.get(band_of(path)) or {}
        genre = info.get("genre") if info.get("genre") in GENRES else None
        confidence = info.get("confidence") if genre and info.get("confidence") in CONFIDENCE else None
        year = years.get(path)
        rows.append((path, size, genre, confidence, year if isinstance(year, int) else None))

    tmp_path = DB_PATH.with_suffix(".sqlite.tmp")
    if tmp_path.exists():
        tmp_path.unlink()

    con = sqlite3.connect(tmp_path)
    try:
        con.execute(
            "CREATE TABLE songs ("
            "path TEXT PRIMARY KEY, size INTEGER NOT NULL, "
            "genre TEXT, genre_confidence TEXT, year INTEGER)"
        )
        con.executemany(
            "INSERT INTO songs (path, size, genre, genre_confidence, year) VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        con.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        con.execute(
            "INSERT INTO meta (key, value) VALUES ('built_at', datetime('now')), ('count', ?)",
            (str(len(rows)),),
        )
        con.commit()
    finally:
        con.close()

    # Zapis przez plik tymczasowy, żeby przeglądarka nie dostała uciętej bazy podczas przebudowy
    os.replace(tmp_path, DB_PATH)
    with_genre = sum(1 for r in rows if r[2])
    with_year = sum(1 for r in rows if r[4])
    print(f"Zapisano {len(rows)} plików do {DB_PATH} (z gatunkiem: {with_genre}, z rokiem: {with_year})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
