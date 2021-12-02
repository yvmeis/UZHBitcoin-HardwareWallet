from typing import Dict
from src.coins.bitcoin import Bitcoin
from src.coins.coin import Coin


class Wallet:
    """ Creates a wallet for coin of type coin. """

    def __init__(self, name: str, coin: str):
        self.__coins_supported = {"bitcoin": Bitcoin()}
        self.__name = name
        if coin not in self.__coins_supported:
            raise ValueError(
                f"Coin '{coin}' is not supported. So far only {self.__coins_supported.keys()}' are supported.")
        self.__coin = self.__coins_supported[coin]

    def __generate(self) -> None:
        """ Generate the wallet with private key and seed phrase. """
        # generate private key
        # generate public key
        pass

    def create(self, name: str, coin: Coin) -> None:
        # check that wallet with same name doesn't exist already

        self.__generate()

    def process_transaction(self, tx):
        self.__coin.handle_transaction(tx)

    def __eq__(self, other) -> bool:
        return self.__name == other.__name

    def __repr__(self) -> str:
        return f"Name: {self.__name}, Coin: {self.__coin}"

    def __str__(self) -> str:
        return self.__repr__()
