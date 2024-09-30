import gaurabda
from gaurabda import GCGregorianDate, EARTHDATA
from gaurabda.GCDayData import GCDayData


def test_masa():
    earth = EARTHDATA()
    earth.latitude_deg = 52.6088
    earth.longitude_deg = 39.5992
    earth.tzone = 3.0
    earth.dst = 297

    date = GCGregorianDate(text='22 Jun 2024')
    astrodata = GCDayData()

    astrodata.MasaCalc(date, earth)

    assert astrodata.nMasa == 1