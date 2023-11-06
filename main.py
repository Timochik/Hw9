from datetime import date, datetime, timedelta

def birth_date_congr(bd):
    if bd.isoweekday() == 6:   
        # if the passed birthday is on Saturday - increase it by 2 days to the next Monday
        return bd + timedelta(days=2)
    elif bd.isoweekday() == 7: 
        # if the passed birthday is on Sunday - increase it by 1 day to the next Monday
        return bd + timedelta(days=1)
    else:
        # otherwise return the passed date as is
        return bd 

def birth_dates_around(bd):
    """ Returns 3 dates to congratulate the passed birthday - (last year, this year and next year) """
    today = date.today()
    # the construction 'datetime(...).date()' is very important to use for MagicMock - @patch("main.date") decorator
    return [
        birth_date_congr ( datetime ( today.year - 1, bd.month, bd.day ).date() ),
        birth_date_congr ( datetime ( today.year,     bd.month, bd.day ).date() ),
        birth_date_congr ( datetime ( today.year + 1, bd.month, bd.day ).date() ),
    ]

def date_in_range(dt, dt_from, dt_to): 
    """ Returns the passed date 'dt' if it's in range [ 'dt_from', 'dt_to' ) or 'None' otherwise """
    return dt if dt >= dt_from and dt < dt_to else None

def birth_date_in_range(bd, dt_from, dt_to):
    """ Returns a date to congratulate the birthday within the passed range:
        - 'bd' is a date when the person was born;
        - 'dt_from' is an inclusive start of the range, when the birthday is going to be celebrated; 
        - 'dt_to' is an exclusive end of the range, when the birthday is going to be celebrated.
    """
    for bd_around in birth_dates_around(bd):
        bd_in_range = date_in_range(bd_around, dt_from, dt_to)
        if bd_in_range is not None: 
            return bd_in_range
    return None

def get_birth_dates_per_week(users):
    """ Returns a dictionary where:
        - 'key' is a date when to congratulate the birthday during a week from now; 
        - 'value' is a list of users' names. 
    """
    today = date.today()
    a_week_from_today = today + timedelta(days=7)
    birth_dates_per_week = {}
    for user in users:
        bd_congr = birth_date_in_range( user["birthday"], today, a_week_from_today)
        if bd_congr is None: continue
        if bd_congr not in birth_dates_per_week: birth_dates_per_week[bd_congr] = []
        birth_dates_per_week[bd_congr].append(user["name"])
    return birth_dates_per_week

def get_birthdays_per_week(users):
    """ Returns a dictionary where:
        - 'key' is a name of week-day ('Monday', 'Tuesday', ...) when to congratulate the birthday; 
        - 'value' is a list of users' names. 
    """
    return { bd.strftime("%A") : user_names for (bd, user_names) in get_birth_dates_per_week(users).items() }

if __name__ == "__main__":
    use = [
        {"name": "Jan Koum", "birthday": date(1976, 1, 1)},
        {"name": "Bill", "birthday": date(2023, 11, 6)},
        {"name": "Jan", "birthday": date(2023, 11, 9)},
        {"name": "Kim", "birthday": date(2023, 11, 10)},
        {"name": "A", "birthday": date(2023, 11, 5)}, # <-- last Sunday (if today is 06 Nov 2023)
        {"name": "B", "birthday": date(2023, 11, 4)}, # <-- last Saturday (if today is 06 Nov 2023)
        {"name": "C", "birthday": date(2023, 11, 3)}, # <-- last Friday (if today is 06 Nov 2023)
        {"name": "D", "birthday": date(2023, 11, 10)}, # <-- this Friday (if today is 06 Nov 2023)
        {"name": "E", "birthday": date(2023, 11, 11)}, # <-- this Saturday (if today is 06 Nov 2023)
        {"name": "F", "birthday": date(2023, 11, 11)}, # <-- this Sunday (if today is 06 Nov 2023)
    ]

    result = get_birthdays_per_week(use)

    # Виводимо результат
    print(result)
    

