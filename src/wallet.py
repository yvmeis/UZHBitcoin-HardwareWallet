import json
from json.encoder import JSONEncoder
from typing import Dict, List
from src.coins.bitcoin import Bitcoin
from src.coins.coin import Coin
from src.apps.bitcoin.key_derivation import derive_child, prv_to_pub, gen_as_dictionary
import src.apps.bitcoin.phrasegenerator as pg
import os
import io
import qrcode


class Wallet:
    """ Creates a wallet for coin of type coin. """

    def __init__(self, name: str, coin: str, address=None, public_key=None, **kwargs):
        self.__address = address
        self.__coins_supported = {"bitcoin": Bitcoin()}
        self.__name = name
        if coin not in self.__coins_supported:
            raise ValueError(
                f"Coin '{coin}' is not supported. So far only {self.__coins_supported.keys()}' are supported.")
        self.__coin = coin

    def create(self, pin: str) -> None:
        # TODO remove hardcoded values and use generated values instead
        # create seed phrase
        wallet_information = gen_as_dictionary()
        self.__seed_phrase: List[str] = wallet_information["seed_phrase"]
        # create private key
        priv_key: str = wallet_information["private_key"].decode()
        # create address
        print(wallet_information["address"])
        self.__address: str = wallet_information["address"].decode()
        # store
        content = None
        with open("./src/data/wallets.json", "r") as wallets_file:
            content = json.loads(wallets_file.read())
            wallets = content["wallets"]
            wallets.append({
                "name": self.__name,
                "coin": self.__coin,
                "address": self.__address,
                "private_key": priv_key
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
        qr.add_data(self.__address)
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        return f"Name: {self.__name}\nCoin: {self.__coin}\nAddress: {self.__address}\n{f.read()}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_seed_phrase(self) -> List[str]:
        return self.__seed_phrase

    def get_address(self) -> str:
        return self.__address
