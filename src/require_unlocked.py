from src.exceptions.WalletLockedException import WalletLockedException
from functools import wraps


def require_unlocked(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not args[0].is_unlocked():
            raise WalletLockedException()
        return func(*args, **kwargs)

    return inner
