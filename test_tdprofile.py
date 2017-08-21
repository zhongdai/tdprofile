# coding=utf-8


"""Tests for Wbteq"""
import os
import unittest

from tdprofile import tdprofile as tdp


class TDPROFILETestCase(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        pass

    def tearDown(self):
        pass

    def test_invalid_username(self):
        with self.assertRaises(TypeError):
                p = tdp.Profile(1,'a','a')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TDPROFILETestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
