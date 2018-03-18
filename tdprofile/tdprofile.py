# coding=utf-8
"""
The main file for TDPROFILE
"""
from datetime import date, datetime, timedelta
import calendar


def conn(dbname=None):
    pass

class Month(object):
    """Represent a Month, provides handy method to convert or move
    """
    def __init__(self, year=None, month=None):
        if year is None and month is None:
            # Current month
            today = date.today()
            self._year = today.year
            self._month = today.month
        else:
            if not isinstance(year, int) or not isinstance(month, int):
                raise ValueError("year and month must be a int type")
            if year < 888 or year > 9999 or month < 1 or month > 12:
                raise ValueError("year (999 - 9999), month (1 - 12)")
            self._year = year
            self._month = month

    @classmethod
    def from_month_key(cls, month_key):
        year = int(month_key[:4])
        month = int(month_key[4:])
        return cls(year, month)

        
    def _get_last_day(self):
        """return the numeric of last day, such as 28, 31
        """
        return calendar.monthrange(self._year, self._month)[1]


    def __repr__(self):
        return "Month({},{})".format(self._year, self._month)
    
    def __str__(self):
        if self._month < 10:
            m_str = '0' + str(self._month)
        else:
            m_str = str(self._month)
        return str(self._year) + m_str
    

    def __le__(self, other):
        pass

    def __eq__(self, other):
        if isinstance(other, Month) and \
            self._year == other._year and  \
            self._month == other._month:
            return True
        else:
            return False
        
    def __sub__(self, n):
        """Assume n > 0"""
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Please give a int and greater than 0")
        if n >= 12:
            year_offset = n // 12
            month_offset = n % 12
        else:
            year_offset = 0
            month_offset = n
            
        if self._month > month_offset:
            new_month = self._month - month_offset
            new_year = self._year - year_offset
        elif self._month == month_offset:
            # last month of pervious year
            new_month = 12
            new_year = self._year - year_offset - 1
        else:
            new_month = self._month + 12 - month_offset
            new_year = self._year - year_offset -1
            
        return Month(new_year, new_month)

    def __add__(self, num_of_month):
        if not isinstance(num_of_month, int) or num_of_month <= 0:
            raise ValueError("Please give a int and greater than 0")
        month = num_of_month + self._month - 1
        year = self._year + month // 12
        month = month % 12 + 1
        return Month(year, month)


    @property
    def first_day(self):
        """return a Date instance of the first day
        """
        return date(self._year, self._month, 1)

    @property
    def last_day(self):
        """return the last day
        """
        return date(self._year, self._month, self._get_last_day()) 

    def offset(self, n=0):
        """move around the month
        """
        pass