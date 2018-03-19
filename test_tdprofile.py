# coding=utf-8


"""Tests for Wbteq"""
import os
import unittest

from tdprofile import Month
from datetime import date


class TDPROFILETestCase(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        pass

    def tearDown(self):
        pass

    def test_curr_month(self):
        m = Month()
        today = date.today()

        self.assertEquals(m._year,today.year)
        self.assertEquals(m._month,today.month)

    def test_month_key_less_than_10(self):
        m = Month(2018,9)
        self.assertEqual('201809', str(m))

    def test_month_key_more_than_10(self):
        m = Month(2018,11)
        self.assertEqual('201811', str(m))

    def test_first_day(self):
        m = Month(2018,1)
        dt = date(2018,1,1)
        self.assertEqual(m.first_day, dt)

    def test_last_day(self):
        m = Month(2018,1)
        dt = date(2018,1,31)
        self.assertEqual(m.last_day, dt)

    def test_equal(self):
        m = Month(2018,1)
        n = Month(2018,1)
        self.assertTrue(m == n)

    def test_add_same_year(self):
        m = Month(2018,1)
        n = Month(2018,2)

        self.assertEqual(n, m + 1)

    def test_sub_same_year(self):
        m = Month(2018,1)
        n = Month(2018,2)
        result = n - 1

        self.assertEqual(m, result)
        
    def test_add_next_year(self):
        m = Month(2018,10)
        n = Month(2019,1)

        self.assertEqual(n, m + 3)

    def test_sub_last_year(self):
        m = Month(2018,10)
        n = Month(2019,1)

        self.assertEqual(m, n - 3)

    def test_sub_zero_month(self):
        m = Month(2017,12)
        n = Month(2018,7)

        self.assertEqual(m, n - 7)

    def test_from_month_key(self):
        m = Month(2018, 10)
        n = Month.from_month_key('201810')

        self.assertEqual(m, n)

    def test_compare(self):
        m = Month(2017,12)
        n = Month(2018,7)

        self.assertTrue(n != m)
        self.assertTrue(m < n)
        self.assertTrue(m <= n)
        self.assertTrue(n > m)
        self.assertTrue(n >= m)

    def test_compare_equal(self):
        m = Month(2018,1)
        n = Month(2018,1)

        self.assertTrue(m <= n)
        self.assertTrue(m >= n)

    def test_as_cy(self):
        m = Month(2018,10)
        m2 = Month(2017,3)
        target = Month(2017,10)

        m.as_cy()
        m2.as_cy()
        self.assertEqual(target, m)
        self.assertEqual(m2, Month(2017,3))


    def test_as_fy(self):
        m = Month(2017,10)
        m2 = Month(2017,3)
        target = Month(2018,10)

        m.as_fy()
        m2.as_fy()
        self.assertEqual(target, m)

        self.assertEqual(m2, Month(2017,3))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TDPROFILETestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
