from coins.coin import Coin

class Wallet:
    """ Creates a wallet for coin of type coin. """
    def __init__(self, coin: Coin):
        self.coin: Coin = coin
        # generate private and public key

    """ Generate private and public key. """
    def __generate_keys(self):
        pass


    def process_transaction(self, tx):
        self.coin.handle_transaction(tx)
