# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`gaurabda` — Python-библиотека для расчёта календаря Гаурабда (Гаудия-Вайшнавский лунный календарь). Выполняет астрономические расчёты (тити, накшатры, йоги, санкранти) и накладывает религиозные события/посты по традиции ИСККОН.

## Tests

| Файл | Что тестирует |
|------|---------------|
| `tests/calendar_lipetsk_year.py` | Интеграционный: 365 дней, Липецк, golden reference JSON (2024/2025/2026) |
| `tests/test_masa.py` | Unit: `GCDayData.MasaCalc` напрямую |
| `tests/test_adhika_masa.py` | Unit + интеграция адхика-масы (~раз в 2.5 года) |
| `tests/test_fasting_schema.py` | `SetFastingSchema()` — глобальное состояние, изоляция между тестами |
| `tests/test_polar.py` | Полярные локации без восхода/захода (Мурманск, декабрь) |

## Commands

```bash
# Все тесты
python -m pytest tests/

# Один файл
python -m pytest tests/test_masa.py

# Один тест по имени
python -m pytest tests/test_adhika_masa.py::test_adhika_masa_detected

# Запуск примера (генерирует календарь для Липецка)
python app/run.py

# REST API сервер (порт 8047)
python server/server.py
```

## Architecture

### Entry points
- **`gaurabda/__init__.py`** — публичный API: `TCalendar`, `GCLocation`, `GCGregorianDate`, `FindLocation`, `GetCountries`, `SetFastingSchema` и др.
- **`server/server.py`** → **`gaurabda/TServer.py`** — Flask REST API с тремя эндпоинтами: `/countries`, `/find-location`, `/calendar`

### Calculation pipeline
1. `TCalendar.CalculateCalendar()` — оркестратор, запускает расчёт на диапазон дат с 8-дневным буфером
2. `GCDayData` — контейнер астрономических данных (позиции солнца/луны)
3. `GCSunData` / `GCMoonData` — расчёт восхода/захода, долгот
4. `GCTithi` / `GCNaksatra` / `GCRasi` / `GCYoga` / `GCSankranti` — расчёт элементов лунного календаря
5. `TCoreEvents` + `GCEventList` — наложение религиозных событий и правил поста
6. `GCCalendarDay` — итоговый объект одного дня

### Unit-тестирование на низком уровне

Для прямого тестирования астро-расчётов без `TCalendar`:

```python
from gaurabda import GCGregorianDate, EARTHDATA
from gaurabda.GCDayData import GCDayData

earth = EARTHDATA()
earth.latitude_deg = 52.6088
earth.longitude_deg = 39.5992
earth.tzone = 3.0
earth.dst = 297  # tzid из locations.json

date = GCGregorianDate(text='22 Jun 2024')
astrodata = GCDayData()
astrodata.DayCalc(date, earth)   # солнце, луна, тити, накшатра, йога
astrodata.MasaCalc(date, earth)  # маса (вызывать после DayCalc)
```

### Key data
- `gaurabda/res/locations.json` — база ~1000+ городов мира
- `gaurabda/res/events.json` + `eventfast.json` — определения праздников и постов
- `gaurabda/res/strings.json` — локализация
- Эталонные данные тестов: `tests/calendar_lipetsk_year.json`

### Output formats
`TCalendar.write()` поддерживает: plain text, HTML, RTF, XML, JSON.

### Important details
- Библиотека — чистый Python без внешних зависимостей (Python ≥ 3.4). Flask нужен только для сервера.
- `SetFastingSchema()` меняет **глобальное состояние** (`GCDisplaySettings`). В тестах сбрасывать через `pytest.fixture(autouse=True)`.
- Вывод результатов: `TCalendar.CalculateCalendar(...)` затем `calendar.__dict__()` → JSON-совместимый словарь.
