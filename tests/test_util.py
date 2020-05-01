import unittest
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup
import xmlrunner

import dokipro1.const as const
import dokipro1.util as util


class TestUtil(unittest.TestCase):

    def test_get_soup_by_url(self):
        url = 'https://www.yahoo.co.jp/'
        res = util.get_soup_by_url(url)
        soup = BeautifulSoup(features="html.parser")
        self.assertEqual(type(res), type(soup))

    @patch('dokipro1.util.get_soup_by_url')
    def test_get_covid19_info(self, mock_func):
        text = '''
            <span class="DataView-DataInfo-summary">72</span>
            <small class="DataView-DataInfo-date">4/26 実績値（前日比: -31 人）</small>
        '''
        soup = BeautifulSoup(text, "html.parser")
        mock_func.return_value = soup
        expected = '本日の東京都のコロナ陽性患者数は72人です。\n4/26 実績値（前日比: -31 人）'
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


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports"))