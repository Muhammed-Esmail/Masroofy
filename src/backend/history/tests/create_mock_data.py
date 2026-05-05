from cycle.models import CycleModel, ActiveCycleModel
from transaction.models import CategoryModel, TransactionModel
from datetime import date

# Categories
food = CategoryModel.objects.create(name="Food", description="Groceries")
transport = CategoryModel.objects.create(name="Transport", description="Travel")

# Cycle
cycle = CycleModel.objects.create(
    startDate=date(2026, 5, 1),
    endDate=date(2026, 5, 31),
    amount=5000
)

# Set as active
ActiveCycleModel.objects.all().delete()
ActiveCycleModel.objects.create(cycle=cycle)

# Transactions
TransactionModel.objects.create(amount=200, cycle=cycle, category=food,      log_date=date(2026, 5, 1), description="Supermarket", note=None)
TransactionModel.objects.create(amount=150, cycle=cycle, category=transport, log_date=date(2026, 5, 2), description="Uber",        note="peak hours")
TransactionModel.objects.create(amount=500, cycle=cycle, category=food,      log_date=date(2026, 5, 3), description="Restaurant",  note=None)