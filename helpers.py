import datetime


def validate_date(date_str: str):
    """
    Проверка даты.
    """
    date_format = "%d.%m.%Y"

    try:
        result = datetime.datetime.strptime(date_str, date_format).date()
    except ValueError:
        result = None

    return result


def validate_int(int_str: str):
    """
    Проверка числа.
    """
    try:
        number = int(int_str)
    except ValueError:
        number = None

    return number


def get_ints(ints_str: str):
    """
    Преобразует строку с числами в массив int.
    """
    ints = []

    for int_str in ints_str.replace(' ', '').split(','):
        int_value = validate_int(int_str)
        if int_value is not None:
            ints.append(int_value)

    return ints
