from enum import Enum
import json
from typing import Any, Dict, Iterable, List
from getpass import getpass
from src.exceptions.PinInvalidException import PinInvalidException

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

    def handle_payment(self) -> None:
        if len(self.__wallets.keys()) < 1:
            print("You first have to create a wallet before you can pay with it.")
            return

        while True:
            wallet_name = input(
                "Type the name of the wallet you want to use for the payment: ")
            if wallet_name not in self.__wallets.keys():
                print(f"Wallet with name {wallet_name} doesn't exist!")
            try:
                # self.__wallets[wallet_name].process_transaction(None)  # TODO
                break
            except:
                print("Please make sure the wallet name is correct.")
                print("These wallets exist:")
                # self.list_wallets()

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

    def recover_wallet(self) -> None:
        """ Recovers a wallet using its seed phrase """
        # TODO
        pass

    @require_unlocked
    def load_wallet(self) -> None:
        # TODO
        pass

    @require_unlocked
    def get_wallets(self) -> Dict[str, Wallet]:
        return self.__wallets

    def get_pin(self) -> Pin:
        return self.__pin

    def get_supported_coins(self) -> Iterable[str]:
        return self.__coins.keys()
