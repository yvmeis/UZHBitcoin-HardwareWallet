from abc import ABC, abstractmethod


class Coin(ABC):

    def handle_transaction(self, tx):
        self.get_transaction_info(tx)
        if self.get_corfirmation_message():
            print("Signing Transaction...")
            self.sign_transaction(tx)

    @abstractmethod
    def sign_transaction(self, tx):
        """ Signs the transaction. """
        pass

    @abstractmethod
    def get_transaction_info(self, tx):
        """ Provides transaction data like receiving address and amount sent. Currently assumes the transaction to be encoded as b64. """
        pass

    def get_corfirmation_message(self) -> bool:
        """ Asks user if they want to proceed with the transaction. """
        confirmation = input(
            "Type y to confirm and n to interrupt the payment.")
        if confirmation == "y":
            return True
        else:
            print("Cancelling payment.")
            return False
