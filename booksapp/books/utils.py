def handle_partial_date(partial_date):
    if len(partial_date) == 4:
        date = f'{partial_date}-01-01'
    elif len(partial_date) == 7:
        date = f'{partial_date}-01'
    elif len(partial_date) == 10:
        date = partial_date
    return date