class Category:

  # Function to receive the name of the class category and an empty ledger list
  def __init__(self, name):
    self.name = name
    self.ledger = []

  # Function to add deposit to the ledger list showing amount and descriptions
  # Appends a dictionary to the ledger list
  def deposit(self, amount, description=None):
    self.ledger.append({"amount": amount, "description": description})

  # Function to find current balance of the budget after deductions
  def current_balance(self):
    balance = 0
    for item in self.ledger:
      balance += item["amount"]
    return balance

  # Function to check if there are enough funds for transactions (Withdrawals & Transfers)
  def check_funds(self, amount):
    if amount > self.current_balance():
      return False
    else:
      return True

  # Function for withdrawals to the ledger list
  # Returns True if the withdrawal took place and False otherwise
  def withdraw(self, amount, description=None):
    if amount > self.current_balance():
      return False
    else:
      self.current_balance() - amount
      self.ledger.append({"amount": -amount, "description": description})
      return True

  # Function to transfer an amount from one budget category to another
  def transfer(self, amount, category):
    # Calling check_funds function to check if funds are available and make transfer
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {category.name}")
      # Deposit the amount into another category and add description
      category.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False

  # Function to print the budget category ledger and balance in the required format
  def __str__(self):
    title = self.name.center(30, "*") + "\n"
    items = ""
    for item in self.ledger:
      description = item["description"] \
          if item["description"] is not None else ""
      items += description[:23].ljust(23) + "{:.2f}".format(
        item["amount"]).rjust(7) + "\n"
    total = "Total: {:.2f}".format(self.current_balance())
    return title + items + total


def create_spend_chart(categories):
  # Finding the total spent and percentages for each category
  total_spent = 0
  category_spent = {}
  for category in categories:
    withdrawals = sum(transaction["amount"] for transaction in category.ledger
                      if transaction["amount"] < 0)
    category_spent[category.name] = withdrawals
    total_spent += withdrawals

  category_percentages = {}
  for category in category_spent:
    category_percentages[category] = int(
      (category_spent[category] / total_spent) * 100)

  # Constructing the chart
  chart = "Percentage spent by category\n"
  for i in range(100, -10, -10):
    chart += f"{i:3d}| "
    for category in category_percentages:
      if category_percentages[category] >= i:
        chart += "o  "
      else:
        chart += "   "
    chart += "\n"
  chart += "    " + "-" * (len(category_percentages) * 3 + 1) + "\n"

  # Adding category names to the chart
  max_name_length = max(len(category.name) for category in categories)
  for i in range(max_name_length):
    chart += "     "
    for category in categories:
      if i < len(category.name):
        chart += category.name[i] + "  "
      else:
        chart += "   "
    chart += "\n"

  return chart
