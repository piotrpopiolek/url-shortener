# API do skracania URL-i

## Opis

Serwis pozwala zamieniać długie adresy url na krótkie i odwrotnie. Krótki adres przekieruje do pierwotnego adresu url.

## Uruchomienie

```powershell
docker compose up --build
```

API jest na `http://localhost:8005`. W kontenerze aplikacja słucha portu 8000, na hoście jest wystawiona jako 8005. Baza Postgresa z hosta jest na porcie 5435.

Na produkcji `SECRET_KEY` musi przyjść ze zmiennej środowiskowej. Domyślna wartość `long_secret_key_randomly_generated` służy tylko do lokalnego uruchomienia.

## API

| Metoda i ścieżka | Wejście | Sukces | Błędy |
| --- | --- | --- | --- |
| `POST /api/shorten/` | `{"url": "http://example.com/very-very/long/url/even-longer"}` | `201` `{"code", "short_url", "url"}` | `400` zły URL, `503` brak wolnego kodu |
| `POST /api/expand/` | `{"short_url": "http://localhost:8005/shrt/aB3xY9z"}` | `200` `{"url": "..."}` | `400` zły format, `404` nieznany kod |
| `GET /shrt/<code>` | — | `302`, nagłówek `Location` | `404` nieznany kod |

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8005/api/shorten/ -ContentType 'application/json' -Body '{"url": "http://example.com/very-very/long/url/even-longer"}'
Invoke-RestMethod -Method Post -Uri http://localhost:8005/api/expand/ -ContentType 'application/json' -Body '{"short_url": "http://localhost:8005/shrt/<kod>"}'
curl.exe -i http://localhost:8005/shrt/<kod>
```

## Testy

```powershell
docker compose up -d db
uv sync
uv run pytest
uv run pytest -m "not e2e" -v
uv run pytest -m e2e -v
```

Testy jednostkowe obejmują testy własnych funkcji: generowania kodu i poprawności kodu. Testy serwisu obejmują zapis/odczyt i obsługę kolizji. Kolejne testy jednostkowe walidują schematy url, adresy url oraz ciało dla metody POST. Ostatnie testy e2e testują cały flow na żywym serwerze HTTP.

## Jakość

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```
Wymuszane jest silne typowanie mypy --strict.

## Niejasności i decyzje

1. **Format kodu.** Niejasny był przykładowy kod `%5C%60`: to zakodowane znaki `\` i `` ` ``. Uznałem to za literówkę. Przyjąłem 7-znakowe kody z `a-zA-Z0-9`, z zapasem do 16 znaków w modelu.
2. **Kolizje.** API obsługuje kolizje i podejmuje do 5 prób wygenerowania unikalnego kodu, po piątej próbie zwraca błąd 503.
3. **Ten sam URL.** Ten sam długi adres dostaje nowy kod. Eliminuje w ten sposób problem wyścigu, że adres jest już w bazie.
4. **Rozwinięcie.** `POST /api/expand/` oddaje oryginał w JSON-ie. `GET /shrt/<code>` przekierowuje przeglądarkę na ten sam adres.
5. **302, nie 301.** Serwis przekierowuje z kodem 302, aby przy następnym wejściu w skrócony link zapytanie przechodziło przez serwer.
6. **Host przy rozwijaniu.** Host jest ignorowany, weryfikowana jest ścieżka z przedrostkiem `/shrt/<code>`.
7. **Walidacja URL-a.** Dozwolone są schematy http i https, maksymalna długość linku to 2048.
8. **Końcowy ukośnik.** Nie jest dopuszczalny końcowy ukośnik w skróconym linku.

## Świadomie pominięte

Serwis nie posiada żadnej autoryzacji, analityki, limitów zapytań.
