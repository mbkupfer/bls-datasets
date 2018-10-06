import unittest
import datetime

import requests

import bls_datasets.util as util
import bls_datasets.oes as oes

# Initial filename check. Already completed, but keeping around for completeness
@unittest.skip('Already tested. This unit takes a long time to complete.')
class TestGetZipUrls(unittest.TestCase):
    def test_correct_urls(self):
        for year in range(2014, datetime.date.today().year + 1):
            urls = oes._get_zip_urls(str(year))
            for k,v in urls.items():
                r = requests.get(v)
                self.assertTrue(r.ok, '\nError with year: {}\nCut: {}'
                    '\nURL: {}'.format(year, k, v))
