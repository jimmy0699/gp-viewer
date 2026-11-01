# GP Viewer

Przeglądarkowa aplikacja do przeglądania, odtwarzania i drukowania zapisów Guitar Pro — bez instalacji i bez serwera. Wystarczy otworzyć `index.html` w przeglądarce.

## Funkcje

- Otwieranie pojedynczych plików lub całego folderu (przycisk albo przeciągnięcie plików na okno).
- Obsługa formatów: `.gp3`, `.gp4`, `.gp5`, `.gpx`, `.gp` (GP7).
- Tryby wyświetlania: **Nuty**, **Tabulatura**, **Nuty + tab**.
- Wyszukiwarka utworów w panelu bocznym z listą plików.
- Panel **Ścieżki** obok partytury: pokazywanie, wyciszanie i solo każdej ścieżki oraz jej głośność. Przycisk **Ścieżki** w pasku narzędzi chowa panel; na telefonie panel jest pod partyturą.
- Odtwarzanie z wbudowanym brzmieniem (SoundFont), pasek pozycji i regulacja tempa (50%–125%).
- Drukowanie partytury.

## Uruchomienie

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/jimmy0699/gp-viewer.git
   cd gp-viewer
   ```
2. Umieść pliki Guitar Pro w katalogu `tabs/` (katalog jest ignorowany przez git).
3. Zbuduj indeks biblioteki (wymaga Python 3, bez dodatkowych pakietów):
   ```bash
   python3 scripts/build-tabs-index.py
   ```
   Powstaje plik `tabs.sqlite` z listą wszystkich plików `.gp*` z `tabs/`. Po każdej zmianie w katalogu uruchom skrypt ponownie.
4. Otwórz aplikację z serwera, np. `python3 -m http.server 8000` i wejdź na `http://localhost:8000`, albo przez Herd (`http://gp-viewer.test`). Sama otwarta strona z dysku (`file://`) nie wczyta biblioteki z `tabs.sqlite`.

Biblioteka [alphaTab](https://www.alphatab.net/), SoundFont i [sql.js](https://sql.js.org/) są ładowane z CDN, więc do odtwarzania i renderowania potrzebne jest połączenie z internetem.

Na starcie aplikacja wczytuje indeks z `tabs.sqlite`, a plik pobiera dopiero po wybraniu utworu. Przyciski **Otwórz pliki…** i **Otwórz folder…** oraz przeciąganie nadal działają i zastępują bieżącą listę.

## Użycie

- **Otwórz pliki…** — wybierz jeden lub kilka plików Guitar Pro.
- **Otwórz folder…** — wczytaj cały folder; aplikacja odnajdzie w nim pliki Guitar Pro.
- Przeciągnij pliki lub folder bezpośrednio na okno aplikacji.
- **Odtwórz / Zatrzymaj** — sterowanie odtwarzaniem; suwak pozwala przejść do dowolnego miejsca w utworze.
- **Tempo** — zmiana prędkości odtwarzania bez zmiany wysokości dźwięku.
- **Drukuj** — wydruk aktualnie wyświetlanej partytury.

## Struktura

```
gp-viewer/
├── index.html                  # cała aplikacja (HTML, CSS i JavaScript w jednym pliku)
├── scripts/
│   └── build-tabs-index.py     # buduje tabs.sqlite z zawartości tabs/
├── tabs/                       # pliki Guitar Pro (poza git)
├── tabs.sqlite                 # indeks biblioteki (generowany, poza git)
└── README.md
```

## Technologie

- HTML, CSS, vanilla JavaScript
- [sql.js](https://sql.js.org/) 1.10.3 — odczyt indeksu `tabs.sqlite` w przeglądarce
- Python 3 (tylko biblioteka standardowa) — skrypt budujący indeks
- [alphaTab](https://www.alphatab.net/) 1.8.4 — renderowanie nut i tablatur, odtwarzanie MIDI
- SoundFont `sonivox.sf3` z pakietu alphaTab

## Prywatność

Pliki są czytane lokalnie w przeglądarce i nigdzie nie są wysyłane. Żądania sieciowe dotyczą biblioteki alphaTab, SoundFontu i sql.js (CDN) oraz plików `tabs.sqlite` i `tabs/` z Twojego serwera.

## Licencja

Brak określonej licencji. Skontaktuj się z autorem przed ponownym wykorzystaniem kodu.
