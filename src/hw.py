from enum import Enum
import json
from typing import Any, Dict, List

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

    def run(self):
        commands: Dict[str, Any] = {
            "create wallet": self.create_new_wallet,
            "load wallet": self.load_wallet,
            "list wallets": self.list_wallets,
            "lock": self.lock,
            "pay": self.handle_payment
        }
        self.unlock()
        print("Welcome to PSBT - Probably Secure Bitcoin Tank")
        while True:
            action = input("What can I do for you? ")
            if action not in commands.keys():
                print(f"Commands are: {list(commands.keys())}")
            else:
                commands[action]()

    def __load_wallets(self):
        with open("./src/data/wallets.json", "r") as wallets_file:
            wallets: List[Dict[str, str]] = json.load(wallets_file)["wallets"]
            self.__wallets = {data["name"]: Wallet(**data) for data in wallets}

    def unlock(self) -> None:
        if not self.__pin.exists():
            self.__pin.create()
        if self.__pin.check():
            self.__status = Status.UNLOCKED

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
                self.list_wallets()

    @require_unlocked
    def lock(self) -> None:
        self.__pin = Pin()
        self.__status = Status.LOCKED
        print("Hardware Wallet is locked.")
        self.unlock()

    @require_unlocked
    def create_new_wallet(self) -> None:
        # Choose a name
        name = input("Give your wallet a name: ")
        while name in self.__wallets.keys():
            name = input(
                f"You already have a wallet named '{name}'. Please choose a different name: ")
        # Choose a coin
        while True:
            print(
                f"Currently these coins are supported: {str(list(self.__coins.keys()))}")
            coin: str = input(
                "Type the name of the coin your wallet should hold: ")
            try:
                wallet = Wallet(name, coin)
                self.__wallets[name] = wallet
                print("Wallet successfully created!")
                break
            except ValueError as e:
                print(e)

    @require_unlocked
    def load_wallet(self) -> None:
        # TODO
        pass

    @require_unlocked
    def list_wallets(self):
        for wallet in self.__wallets:
            print(wallet)
