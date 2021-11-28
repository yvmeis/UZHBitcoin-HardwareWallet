from enum import Enum
import json
from typing import List

from src.require_unlocked import require_unlocked
from src.coins.coin import Coin
from src.pin import Pin
from src.wallet import Wallet


class Status(Enum):
    LOCKED = 1,
    UNLOCKED = 2


class HW:

    def __init__(self) -> None:
        self.__pin = Pin()
        self.__wallets: dict = json.load(open("./src/data/wallets.json", "r"))
        self.__status: Status = Status.LOCKED

    def unlock(self) -> None:
        if not self.__pin.exists():
            self.__pin.create()
        if self.__pin.check():
            self.__status = Status.UNLOCKED

    def is_unlocked(self) -> bool:
        return self.__status == Status.UNLOCKED

    @require_unlocked
    def lock(self) -> None:
        self.__pin = Pin()
        self.__status = Status.LOCKED
        print("Hardware Wallet is locked.")

    @require_unlocked
    def create_new_wallet(self, coin: Coin) -> None:
        # TODO
        pass

    @require_unlocked
    def load_wallet(self, name: str) -> None:
        # TODO
        pass

    @require_unlocked
    def list_wallets(self) -> List[Wallet]:
        # TODO
        return []
