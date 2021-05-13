#source: https://quakkels.com/posts/credit-card-processing-with-python/


class CreditCard:
    number = None
    expiration_date = None
    code = None

class TransactionResponse:
    is_success = False
    messages = []