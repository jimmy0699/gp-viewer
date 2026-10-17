# GP Viewer

Przeglądarkowa aplikacja do przeglądania, odtwarzania i drukowania zapisów Guitar Pro — bez instalacji i bez serwera. Wystarczy otworzyć `index.html` w przeglądarce.

## Funkcje

- Otwieranie pojedynczych plików lub całego folderu (przycisk albo przeciągnięcie plików na okno).
- Obsługa formatów: `.gp3`, `.gp4`, `.gp5`, `.gpx`, `.gp` (GP7).
- Tryby wyświetlania: **Nuty**, **Tabulatura**, **Nuty + tab**.
- Wyszukiwarka utworów w panelu bocznym z listą plików i ścieżek.
- Odtwarzanie z wbudowanym brzmieniem (SoundFont), pasek pozycji i regulacja tempa (50%–125%).
- Drukowanie partytury.

## Uruchomienie

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/jimmy0699/gp-viewer.git
   cd gp-viewer
   ```
2. Otwórz `index.html` w przeglądarce (Chrome, Firefox, Safari, Edge).

Nie ma etapu budowania ani zależności do zainstalowania lokalnie. Biblioteka [alphaTab](https://www.alphatab.net/) oraz SoundFont są ładowane z CDN (jsDelivr), więc do odtwarzania i renderowania potrzebne jest połączenie z internetem.

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
├── index.html   # cała aplikacja (HTML, CSS i JavaScript w jednym pliku)
└── README.md
```

## Technologie

- HTML, CSS, vanilla JavaScript
- [alphaTab](https://www.alphatab.net/) 1.8.4 — renderowanie nut i tablatur, odtwarzanie MIDI
- SoundFont `sonivox.sf3` z pakietu alphaTab

## Prywatność

Pliki są wczytywane lokalnie w przeglądarce i nigdzie nie są wysyłane. Jedyne żądania sieciowe dotyczą biblioteki alphaTab i SoundFontu.

## Licencja

Brak określonej licencji. Skontaktuj się z autorem przed ponownym wykorzystaniem kodu.
