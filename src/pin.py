from typing import ByteString
import bcrypt
from getpass import getpass
import json

from src.exceptions.pinIncorrectFormattedException import PinIncorrectFormattedException


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

    def create(self, pin) -> None:
        """ Creates a new pin """
        if len(pin) > 32 or len(pin) < 8:
            raise PinIncorrectFormattedException(
                "Pin length has to be between 32 and 8 characters.")
        for symbol in pin:
            if symbol not in "0123456789":
                raise PinIncorrectFormattedException(
                    "Pin has to consist of numbers only.")

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
