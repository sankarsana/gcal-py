import json

import pytest

import gaurabda


def test_calenar_lipetsk_year():
    location = gaurabda.GCLocation(data={
        'latitude': 52.6088,
        'longitude': 39.5992,
        'tzname': '+3:00 Europe/Moscow',
        'name': 'Lipetsk',
    })
    date = gaurabda.GCGregorianDate(year=2024, month=9, day=1)
    with open('tests/calendar_lipetsk_year.json', 'r') as f:
        expected = json.load(f)

    calendar = gaurabda.TCalendar()
    calendar.CalculateCalendar(location, date, 365)
    result = calendar.__dict__()

    assert result['location'] == expected['location']
    assert result['start'] == expected['start']
    assert result['count'] == expected['count']

    for i, day in enumerate(result['days']):
        day_expected = expected['days'][i]
        assert day['date'] == day_expected['date']
        assert day['ekadashiName'] == day_expected['ekadashiName']
        assert day['ekadashiType'] == day_expected['ekadashiType']
        assert day['fast'] == day_expected['fast']
        assert day['feasting'] == day_expected['feasting']
        assert day['hasDST'] == day_expected['hasDST']

        astrodata = day['astrodata']
        astrodata_expected = day_expected['astrodata']
        assert astrodata['ayanamsha'] == astrodata_expected['ayanamsha']
        assert astrodata['gaurabda_year'] == astrodata_expected['gaurabda_year']
        assert astrodata['julianDay'] == pytest.approx(astrodata_expected['julianDay'], rel=1e-6)
        assert astrodata['masa'] == astrodata_expected['masa']
        assert astrodata['moon_rasi'] == astrodata_expected['moon_rasi']
        assert astrodata['naksatra'] == astrodata_expected['naksatra']
        assert astrodata['naksatraElapse'] == pytest.approx(astrodata_expected['naksatraElapse'], rel=1e-6)
        assert astrodata['sun_rasi'] == astrodata_expected['sun_rasi']
        assert astrodata['tithi'] == astrodata_expected['tithi']
        assert astrodata['tithiElapse'] == astrodata_expected['tithiElapse']
        assert astrodata['yoga'] == astrodata_expected['yoga']

        sun = astrodata['sun']
        sun_expected = astrodata_expected['sun']
        assert sun['noon'] == sun_expected['noon']
        assert sun['rise'] == sun_expected['rise']
        assert sun['set'] == sun_expected['set']
        assert sun['noon_deg'] == pytest.approx(sun_expected['noon_deg'], rel=1e-6)
        assert sun['rise_deg'] == pytest.approx(sun_expected['rise_deg'], rel=1e-6)
        assert sun['set_deg'] == pytest.approx(sun_expected['set_deg'], rel=1e-6)

        events = day['events']
        events_expected = day_expected['events']
        assert len(events) == len(events_expected)
        for n, event in enumerate(events):
            event_expected = events_expected[n]
            assert event['disp'] == event_expected['disp']
            assert event['prio'] == event_expected['prio']
            assert event['text'] == event_expected['text']
