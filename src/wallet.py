import json
from json.encoder import JSONEncoder
from typing import Dict, List
from src.coins.bitcoin import Bitcoin
from src.coins.coin import Coin
from src.apps.bitcoin.key_derivation import create_extended_private_key
import src.apps.bitcoin.phrasegenerator as pg
import os
import random


class Wallet:
    """ Creates a wallet for coin of type coin. """

    def __init__(self, name: str, coin: str, private_key=None):
        self.__coins_supported = {"bitcoin": Bitcoin()}
        self.__name = name
        if coin not in self.__coins_supported:
            raise ValueError(
                f"Coin '{coin}' is not supported. So far only {self.__coins_supported.keys()}' are supported.")
        self.__coin = coin

    def __create_seed_phrase(self) -> List[str]:
        """ Generates a seed phrase, makes sure the user writes it down and tries to verify if the user wrote it down. """
        def clearConsole(): return os.system(
            'cls' if os.name in ('nt', 'dos') else 'clear')

        words = pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128))
        while True:
            print("\nWrite down all the following words on paper and in the correct order. DO NOT STORE THEM DIGITALLY!")
            print(
                "They will be used to recover your wallet in case you ever loose access to it.")
            print("\n" + ("*" * len(" ".join(words))))
            print(" ".join(words))
            print("*" * len(" ".join(words)) + "\n")
            input("Press enter after you've finished writing all words down.")
            clearConsole()
            # check if user wrote down the words correctly
            indices = list(range(len(words)))

            # TODO uncomment after testing
            # while True:
            #     n = indices.pop(random.randint(0, len(indices)-1))
            #     word = input(
            #         f"Please type the word at place {n+1} and press enter: ")
            #     if word != words[n]:
            #         print("Word is not correct. Try again.")
            #         word = input(
            #             f"Please type the word at place {n} and press enter: ")
            #     if word != words[n]:
            #         print("Two incorrect tries. Showing words again.")
            #         break
            #     if len(indices) == 0:
            #         return words
            return words  # TODO remove later

    def create(self, pin: str) -> None:
        # create seed phrase
        words: List[str] = self.__create_seed_phrase()
        # create private key
        priv_key: bytes = create_extended_private_key(pg.gen_seed(words))
        # store
        content = None
        with open("./src/data/wallets.json", "r") as wallets_file:
            content = json.loads(wallets_file.read())
            wallets = content["wallets"]
            wallets.append({
                "name": self.__name,
                "coin": self.__coin,
                "private_key": priv_key.decode()
            })
            content["wallets"] = wallets
        with open("./src/data/wallets.json", "w") as f:
            f.write(json.dumps(content))

        # encrypt private key with pin

    def process_transaction(self, tx):
        self.__coins_supported[self.__coin].handle_transaction(tx)

    def __eq__(self, other) -> bool:
        return self.__name == other.__name

    def __repr__(self) -> str:
        return f"Name: {self.__name}, Coin: {self.__coin}"

    def __str__(self) -> str:
        return self.__repr__()
