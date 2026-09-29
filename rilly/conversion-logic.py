from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime

class RedemptionType(Enum):
    INTERNAL_PURCHASE = "RILLY_APP_PURCHASE"
    THIRD_PARTY_STORE = "THIRD_PARTY_STORE"

@dataclass
class Transaction:
    transaction_id: str
    redemption_type: RedemptionType
    points_used: int
    rupees_value: float
    description: str
    timestamp: datetime

class RillyWallet:
    CONVERSION_RATE = 100  # 100 points = 1 INR (1 Rs)

    def __init__(self, user_id: str, initial_points: int = 0):
        self.user_id = user_id
        self.points_balance = initial_points
        self.transaction_history = []

    def earn_points(self, points: int):
        """Adds points to user balance."""
        if points <= 0:
            raise ValueError("Earned points must be greater than zero.")
        self.points_balance += points

    @property
    def rupee_balance(self) -> float:
        """Converts current points balance to Rupees (100 points = 1 Rs)."""
        return self.points_balance / self.CONVERSION_RATE

    def redeem_points(self, points: int, redemption_type: RedemptionType, description: str) -> Transaction:
        """Redeems points for internal app purchases or third-party stores."""
        if points <= 0:
            raise ValueError("Redemption points must be greater than zero.")
        if points > self.points_balance:
            raise ValueError(f"Insufficient points. Required: {points}, Available: {self.points_balance}")

        # Deduct points balance
        self.points_balance -= points
        rupee_value = points / self.CONVERSION_RATE

        # Record transaction
        tx = Transaction(
            transaction_id=str(uuid.uuid4())[:8],
            redemption_type=redemption_type,
            points_used=points,
            rupees_value=rupee_value,
            description=description,
            timestamp=datetime.now()
        )
        self.transaction_history.append(tx)
        return tx

    def buy_rilly_product(self, product_name: str, price_in_rs: float):
        """Buys an internal product on the Rilly app using points balance."""
        required_points = int(price_in_rs * self.CONVERSION_RATE)
        tx = self.redeem_points(
            points=required_points,
            redemption_type=RedemptionType.INTERNAL_PURCHASE,
            description=f"Purchased product '{product_name}' on Rilly App"
        )
        return tx

    def redeem_to_third_party(self, partner_store: str, amount_in_rs: float):
        """Generates a voucher/redeems balance for third-party online stores."""
        required_points = int(amount_in_rs * self.CONVERSION_RATE)
        tx = self.redeem_points(
            points=required_points,
            redemption_type=RedemptionType.THIRD_PARTY_STORE,
            description=f"Voucher issued for {partner_store}"
        )
        return tx


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Create wallet with initial 50,000 points
    user_wallet = RillyWallet(user_id="usr_987", initial_points=50000)

    print(f"Initial Points Balance: {user_wallet.points_balance} pts")
    print(f"Equivalent Rupee Balance: ₹{user_wallet.rupee_balance:.2f}\n")

    # 1. Buy an internal item on Rilly App worth ₹150 (Requires 15,000 points)
    tx1 = user_wallet.buy_rilly_product("Rilly Premium Shaker", price_in_rs=150.0)
    print(f"[SUCCESS] {tx1.description} | Spent: {tx1.points_used} pts (₹{tx1.rupees_value}) | Tx ID: {tx1.transaction_id}")

    # 2. Redeem points at a third-party partner store (e.g., Amazon/Myntra) worth ₹250 (Requires 25,000 points)
    tx2 = user_wallet.redeem_to_third_party("Amazon Pay Voucher", amount_in_rs=250.0)
    print(f"[SUCCESS] {tx2.description} | Spent: {tx2.points_used} pts (₹{tx2.rupees_value}) | Tx ID: {tx2.transaction_id}")

    # Final summary
    print(f"\nRemaining Points: {user_wallet.points_balance} pts")
    print(f"Remaining Rupee Value: ₹{user_wallet.rupee_balance:.2f}")