# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`gaurabda` — Python-библиотека для расчёта календаря Гаурабда (Гаудия-Вайшнавский лунный календарь). Выполняет астрономические расчёты (тити, накшатры, йоги, санкранти) и накладывает религиозные события/посты по традиции ИСККОН.

## Commands

```bash
# Тесты
python -m pytest tests/calendar_lipetsk_year.py

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

### Key data
- `gaurabda/res/locations.json` — база ~1000+ городов мира
- `gaurabda/res/events.json` + `eventfast.json` — определения праздников и постов
- `gaurabda/res/strings.json` — локализация
- Эталонные данные тестов: `tests/calendar_lipetsk_year.json`

### Output formats
`TCalendar.write()` поддерживает: plain text, HTML, RTF, XML, JSON.

### Important detail
Библиотека чистый Python без внешних зависимостей (Python ≥ 3.4). Flask нужен только для сервера.
