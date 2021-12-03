from typing import ByteString
import bcrypt
from getpass import getpass
import json


class Pin:

    def __init__(self):
        with open("./src/data/pin.json", "r") as pin_file:
            pin = json.load(pin_file)
            if pin["pin"] != "":
                self.hashed: bytes = bytes(pin["pin"], encoding='utf-8')
            else:
                self.hashed = b""

    def exists(self) -> bool:
        """ Checks if a pin exists. """
        return self.hashed != b""

    def create(self) -> None:
        """ Asks user to create a new pin. """
        print("Please create a pin for your hardware wallet. It will be used to unlock it.")
        pin = getpass(
            "Your pin is should consist of numbers only and have between 8 and 32 characters: ")
        while True:
            formatting_correct = True
            if len(pin) > 32 or len(pin) < 8:
                formatting_correct = False
                pin = input(
                    "The pin has to be between 8 and 32 numbers. Please provide a new pin: ")
            for symbol in pin:
                if symbol not in "0123456789":
                    formatting_correct = False
                    pin = input(
                        "The pin has to be between 8 and 32 numbers. Please provide a new pin: ")
                    break
            if formatting_correct:
                break

        self.hashed = self.__hash(pin)
        with open(r"./src/data/pin.json", "w") as pin_file:
            pin_file.write(json.dumps({"pin": self.hashed.decode()}))
        # check if pin already exists

    def check(self, pin: str) -> bool:
        """ Used to validate user input. """
        pin_encoded = pin.encode()
        if bcrypt.checkpw(pin_encoded, self.hashed):
            self.value = pin
            return True
        return False

    def __hash(self, pin) -> bytes:
        """ returns the hashed password. """
        pin = pin.encode()
        hashed = bcrypt.hashpw(pin, bcrypt.gensalt())
        return hashed
