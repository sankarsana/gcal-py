import gaurabda

MURMANSK = {
    'latitude': 68.9585,
    'longitude': 33.0827,
    'tzname': '+3:00 Europe/Moscow',
    'name': 'Murmansk',
}


def _run(days=30):
    location = gaurabda.GCLocation(data=MURMANSK)
    date = gaurabda.GCGregorianDate(year=2024, month=12, day=15)
    calendar = gaurabda.TCalendar()
    calendar.CalculateCalendar(location, date, days)
    return calendar.__dict__()['days']


def test_polar_no_crash():
    """CalculateCalendar для полярной локации в зимний период не крашится."""
    days = _run()
    assert len(days) == 30


def test_polar_night_sentinel():
    """В декабре в Мурманске хотя бы часть дней имеет sun.rise_deg < 0 (полярная ночь)."""
    days = _run()
    polar = [d for d in days if d['astrodata']['sun']['rise_deg'] < 0]
    assert len(polar) > 0, "Ожидаются дни без восхода (полярная ночь)"


def test_polar_tithi_valid():
    """Тити вычисляются корректно (0–29) даже для дней без восхода."""
    days = _run()
    polar = [d for d in days if d['astrodata']['sun']['rise_deg'] < 0]
    for d in polar:
        tithi = d['astrodata']['tithi']
        assert 0 <= tithi <= 29, f"Тити {tithi} вне диапазона для полярного дня"
