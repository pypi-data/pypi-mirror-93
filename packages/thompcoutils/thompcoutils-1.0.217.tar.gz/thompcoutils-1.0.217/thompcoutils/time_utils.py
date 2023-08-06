import datetime
import calendar
from dateutil.relativedelta import relativedelta, TH


class Holiday(datetime.datetime):
    THANKSGIVING = "thanksgiving"
    CHRISTMAS = "christmas"
    NEW_YEARS = "newyears"
    INDEPENDENCE = "independence"

    def __new__(cls, holiday_in):
        year = datetime.datetime.now().year
        holiday = holiday_in.lower()

        if holiday == Holiday.THANKSGIVING:
            month = 11
            november = datetime.datetime(year=year, month=month, day=1)
            day = (november + relativedelta(day=31, weekday=TH(-1))).day
        elif holiday == Holiday.CHRISTMAS:
            month = 12
            day = 25
        elif holiday == Holiday.NEW_YEARS or holiday == "new years":
            month = 1
            day = 1
        elif holiday == Holiday.INDEPENDENCE:
            month = 7
            day = 4
        else:
            raise RuntimeError("{} is not a recognised Holiday".format(holiday))
        return super().__new__(cls, year=year, month=month, day=day)


def is_weekend(dt):
    return dt.weekday() >= 5
