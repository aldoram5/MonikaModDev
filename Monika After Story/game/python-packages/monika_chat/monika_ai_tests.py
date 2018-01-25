import unittest
from datetime import date
from utils import parse_any_date, strip_punc, expand_contractions


class TestStringMethods(unittest.TestCase):

    def test_date_parser(self):
        print("DateParser tests")
        self.assertEqual(parse_any_date("9/9/1999"),date(1999, 9, 9))
        self.assertEqual(parse_any_date("My birthday is 9-9-1999"),date(1999, 9, 9))
        self.assertEqual(parse_any_date("30-9-1999"),date(1999, 9, 30))
        self.assertEqual(parse_any_date("An important date is 30-9-1999"),date(1999, 9, 30))
        self.assertEqual(parse_any_date("An important date is 9-30-1999", True),date(1999, 9, 30))
        self.assertEqual(parse_any_date("No date to parse here", True), None)
        print("DateParser tests - Passed")

    def test_strip_punctuation(self):
        print("StripPunctuation tests")
        self.assertEqual(strip_punc("punctuated+-:;?|.", True), "punctuated")
        self.assertEqual(strip_punc("punctuated+-:;?|.", False), "punctuated")
        print("StripPunctuation tests - Passed")


if __name__ == '__main__':
    unittest.main()
