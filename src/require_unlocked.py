from hw import HW
from src.exceptions.WalletLockedException import WalletLockedException

def require_unlocked(func):
    def inner(hw: HW, *args, **kwargs):
        if hw.is_wallet_unlocked():
            raise WalletLockedException()
        else:
            func(*args, **kwargs)