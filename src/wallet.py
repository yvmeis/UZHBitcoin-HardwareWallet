from src.coins.coin import Coin


class Wallet:
    """ Creates a wallet for coin of type coin. """

    def __init__(self, name: str, coin: Coin):
        self.name: str = name
        self.coin: Coin = coin

    """ Generate private and public key. """

    def __generate_keys(self):
        # generate private and public key
        pass

    def process_transaction(self, tx):
        self.coin.handle_transaction(tx)
