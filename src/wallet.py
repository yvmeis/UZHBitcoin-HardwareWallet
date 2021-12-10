import json
from json.encoder import JSONEncoder
from typing import Any, Dict, List

from btclib.psbt import Psbt
from src.coins.bitcoin import Bitcoin
from src.coins.coin import Coin
from src.apps.bitcoin.key_derivation import derive_child, prv_to_pub, gen_wallet, gen_child
import src.apps.bitcoin.phrasegenerator as pg
import os
import io
import qrcode


class Wallet:
    """ Creates a wallet for coin of type coin. """

    def __init__(self, name: str, coin: str, address=None, public_key=None, private_key=None, root_key=None, **kwargs):
        self.__address = address
        self.__coins_supported = {"bitcoin": Bitcoin()}
        self.__name = name
        self.__priv_key = private_key
        if coin not in self.__coins_supported:
            raise ValueError(
                f"Coin '{coin}' is not supported. So far only {list(self.__coins_supported.keys())}' are supported.")
        self.__coin = coin

    def create(self, pin: str, root_key=None) -> None:
        """ Creates and stores wallet information """

        # get wallet information
        wallet_information = gen_wallet()
        self.__seed_phrase: List[str] = wallet_information["seed_phrase"]
        if root_key:
            self.__root_key = root_key
        else:
            self.__root_key: str = wallet_information["root_key"].decode()
        # TODO always create a random key pair
        children: Dict[str, Any] = gen_child(self.__root_key, 0)
        self.__priv_key: str = children["private_key"]
        self.__address: str = children["address"].decode()

        # store
        content = None
        with open("./src/data/wallets.json", "r") as wallets_file:
            content = json.loads(wallets_file.read())
            wallets = content["wallets"]
            wallets.append({
                "name": self.__name,
                "coin": self.__coin,
                "address": self.__address,
                "private_key": self.__priv_key,
                "root_key": self.__root_key
            })
            content["wallets"] = wallets
        with open("./src/data/wallets.json", "w") as f:
            f.write(json.dumps(content))

    def process_transaction(self, tx: str):
        return self.__coins_supported[self.__coin].sign_transaction(
            tx, self.__priv_key)

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

    def get_coin(self) -> Coin:
        return self.__coins_supported[self.__coin]

    def get_coin_str(self) -> str:
        return self.__coin
