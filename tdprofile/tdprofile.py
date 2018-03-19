# coding=utf-8
"""
The main file for TDPROFILE
"""
import calendar
from contextlib import contextmanager
import configparser
from datetime import date, datetime, timedelta
import os
import sys

import pyodbc

CONFIG_CONTENT = """
# This is the config file for tdprofile

# The section of database tdp5, please make sure lower case
[tdp5]
dburl = 
td_user_name = 
td_password = 

# The section of database tdp5, please make sure lower case
[tdp3]
dburl = 
td_user_name = 
td_password = 
"""


TD_CONN_FMT = "DRIVER=Teradata;DBCNAME={url};UID={u};PWD={p};QUIETMODE=YES"
BTEQ_CONN_FMT = "{url}/{u}, {p};"


CONFIG_FILE = '.tdprofile'
HOME = os.getenv('HOME', None) or os.getenv('USERPROFILE', None)
if not HOME:
    raise SystemExit("Home folder not found")

CONFIG_FILE_FULL = os.path.join(HOME, CONFIG_FILE)
if not os.path.isfile(CONFIG_FILE_FULL):
    with open(CONFIG_FILE_FULL, 'w') as f:
        f.write(CONFIG_CONTENT)



class TD(object):
    """The teradata object to represent a one Teradata instance
    """
    ALLOWED_DB_NAME = ['tdp1', 'tdp5']
    def __init__(self, name):
        if not isinstance(name, str) or name.lower() not in TD.ALLOWED_DB_NAME:
            raise ValueError("The db name is not valid, please check")
        self._tdname = name.lower()
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE_FULL)

        if self._tdname not in self.config:
            raise ValueError("[{0}] has not been defined in {1}".format(
                self._tdname,
                CONFIG_FILE_FULL
            ))

        self._url = self.config[self._tdname]['dburl']
        self._u = self.config[self._tdname]['td_user_name']
        self._p = self.config[self._tdname]['td_password']
        
    def __repr__(self):
        return "TD({})".format(self._tdname)

    def __str__(self):
        return "TD({})".format(self._tdname)


    def _conn(self):
        """internal connection"""
        self.connection = pyodbc.connect(TD_CONN_FMT.format(
            url = self._url,
            u = self._u,
            p = self._p 
        ))


    @contextmanager
    def conn(self):
        """ use Context to make sure the cursor will be closed
        """
        try:
            self._conn()
            yield self.connection
        finally:
            self.connection.close()


    @property
    def bteq_logon_str(self):
        return  BTEQ_CONN_FMT.format(
            url = self._url,
            u = self._u,
            p = self._p 
        )


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
        """ a <= b
        """
        if not isinstance(other, Month):
            raise TypeError("Not same type Month, cannot compare")
        if self._year < other._year or \
            (self._year == other._year and self._month < other._month) or \
            self.__eq__(other):
            return True
        else:
            return False

    def __lt__(self, other):
        """ a < b
        """
        if not isinstance(other, Month):
            raise TypeError("Not same type Month, cannot compare")
        if self._year < other._year or \
            (self._year == other._year and self._month < other._month):
            return True
        else:
            return False
        pass

    def __ge__(self, other):
        """ a >= b
        """
        if not isinstance(other, Month):
            raise TypeError("Not same type Month, cannot compare")
        if self._year > other._year or \
            (self._year == other._year and self._month > other._month) or \
            self.__eq__(other):
            return True
        else:
            return False

    def __gt__(self, other):
        """ a > b
        """
        if not isinstance(other, Month):
            raise TypeError("Not same type Month, cannot compare")
        if self._year > other._year or \
            (self._year == other._year and self._month > other._month): 
            return True
        else:
            return False

    def __ne__(self, other):
        """ a != b
        """
        if not isinstance(other, Month):
            raise TypeError("Not same type Month, cannot compare")
        
        if self._year != other._year or self._month != other._month:
            return True
        else:
            return False


    def __eq__(self, other):
        """ a == b
        """
        if not isinstance(other, Month):
            raise TypeError("Not same type Month, cannot compare")
        if self._year == other._year and self._month == other._month:
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

    def as_fy(self, start_month=10):
        """Assume self is calendar year, then convert to finanical year
        eg 201610 -> 201710
        start_month is the first month of finical year
        """
        if self._month >= start_month:
            self._year = self._year + 1

    def as_cy(self, start_month=10):
        """Assume self is a finical year, then convert to calendar year
        eg. 201710 -> 201610
        """
        if self._month >= start_month: # 10, 11, 12
            self._year = self._year - 1
        