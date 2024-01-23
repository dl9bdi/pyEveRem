from datetime import datetime as dt
from unittest import TestCase

from difference_tools import day_difference


class Test(TestCase):
    def test_day_difference_2days(self):
        date1 = dt.strptime("10.01.2024", "%d.%m.%Y").date()
        date2 = dt.strptime("08.01.2024", "%d.%m.%Y").date()
        self.assertEqual(-2, day_difference(date1, date2))
        date1 = dt.strptime("10.01.2024", "%d.%m.%Y").date()
        date2 = dt.strptime("12.01.2024", "%d.%m.%Y").date()
        self.assertEqual(2, day_difference(date1, date2))

    def test_day_difference_1days(self):
        date1 = dt.strptime("10.01.2024", "%d.%m.%Y").date()
        date2 = dt.strptime("09.01.2024", "%d.%m.%Y").date()
        self.assertEqual(-1, day_difference(date1, date2))
        date1 = dt.strptime("10.01.2024", "%d.%m.%Y").date()
        date2 = dt.strptime("11.01.2024", "%d.%m.%Y").date()
        self.assertEqual(1, day_difference(date1, date2))
