from enum import Enum
import json
from typing import Any, Dict, Iterable, List
from getpass import getpass
from src.exceptions.PinInvalidException import PinInvalidException
from src.exceptions.WalletNotFoundException import WalletNotFoundException

from src.require_unlocked import require_unlocked
from src.coins.coin import Coin
from src.coins.bitcoin import Bitcoin
from src.pin import Pin
from src.wallet import Wallet


class Status(Enum):
    LOCKED = 1,
    UNLOCKED = 2


class HW:

    def __init__(self) -> None:
        self.__pin = Pin()
        self.__status: Status = Status.LOCKED
        self.__coins: Dict[str, Coin] = {"bitcoin": Bitcoin()}
        self.__load_wallets()

    def __load_wallets(self):
        with open("./src/data/wallets.json", "r") as wallets_file:
            wallets: List[Dict[str, str]] = json.load(wallets_file)["wallets"]
            self.__wallets = {data["name"]: Wallet(**data) for data in wallets}

    def unlock(self, pin) -> bool:
        """ returns True on success False on failure """
        if not self.__pin.exists():
            raise PinInvalidException("Please create a pin first.")
        if self.__pin.check(pin):
            self.__status = Status.UNLOCKED
            return True
        return False

    def is_unlocked(self) -> bool:
        return self.__status == Status.UNLOCKED

    def handle_payment(self, name: str, tx: str) -> None:
        self.get_wallet(name).process_transaction(tx)

    @require_unlocked
    def lock(self) -> None:
        self.__pin = Pin()
        self.__status = Status.LOCKED

    @require_unlocked
    def create_new_wallet(self, name: str, coin: str, pin: str) -> Wallet:
        if name in self.__wallets.keys():
            raise ValueError(f"A wallet named '{name}' already exists.")
        if not self.__pin.check(pin):
            raise ValueError(f"Pin incorrect.")

        wallet = Wallet(name, coin)
        wallet.create(pin)
        self.__wallets[name] = wallet
        return wallet

    def get_wallet(self, name: str) -> Wallet:
        """ Raises WalletNotFoundException if there is no wallet with that name."""
        if name in self.__wallets.keys():
            return self.__wallets[name]
        raise WalletNotFoundException("No wallet with this name exists.")

    def recover_wallet(self) -> None:
        """ Recovers a wallet using its seed phrase """
        # TODO
        pass

    @require_unlocked
    def get_wallets(self) -> Dict[str, Wallet]:
        return self.__wallets

    def get_pin(self) -> Pin:
        return self.__pin

    def get_supported_coins(self) -> Iterable[str]:
        return self.__coins.keys()
