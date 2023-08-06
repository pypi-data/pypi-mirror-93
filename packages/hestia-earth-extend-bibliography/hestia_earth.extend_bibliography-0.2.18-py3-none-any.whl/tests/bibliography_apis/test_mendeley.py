import unittest
from unittest.mock import patch
import json

from tests.utils import fixtures_path
from hestia_earth.extend_bibliography.bibliography_apis.mendeley import extend_mendeley


def get_citations():
    titles = []
    with open(f"{fixtures_path}/titles.txt", 'r') as f:
        for line in f:
            titles.append(line.rstrip())
    return titles


class FakeGetRequest():
    def __init__(self):
        with open(f"{fixtures_path}/mendeley/response.json", 'r') as f:
            self.content = json.load(f)

    def json(self):
        return self.content


def get_exception(): raise Exception('error')


class TestMendeley(unittest.TestCase):
    @patch('requests.get', return_value=FakeGetRequest())
    def test_extend_mendeley(self, _m):
        with open(f"{fixtures_path}/mendeley/results.json", 'r') as f:
            expected = json.load(f)
        (actors, bibliographies) = extend_mendeley(get_citations())
        result = actors + bibliographies
        self.assertEqual(result, expected)

    @patch('requests.get', side_effect=get_exception)
    def test_extend_mendeley_exception(self, _m):
        self.assertEqual(extend_mendeley(['title']), ([], []))


if __name__ == '__main__':
    unittest.main()
