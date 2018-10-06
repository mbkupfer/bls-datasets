import unittest
import datetime

import bls_datasets.qcew as qcew

class TestURLGenerators(unittest.TestCase):

    def test_get_area_url(self):
        self.assertEqual(qcew._get_area_url(year='2017', qtr='a',
            area='US000'),
            'http://data.bls.gov/cew/data/api/2017/a/area/US000.csv')

    def test_get_industry_url(self):
        self.assertEqual(qcew._get_industry_url(year='2017', qtr='1',
            industry='10'),
            'http://data.bls.gov/cew/data/api/2017/1/industry/10.csv')

    def test_get_size_url(self):
        self.assertEqual(qcew._get_size_url(year='2017', size='3'),
            'http://data.bls.gov/cew/data/api/2017/1/size/3.csv')

class TestGetData(unittest.TestCase):

    def test_raises_value_error(self):
        self.assertRaises(ValueError, qcew.get_data, 'cut', year=2017)
        self.assertRaises(ValueError, qcew.get_data, 'cut', size=1)
        self.assertRaises(ValueError, qcew.get_data, 'cut', qtr=2017)
        self.assertRaises(ValueError, qcew.get_data, 'cut', industry=52)

    def test_get_slice_by_area(self):
        df = qcew.get_data('area', rtype='dataframe', year='2017',
            qtr='1', area='26000')
        self.assertEqual(df[:1]['avg_wkly_wage'].values[0], 1043)

    def test_get_slice_by_industry(self):
        df = qcew.get_data('industry', rtype='dataframe', year='2017',
            qtr='1', industry='10')
        self.assertEqual(df[:1]['avg_wkly_wage'].values[0], 893)

    def test_get_slice_by_size(self):
        df = qcew.get_data('size', rtype='dataframe', year='2017',
            size='3')
        self.assertEqual(df[:1]['qtrly_estabs'].values[0], 14999)
