from enum import Enum

from src.require_unlocked import require_unlocked 

class HW:

    def __init__(self):
        self.wallets = {} # TODO load from memory
        self.__status = Status.LOCKED

    def unlock(self, pin):
        # TODO
        self.__status = Status.UNLOCKED

    @require_unlocked
    def create_new_wallet(self, coin):
        # TODO
        pass

    @require_unlocked
    def load_wallet(self, name):
        # TODO
        pass

    @require_unlocked
    def list_wallets(self):
        # TODO
        pass

    def is_wallet_unlocked(self):
        return self.__status == Status.LOCKED
        
class Status(Enum):
    LOCKED = 1
    UNLOCKED = 2