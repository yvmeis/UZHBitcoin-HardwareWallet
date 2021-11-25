import unittest
from unittest import mock

from src.pin import Pin


class TestPin(unittest.TestCase):

    def setUp(self):
        with open("src/data/pin.json", "w") as pin_file:
            pin_file.write('{"pin": ""}')
        self.pin = Pin()

    def tearDown(self) -> None:
        self.setUp()

    
    def test_creation(self):
        with mock.patch('builtins.input', return_value="12345678"):
            self.pin.create()

    def test_pin_exists_true(self):
        with mock.patch('builtins.input', return_value="12345678"):
            self.pin.create()
        self.assertTrue(self.pin.exists())

    def test_pin_exists_false(self):
        self.assertFalse(self.pin.exists())

    def test_check_pin_success(self):
        with mock.patch('builtins.input', return_value="12345678"):
            self.pin.create()
            self.assertTrue(self.pin.check())

    def test_check_pin_failure(self):
        with mock.patch('builtins.input', return_value="12345678"):
            self.pin.create()
        with mock.patch('builtins.input', return_value="12345679"):
            self.assertFalse(self.pin.check())
