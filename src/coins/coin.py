from abc import ABC, abstractmethod

class Coin(ABC):

    def handle_transaction(self, tx):
        self.get_transaction_info(tx)
        if self.get_corfirmation_message():
            print("Signing Transaction...")
            self.sign_transaction(tx)
        
    """ Signs the transaction. """
    @abstractmethod
    def sign_transaction(self, tx):
        pass

    """ Displays transaction details. Currently assumes the transaction to be encoded as b64. """
    @abstractmethod
    def get_transaction_info(self, tx):
        pass

    """ Asks user if they want to proceed with the transaction. """
    def get_corfirmation_message(self) -> bool:
        confirmation = input("Type y to confirm and n to interrupt the payment.")
        if confirmation == "y":
            return True
        else:
            print("Cancelling payment.")
            return False
            