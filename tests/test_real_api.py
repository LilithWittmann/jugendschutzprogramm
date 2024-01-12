import unittest

import vcr

from jugendschutzprogramm import (
    JugendschutzAPIClient,
    APIResult,
    JugendschutzAPIClientException,
)


class TestAPIResult(unittest.TestCase):
    def setUp(self):
        self.client = JugendschutzAPIClient()

    @vcr.use_cassette("tests/vcr_cassettes/test_base_path.yaml")
    def test_base_path(self):
        result = self.client.check_url("bild.de", 16)
        self.assertEqual(result.age, 12)
        self.assertEqual(result.scope_url, "*.bild.de/*")
        self.assertEqual(result.show, True)

    @vcr.use_cassette("tests/vcr_cassettes/test_full_url.yaml")
    def test_full_url(self):
        result = self.client.check_url("https://bild.de", 16)
        self.assertEqual(result.age, 12)
        self.assertEqual(result.scope_url, "*.bild.de/*")
        self.assertEqual(result.show, True)

    @vcr.use_cassette("tests/vcr_cassettes/test_invalid_url.yaml")
    def test_invalid_url(self):
        result = self.client.check_url("https://invalidurl", 16)
        self.assertEqual(result.age, 6)
        result = self.client.check_url("https://sexism-invalid-url", 16)
        self.assertEqual(result.age, 6)
        result = self.client.check_url("https://xxx-invalid-url", 16)
        self.assertEqual(result.age, 6)
        result = self.client.check_url("https://sex-xxx-unused-domain.de", 16)
        self.assertEqual(result.age, 6)
