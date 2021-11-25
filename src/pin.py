from typing import ByteString
import bcrypt
import json

class Pin:

    def __init__(self):
        with open("./src/data/pin.json", "r") as pin_file:
            pin = json.load(pin_file)
            self.hashed = pin["pin"]

    def exists(self):
        return self.hashed != "" 

    def create(self):
        pin = input("Please create a pin for your hardware wallet. It will be used to unlock it: ")
        while True:
            formatting_correct = True
            if len(pin) > 32 or len(pin) < 8:
                formatting_correct = False
                pin = input("The pin has to be between 8 and 32 numbers. Please provide a new pin: ")
            for symbol in pin:
                if symbol not in "0123456789":
                    formatting_correct = False
                    pin = input("The pin has to be between 8 and 32 numbers. Please provide a new pin: ")
                    break
            if formatting_correct:
                break

        self.hashed = self.__hash(pin)
        with open(r"./src/data/pin.json", "w") as pin_file:
            pin_file.write(json.dumps({"pin": str(self.hashed)}))
        # check if pin already exists

    def check(self) -> bool:
        for _ in range(3):
            pin = input("Please enter your pin: ")
            pin = pin.encode()
            if bcrypt.checkpw(pin, self.hashed):
                print("Wallet unlocked.")
                return True
            else:
                print("Pin incorrect.")
        print("Three incorrect attempts.")
        return False

    #returns the hashed password
    def __hash(self, pin) -> bytes:
        pin = pin.encode()
        hashed = bcrypt.hashpw(pin, bcrypt.gensalt())
        return hashed