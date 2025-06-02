class Transaction:
    def __init__(self, amount, txn_type, narration):
        self.date_time = datetime.now()
        self.amount = amount
        self.txn_type = txn_type
        self.narration = narration
    def __repr__(self):
        return f"{self.date_time} | {self.txn_type.upper()} | {self.narration} | {self.amount}"
class Account:
    interest_rate = 0.05
    _account_counter = 30000
    minimum_balance = 200
    def __init__(self, owner):
        self.owner = owner
        self._account_number = Account._account_counter
        Account._account_counter += 1
        self._loan = 0
        self._is_frozen = False
        self._closed = False
        self._transactions = []
    def _add_transaction(self, amount, txn_type, narration):
        self._transactions.append(Transaction(amount, txn_type, narration))
    def deposit(self, amount):
        if amount <= 0 or self._is_frozen or self._closed:
            return "Invalid deposit."
        self._add_transaction(amount, 'deposit', "Deposit")
        return f"Deposit successful. New balance is {self.get_balance()}"
    def withdraw(self, amount):
        if self._is_frozen or self._closed:
            return "Account is not active."
        if amount <= 0:
            return "Invalid withdrawal amount."
        if self.get_balance() - amount < Account.minimum_balance:
            return "Insufficient funds."
        self._add_transaction(-amount, 'withdrawal', "Withdrawal")
        return f"Withdrawal successful. New balance is {self.get_balance()}"
    def transfer_funds(self, amount, other_account):
        withdrawal_result = self.withdraw(amount)
        if withdrawal_result.startswith("Withdrawal successful"):
            deposit_result = other_account.deposit(amount)
            if deposit_result.startswith("Deposit successful"):
                return "Transfer successful."
            else:
                self._add_transaction(amount, 'deposit', "Reversed Transfer")
                return f"Transfer failed: {deposit_result}"
        return withdrawal_result
    def request_loan(self, amount):
        if self._is_frozen or self._closed or amount <= 0:
            return "Loan request not allowed."
        self._loan += amount
        self._add_transaction(-amount, 'loan', f"Loan requested: {amount}")
        return f"Loan of {amount} approved. Current loan is {self._loan}"
    def repay_loan(self, amount):
        if amount <= 0:
            return "Invalid repayment."
        if amount >= self._loan:
            self._add_transaction(self._loan, 'repayment', "you have repaid your loan")
            self._loan = 0
            return "you have repaid your loan."
        else:
            self._loan -= amount
            self._add_transaction(amount, 'repayment', f"you have repaid insuffiecient amount for your loan"): {amount}")
            return f"you have repaid insuffiecient amount for your loan. Remaining amount is {self._loan}"
    def get_balance(self):
        balance = sum(txn.amount for txn in self._transactions)
        return balance - self._loan
    def view_account_details(self):
        return f"Owner: {self.owner}, Balance: {self.get_balance()}, Loan: {self._loan}, Account Number: {self._account_number}"
    def change_account_owner(self, new_owner):
        self.owner = new_owner
        return f"Account owner changed to {self.owner}"
    def account_statement(self):
        lines = ["Account Statement:"]
        for txn in self._transactions:
            lines.append(str(txn))
        lines.append(f"Current Balance is {self.get_balance()}")
        return "\n".join(lines)
    def apply_interest(self):
        if self._is_frozen or self._closed:
            return "no interest."
        interest = self.get_balance() * Account.interest_rate
        self._add_transaction(interest, 'interest', "Interest Applied")
        return f"Interest of {interest:.2f} applied. New balance is {self.get_balance()}"
    def freeze_account(self):
        self._is_frozen = True
        return "Account has been frozen."
    def unfreeze_account(self):
        self._is_frozen = False
        return "Account has been unfrozen."
    def set_minimum_balance(self, amount):
        Account.minimum_balance = amount
        return f"Minimum balance set to {amount}."
    def close_account(self):
        self._transactions.clear()
        self._loan = 0
        self._closed = True
        return "Your  has been account closed and all data havereset."
    def get_account_number(self):
        return self._account_number
    def get_loan_amount(self):
        return self._loan
    def is_account_frozen(self):
        return self._is_frozen
    def is_account_closed(self):
        return self._closed
    def get_transactions(self):
        return list(self._transactions)



