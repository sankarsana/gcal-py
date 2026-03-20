import gaurabda
from gaurabda import GCGregorianDate, EARTHDATA
from gaurabda.GCDayData import GCDayData

# Липецк: адхика-маса 2023 — 18 июля по 16 августа
LIPETSK = dict(latitude=52.6088, longitude=39.5992, tzone=3.0, tzid=186)


# --- Unit-level ---

def test_adhika_masa_detected():
    """GCDayData.MasaCalc напрямую: дата в середине адхика-периода (1 авг 2023) даёт nMasa=12."""
    earth = EARTHDATA()
    earth.latitude_deg = LIPETSK['latitude']
    earth.longitude_deg = LIPETSK['longitude']
    earth.tzone = LIPETSK['tzone']
    earth.dst = LIPETSK['tzid']

    date = GCGregorianDate(text='1 Aug 2023')
    astrodata = GCDayData()
    astrodata.DayCalc(date, earth)
    astrodata.MasaCalc(date, earth)

    assert astrodata.nMasa == 12


# --- Integration-level ---

def test_adhika_masa_sequence():
    """В 90-дневном окне (1 июля 2023):
    - есть хотя бы один день с masa==12
    - маса до и после адхика-периода совпадают (masa==3, Ashadha)
    """
    location = gaurabda.GCLocation(data={
        'latitude': LIPETSK['latitude'],
        'longitude': LIPETSK['longitude'],
        'tzname': '+3:00 Europe/Moscow',
        'name': 'Lipetsk',
    })
    date = gaurabda.GCGregorianDate(year=2023, month=7, day=1)

    calendar = gaurabda.TCalendar()
    calendar.CalculateCalendar(location, date, 90)
    days = calendar.__dict__()['days']

    masas = [d['astrodata']['masa'] for d in days]

    adhika_indices = [i for i, m in enumerate(masas) if m == 12]
    assert len(adhika_indices) >= 1, "Адхика-маса не найдена в окне"

    first = adhika_indices[0]
    last = adhika_indices[-1]

    if first > 0 and last < len(masas) - 1:
        masa_before = masas[first - 1]
        masa_after = masas[last + 1]
        assert masa_before == masa_after, (
            f"Маса до ({masa_before}) и после ({masa_after}) адхика-масы должны совпадать"
        )
