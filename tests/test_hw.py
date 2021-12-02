import unittest
from unittest import mock
from src.coins.bitcoin import Bitcoin
from src.exceptions.WalletLockedException import WalletLockedException

from src.hw import HW


class TestHW(unittest.TestCase):

    def setUp(self) -> None:
        self.hw = HW()

    def test_unlock(self):
        with mock.patch('builtins.input', return_value="12345678"):
            self.hw.unlock()
        self.assertTrue(self.hw.is_unlocked())

    def test_create_wallet_when_locked(self):
        with self.assertRaises(WalletLockedException):
            self.hw.create_new_wallet()

    def test_create_new_wallet(self):
        pass

    def test_load_wallet(self):
        pass

    def test_list_wallets(self):
        pass


if __name__ == '__main__':
    unittest.main()
