import unittest
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup
import xmlrunner
from http.client import HTTPResponse

import dokipro1.const as const
import dokipro1.util as util


class TestUtil(unittest.TestCase):

    def test_get_soup_by_url(self):
        url = 'https://www.yahoo.co.jp/'
        res = util.get_soup_by_url(url)
        soup = BeautifulSoup(features="html.parser")
        self.assertEqual(type(res), type(soup))

    @patch('dokipro1.util.get_covid19_data')
    def test_get_covid19_info_plus(self, mock_func):
        res = {
            "date":  "2020/7/23 20:30",
            "data": [
                {
                    "diagnosed_date": "2020-04-25",
                    "count": 119,
                    "missing_count": 68,
                    "reported_count": 51,
                    "weekly_gain_ratio": 0.8,
                    "untracked_percent": 60.6,
                    "weekly_average_count": 125.6,
                    "weekly_average_untracked_count": 76.1,
                    "weekly_average_untracked_increse_percent": 74.1
                },
                {
                    "diagnosed_date": "2020-04-26",
                    "count": 82,
                    "missing_count": 56,
                    "reported_count": 26,
                    "weekly_gain_ratio": 0.82,
                    "untracked_percent": 61.3,
                    "weekly_average_count": 121.7,
                    "weekly_average_untracked_count": 74.6,
                    "weekly_average_untracked_increse_percent": 73
                }
            ]
        }

        mock_func.return_value = res
        expected = '本日の東京都のコロナ陽性患者数は82人です。\n（前日比: -37 人）'
        self.assertEqual(util.get_covid19_info(const.TODAY), expected)

    @patch('dokipro1.util.get_covid19_data')
    def test_get_covid19_info_minus(self, mock_func):
        res = {
            "date":  "2020/7/23 20:30",
            "data": [
                {
                    "diagnosed_date": "2020-07-22",
                    "count": 238,
                    "missing_count": 138,
                    "reported_count": 100,
                    "weekly_gain_ratio": 1.3,
                    "untracked_percent": 53.4,
                    "weekly_average_count": 242.9,
                    "weekly_average_untracked_count": 129.6,
                    "weekly_average_untracked_increse_percent": 148.2
                },
                {
                    "diagnosed_date": "2020-07-23",
                    "count": 366,
                    "missing_count": 225,
                    "reported_count": 141,
                    "weekly_gain_ratio": 1.3,
                    "untracked_percent": 55.9,
                    "weekly_average_count": 254.3,
                    "weekly_average_untracked_count": 142.1,
                    "weekly_average_untracked_increse_percent": 154
                }
            ]
        }

        mock_func.return_value = res
        expected = '本日の東京都のコロナ陽性患者数は366人です。\n（前日比: +128 人）'
        self.assertEqual(util.get_covid19_info(const.TODAY), expected)

    @patch('dokipro1.util.get_soup_by_url')
    def test_get_tech_news(self, mock_func):
        text='''
        <h3 class="entrylist-contents-title">
            <a href="https://example.com">sample</a>
        </h3>
        '''
        soup = BeautifulSoup(text, "html.parser")
        mock_func.return_value = soup
        expected = '本日のテクノロジーニュースです\n\nsample\nhttps://example.com'
        self.assertEqual(util.get_tech_news(1), expected)

    def test_get_tech_news_one(self):
        text='''
        <h3 class="entrylist-contents-title">
            <a href="https://example.com">sample</a>
        </h3>
        '''
        soup = BeautifulSoup(text, "html.parser")
        expected = 'sample\nhttps://example.com'
        self.assertEqual(util.get_tech_news_one(soup, 0), expected)

    def test_guess_horse_racing(self):
        expected = '10 18 11'
        self.assertEqual(util.guess_horse_racing(202105300511, 18), expected)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports"))