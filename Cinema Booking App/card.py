
# this file contains the card class


class Card:
    """
    This class contains information of a debit card.
    """

    # constructor
    def __init__(self, holder_name, card_type, card_number, card_cvc, card_balance):
        self.card_balance = card_balance
        self.card_cvc = card_cvc
        self.card_number = card_number
        self.card_type = card_type
        self.holder_name = holder_name
