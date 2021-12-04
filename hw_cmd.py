import os
from typing import Dict, Any, List
from getpass import getpass
import random

from src.hw import HW


class HWCmd:
    """ This class is meant for users to interact with the wallet. """

    def run(self) -> None:
        self.hw = HW()

        commands: Dict[str, Any] = {
            "create wallet": self.create_new_wallet,
            "get wallet": self.get_wallet,
            "list wallets": self.list_wallets,
            "lock": self.lock,
            "pay": self.handle_payment
        }

        self.unlock()
        print("Welcome to PSBT - Probably Secure Bitcoin Tank")
        while True:
            action = input("What can I do for you? ")
            if action not in commands.keys():
                print(f"Commands are: {list(commands.keys())}")
            else:
                commands[action]()
                print("")

    def create_new_wallet(self) -> None:
        while True:
            name = input("Give your wallet a name: ")
            print(
                f"Currently these coins are supported: {str(list(self.hw.get_supported_coins()))}")
            coin = input("Type the name of the coin your wallet should hold: ")
            pin = getpass("Please enter your pin: ")

            try:
                wallet = self.hw.create_new_wallet(name, coin, pin)
                break
            except ValueError as e:
                print(e)
        seed_phrase = wallet.get_seed_phrase()
        self.__check_seed_phrase(seed_phrase)

        print("Wallet successfully created!")
        print(wallet)

    def __check_seed_phrase(self, seed_phrase: List[str]) -> List[str]:
        """ Generates a seed phrase, makes sure the user writes it down and tries to verify if the user wrote it down. """
        def clearConsole(): return os.system(
            'cls' if os.name in ('nt', 'dos') else 'clear')

        while True:
            print("\nWrite down all the following words on paper and in the correct order. DO NOT STORE THEM DIGITALLY!")
            print(
                "They will be used to recover your wallet in case you ever loose access to it.")
            print("\n" + ("*" * len(" ".join(seed_phrase))))
            print(" ".join(seed_phrase))
            print("*" * len(" ".join(seed_phrase)) + "\n")
            input("Press enter after you've finished writing all words down.")
            clearConsole()
            # check if user wrote down the seed_phrase correctly
            indices = list(range(len(seed_phrase)))

            while True:
                n = indices.pop(random.randint(0, len(indices)-1))
                word = input(
                    f"Please type the word at place {n+1} and press enter: ")
                if word != seed_phrase[n]:
                    print("Word is not correct. Try again.")
                    word = input(
                        f"Please type the word at place {n} and press enter: ")
                if word != seed_phrase[n]:
                    print("Two incorrect tries. Showing words again.")
                    break
                if len(indices) == 0:
                    return seed_phrase

    def list_wallets(self) -> None:
        for wallet in self.hw.get_wallets().values():
            print(wallet, "\n")

    def get_wallet(self) -> None:
        wallets = self.hw.get_wallets()
        name = input("Type the name of the wallet: ")
        if name in wallets.keys():
            print(wallets[name])

    def unlock(self) -> None:
        if not self.hw.get_pin().exists():
            print(
                "Please create a pin for your hardware wallet. It will be used to unlock it.")
            pin = getpass(
                "Your pin is should consist of numbers only and have between 8 and 32 characters: ")
            self.hw.get_pin().create(pin)
        for i in range(10):
            pin = getpass("Please enter your pin: ")
            if self.hw.unlock(pin):
                print("Wallet unlocked.")
                return
            else:
                print(f"Pin incorrect. {10-i-1} attemps left.")
        print("Ten incorrect attempts. Destroying all sensitiv information...")

    def lock(self) -> None:
        self.hw.lock()
        print("Hardware wallet is locked.")
        self.unlock()

    def handle_payment(self):
        pass


hw_cmd = HWCmd()
hw_cmd.run()
