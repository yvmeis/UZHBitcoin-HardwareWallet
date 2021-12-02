import unittest

from src.coins.bitcoin import Bitcoin
from src.wallet import Wallet


class TestWallet(unittest.TestCase):

    def setUp(self) -> None:
        self.wallet = Wallet("Test", "bitcoin")

    def test_process_payment(self):
        pass

    def test_representation_str(self):
        expected = "Name: Test, Coin: Bitcoin"
        actual = str(self.wallet)
        self.assertTrue(expected, actual)

    def test_representation_repr(self):
        expected = "Name: Test, Coin: Bitcoin"
        actual = repr(self.wallet)
        self.assertTrue(expected, actual)


if __name__ == '__main__':
    unittest.main()
