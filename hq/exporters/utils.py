import json
import calendar
from datetime import datetime, timedelta


def get_start_and_end_date_of_last_month(iso_format=False):
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    month = last_month.strftime("%m")
    year = last_month.strftime("%Y")
    last_day_of_month = calendar.monthrange(int(year), int(month))[1]

    if iso_format:
        beg = f'{year}-{month}-01T00:00:00-00:00'
        end = f'{year}-{month}-{last_day_of_month}T00:00:00-00:00'
    else:
        beg = f'{year}-{month}-01'
        end = f'{year}-{month}-{last_day_of_month}'
    return beg, end


def dumper(data, filename):
    json_data = json.dumps(data, ensure_ascii=False, indent=1)
    filename.write_text(json_data)
