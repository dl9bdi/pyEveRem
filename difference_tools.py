def day_difference(date1, date2):
    """
    Calculates the shortes distance between two dates in days. Important at year roll-over.
    It checks difference for days in the same year as well as to one year ahead and one year back.
    :param date1: first date
    :param date2: second date
    :return: difference in days
    """
    short_difference = 600
    tmp_date = date2.replace(date1.year)
    if abs((tmp_date - date1).days) < abs(short_difference):
        short_difference = (tmp_date - date1).days

    tmp_date = date2.replace(date1.year - 1)
    if abs((tmp_date - date1).days) < abs(short_difference):
        short_difference = (tmp_date - date1).days

    tmp_date = date2.replace(date1.year + 1)
    if abs((tmp_date - date1).days) < abs(short_difference):
        short_difference = (tmp_date - date1).days
    return short_difference
