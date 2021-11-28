from src.exceptions.WalletLockedException import WalletLockedException


def require_unlocked(func):
    def inner(*args, **kwargs):
        if not args[0].is_unlocked():
            raise WalletLockedException()
        func(*args, **kwargs)
    return inner
