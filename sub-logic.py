from datetime import datetime
import time
import schedule


class Customer:

    def __init__(self, name: str, address: str, wallet_balance: float):
        self.name = name
        self.address = address
        self.wallet_balance = wallet_balance

    def add_funds(self, amount: float):
        self.wallet_balance += amount
        print(f"[{self.name}] Added ₹{amount}. New Balance: ₹{self.wallet_balance}")


class MilkSubscription:

    def __init__(
        self,
        customer: Customer,
        product_name: str = "Daily Milk (1L)",
        price: float = 60.0,
    ):
        self.customer = customer
        self.product_name = product_name
        self.price = price
        self.is_active = True

    def process_daily_delivery(self):
        """Processes the daily milk delivery and deducts funds from wallet."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not self.is_active:
            print(f"[{now}] Subscription for {self.customer.name} is paused.")
            return

        # Check if customer has enough wallet balance
        if self.customer.wallet_balance >= self.price:
            self.customer.wallet_balance -= self.price
            print(f"[{now}] SUCCESS: Delivered {self.product_name} to '{self.customer.address}'.")
            print(
                f"          Deducted: ₹{self.price} | Remaining Balance: ₹{self.customer.wallet_balance}\n"
            )
        else:
            print(
                f"[{now}] FAILED: Insufficient balance for {self.customer.name}."
            )
            print(
                f"          Required: ₹{self.price} | Available: ₹{self.customer.wallet_balance}"
            )
            print(f"          Delivery skipped. Please top up wallet!\n")


# --- Setup Subscriptions & Cron Job ---

# Create sample customer and subscription
user = Customer(
    name="Rahul Sharma",
    address="Flat 302, Green Apartments, Sector 45",
    wallet_balance=200.0,  # Enough for ~3 days at ₹60/day
)
subscription = MilkSubscription(customer=user, price=60.0)

# Schedule delivery every day at 05:30 AM (well before 7:00 AM target)
schedule.every().day.at("05:30").do(subscription.process_daily_delivery)


# Run manually once to simulate an execution right now
print("--- Initial Test Run ---")
subscription.process_daily_delivery()

# Start scheduler loop (keeps process alive in production)
print("Scheduler started. Waiting for next run at 05:30 AM daily...")
# while True:
#     schedule.run_pending()
#     time.sleep(60)



# End of file
