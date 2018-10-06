import unittest
import datetime

import bls_datasets.oes as oes

class TestGetData(unittest.TestCase):

    def test_out_of_range_past_year(self):
        self.assertRaises(ValueError, oes.get_data, year=2013)

    def test_out_of_range_future_year(self):
        CUR_YEAR = datetime.date.today().year
        self.assertRaises(ValueError, oes.get_data, year=CUR_YEAR+1)

    def test_bad_industry_scope(self):
        self.assertRaises(ValueError, oes.get_data, industry_scope=7)
