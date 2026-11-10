from datetime import date
from pathlib import Path
import calendar
import re

DOB = date(2003, 3, 10)
SVG_PATH = Path('terminal-2.svg')

def age(born, today):
    years = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        years -= 1
    anchor_year = born.year + years
    base = date(anchor_year, born.month, min(born.day, calendar.monthrange(anchor_year, born.month)[1]))
    anchor = base
    months = 0
    while True:
        n = months + 1
        year = base.year + (base.month - 1 + n) // 12
        month = (base.month - 1 + n) % 12 + 1
        next_date = date(year, month, min(born.day, calendar.monthrange(year, month)[1]))
        if next_date > today:
            break
        months = n
        anchor = next_date
    return f'{years} years, {months} months, {(today - anchor).days} days'

svg = SVG_PATH.read_text(encoding='utf-8')
new_svg, count = re.subn(
    r'(<text\b(?=[^>]*\bid="age_data")[^>]*>)[^<]*(</text>)',
    lambda m: m.group(1) + age(DOB, date.today()) + m.group(2),
    svg,
    count=1,
)
if count != 1:
    raise RuntimeError('Could not locate uptime element with id="age_data"')
if new_svg != svg:
    SVG_PATH.write_text(new_svg, encoding='utf-8')
print('Uptime:', age(DOB, date.today()))
