from utils import add_expense, load_expenses
import random
import datetime

# Some categories to randomly choose from
categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment"]

# Generate 10 random expenses
for _ in range(10):
    date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 30))
    category = random.choice(categories)
    amount = round(random.uniform(50, 500), 2)
    add_expense(date, category, amount)

print("✅ Sample expenses added!")
print(load_expenses())
