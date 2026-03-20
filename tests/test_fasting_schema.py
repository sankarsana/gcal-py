import pytest
import gaurabda

LIPETSK = {'latitude': 52.6088, 'longitude': 39.5992, 'tzname': '+3:00 Europe/Moscow', 'name': 'Lipetsk'}
FAST_DUSK = 0x204  # schema=1 (old): tithi=28, masa=0 → nFastType из колонки fast
FAST_DAY  = 0x207  # schema=0 (new): тот же праздник → nFastType из колонки newfast


@pytest.fixture(autouse=True)
def reset_schema():
    yield
    gaurabda.SetFastingSchema(1)  # сброс к дефолту (old style) после каждого теста


def _fast_for_tithi28_masa0(schema: int) -> int:
    """Возвращает fast для tithi=28 masa=0 (2025-05-11, Липецк) при заданной схеме."""
    gaurabda.SetFastingSchema(schema)
    location = gaurabda.GCLocation(data=LIPETSK)
    date = gaurabda.GCGregorianDate(year=2025, month=5, day=10)
    calendar = gaurabda.TCalendar()
    calendar.CalculateCalendar(location, date, 3)
    for d in calendar.__dict__()['days']:
        if d['astrodata']['tithi'] == 28 and d['astrodata']['masa'] == 0:
            return d['fast']
    raise AssertionError("tithi=28, masa=0 не найден в окне 2025-05-10..12")


def test_schema_diverges_on_tithi28_masa0():
    """Старая и новая схемы дают разные значения fast для одного праздника."""
    assert _fast_for_tithi28_masa0(schema=1) == FAST_DUSK
    assert _fast_for_tithi28_masa0(schema=0) == FAST_DAY


def test_schema_resets_between_tests():
    """Фикстура сбрасывает схему к дефолту (1) между тестами."""
    assert _fast_for_tithi28_masa0(schema=1) == FAST_DUSK
