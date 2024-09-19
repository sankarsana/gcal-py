import os

import gaurabda as gcal
from gaurabda.TToday import unittests


def run():
    # unittests()
    # return

    location = gcal.GCLocation(data={
        'latitude': 52.6088,
        'longitude': 39.5992,
        'tzname': '+3:00 Europe/Moscow',
        'name': 'Lipetsk',
    })
    date = gcal.GCGregorianDate(year=2024, month=9, day=1)

    calendar = gcal.TCalendar()
    calendar.CalculateCalendar(location, date, 90)

    print_calendar(calendar, 'txt')


def print_calendar(calendar, extension='txt'):
    curent_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(curent_dir, "output")
    if not os.path.exists(output_dir): os.mkdir(output_dir)

    file = os.path.join(output_dir, 'calendar.' + extension)

    with open(file, 'wt') as wf: calendar.write(wf, format=out_formats.get(extension))
    # with open(file,'wt') as wf: calendar.write(wf)
    # with open(file,'wt') as wf: calendar.write(wf, layout='table')

    print("Success")


out_formats = {
    'txt': 'plain',
    'json': 'json',
    'rtf': 'rtf',
}

run()
