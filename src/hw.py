from enum import Enum
import json
from typing import List
from src.coins.coin import Coin
from src.pin import Pin

from src.require_unlocked import require_unlocked
from src.wallet import Wallet 

class HW:

    def __init__(self) -> None:
        self.pin = Pin()
        self.wallets = json.load(open("./data/wallets.json", "r"))

    def access(self) -> None:
        if not self.pin.exists():
            self.pin.create()
        self.pin.check()


    def create_new_wallet(self, coin: Coin) -> None:
        # TODO
        pass

    def load_wallet(self, name: str) -> None:
        # TODO
        pass

    def list_wallets(self) -> List[Wallet]:
        # TODO
        return []
        
