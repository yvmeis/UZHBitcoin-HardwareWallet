import json
from json.encoder import JSONEncoder
from typing import Dict, List
from src.coins.bitcoin import Bitcoin
from src.coins.coin import Coin
from src.apps.bitcoin.key_derivation import create_extended_private_key, derive_child, prv_to_pub, gen_address
import src.apps.bitcoin.phrasegenerator as pg
import os
import io
import qrcode


class Wallet:
    """ Creates a wallet for coin of type coin. """

    def __init__(self, name: str, coin: str, public_key=None, private_key=None):
        self.__coins_supported = {"bitcoin": Bitcoin()}
        self.__name = name
        self.__public_key = public_key
        self.__address: bytes = gen_address(self.__public_key)
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
        self.__public_key: str = prv_to_pub(derive_child(priv_key, 0))
        self.__address: bytes = gen_address(self.__public_key)
        # store
        content = None
        with open("./src/data/wallets.json", "r") as wallets_file:
            content = json.loads(wallets_file.read())
            wallets = content["wallets"]
            wallets.append({
                "name": self.__name,
                "coin": self.__coin,
                "public_key": self.__public_key,
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
        qr = qrcode.QRCode()
        qr.add_data(self.__address.decode())
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        return f"Name: {self.__name}\nCoin: {self.__coin}\nPublic Key: {self.__address.decode()}\n{f.read()}"

    def __str__(self) -> str:
        return self.__repr__()
