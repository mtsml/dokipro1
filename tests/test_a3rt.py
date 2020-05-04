import unittest
from unittest.mock import Mock, patch

import xmlrunner

import dokipro1.const as const
import dokipro1.a3rt as a3rt


# 外部のAPIを呼び出してしまっているためMock化が必要
class TestA3rt(unittest.TestCase):

    def test_get_reply_messgage_ok(self):
        expected='調子はいいです'
        self.assertEqual(a3rt.get_reply_message("調子はどう？"), expected)

    def test_get_reply_messgage_ng(self):
        expected='ちょっと何言ってるか分からないです'
        self.assertEqual(a3rt.get_reply_message(""), expected)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports"))