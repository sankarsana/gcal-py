import json

import gaurabda


def test_calenar_lipetsk_year():
    location = gaurabda.GCLocation(data={
        'latitude': 52.6088,
        'longitude': 39.5992,
        'tzname': '+3:00 Europe/Moscow',
        'name': 'Lipetsk',
    })
    date = gaurabda.GCGregorianDate(year=2024, month=9, day=1)

    calendar = gaurabda.TCalendar()
    calendar.CalculateCalendar(location, date, 365)
    result = calendar.__dict__()
    with open('tests/calendar_lipetsk_year.json', 'r') as f:
        expected = json.load(f)

    assert result == expected