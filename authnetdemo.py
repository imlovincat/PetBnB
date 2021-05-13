#source: https://quakkels.com/posts/credit-card-processing-with-python/

import models
import paymentprocessing

amount = "19.99"

card = models.CreditCard()
card.number = "4007000000027" # visa test number
card.expiration_date = "2050-01" # any date in the future
card.code = "123" # any 3 digit code

response = paymentprocessing.charge_credit_card(card, amount)

print(response.is_success)
print(response.messages)