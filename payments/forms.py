from django import forms
# from .models import Ticket


# Defining the user class with a balance attribute
class balance(forms.Form):
  balance = forms.DecimalField(max_digits=8, decimal_places=2)
  total = forms.DecimalField(
        max_digits=8, decimal_places=2,
        widget=forms.NumberInput()
    )
  def clean(self):
        cleaned_data = super().clean()
        balance = cleaned_data.get('balance')
        user = self.request.user
        if user.balance < balance:
            raise forms.ValidationError("You don't have enough balance to purchase this ticket.")
        return cleaned_data
  def __init__(self, balance=0.0):
    self.balance = balance
    
  def add_funds(self, amount):
    self.balance += amount
    
  def check_balance(self):
    return self.balance
  
  def make_purchase(self, amount):
    if self.balance >= amount:
      self.balance -= amount
      return True
    else:
      return False


class PaymentMethod:
    def __init__(self, name, account_number, routing_number):
        self.name = name
        self.account_number = account_number
        self.routing_number = routing_number
    
    def process_payment(self, amount):
        # print(f"Processing payment of {amount} using {self.}")
        print(f"Processing payment of {amount} BD")

class CreditCard(PaymentMethod):
    def __init__(self, name, card_number, expiration_date, cvv):
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv
        super().__init__(name, card_number, None)
    
    def process_payment(self, amount):
        # Validate card details before processing payment
        if self.is_valid():
            super().process_payment(amount)
        else:
            print("Invalid card details. Payment failed.")
    
    def is_valid(self):
        return True

class BankAccount(PaymentMethod):
    def __init__(self, name, account_number, routing_number):
        super().__init__(name, account_number, routing_number)

credit_card = CreditCard("XX", "1234 5678 1234 5678", "01/2023", "123")
credit_card.process_payment(50)

bank_account = BankAccount("XX", "1234-5678", "123456789")
bank_account.process_payment(100)
