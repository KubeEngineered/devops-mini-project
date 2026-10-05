from datetime import datetime, timedelta

class RillyPointsManager:
    def __init__(self, username: str):
        self.username = username
        self.total_lifetime_steps = 0
        # Stores earned points batches: [{"points": int, "earned_date": datetime}]
        self.points_ledger = []

    def add_steps(self, steps: int, activity_date: datetime = None):
        """Converts steps to points (1 point per 100 steps) and records entry."""
        if steps <= 0:
            print("Step count must be positive.")
            return

        activity_date = activity_date or datetime.now()
        earned_points = steps // 100
        
        self.total_lifetime_steps += steps
        
        if earned_points > 0:
            self.points_ledger.append({
                "points": earned_points,
                "earned_date": activity_date
            })
            print(f"✓ Added {steps:,} steps! You earned {earned_points} points.")
        else:
            print(f"✓ Added {steps} steps (Minimum 100 steps required to earn 1 point).")

    def purge_expired_points(self, current_date: datetime = None):
        """
        Scheduled job method: Removes points older than 180 days from earned_date.
        Should run daily or every 180 days on user accounts.
        """
        current_date = current_date or datetime.now()
        cutoff_date = current_date - timedelta(days=180)
        
        initial_points = self.get_available_points()
        
        # Keep only point batches earned within the 180-day window
        self.points_ledger = [
            batch for batch in self.points_ledger 
            if batch["earned_date"] > cutoff_date
        ]
        
        purged_points = initial_points - self.get_available_points()
        
        if purged_points > 0:
            print(f"⚠️ Maintenance Alert: {purged_points} unused points expired (>180 days old) and were removed.")
        else:
            print("✓ Maintenance Check: No expired points found.")

    def get_available_points(self) -> int:
        """Calculates total currently active/valid points."""
        return sum(batch["points"] for batch in self.points_ledger)

    def redeem_points(self, cost: int, item_name: str) -> bool:
        """Redeems available points using FIFO (First In, First Out) strategy."""
        if cost <= 0:
            print("Invalid redemption amount.")
            return False

        if self.get_available_points() < cost:
            print(f"❌ Insufficient points! Required: {cost}, Available: {self.get_available_points()}")
            return False

        remaining_to_deduct = cost
        
        # Deduct from oldest active batches first (FIFO)
        for batch in self.points_ledger:
            if batch["points"] <= remaining_to_deduct:
                remaining_to_deduct -= batch["points"]
                batch["points"] = 0
            else:
                batch["points"] -= remaining_to_deduct
                remaining_to_deduct = 0
                break

        # Cleanup empty entries
        self.points_ledger = [b for b in self.points_ledger if b["points"] > 0]
        
        print(f"🎉 Successfully redeemed '{item_name}' for {cost} points!")
        return True


# --- Demo / Testing the Logic ---
if __name__ == "__main__":
    today = datetime.now()
    
    # Initialize user
    user = RillyPointsManager(username="aditya")

    print("--- Day 1: User logs steps ---")
    user.add_steps(10500, activity_date=today - timedelta(days=181))  # Logged 181 days ago (Old batch)
    user.add_steps(4200, activity_date=today - timedelta(days=30))    # Logged 30 days ago (Recent batch)
    
    print(f"\nAvailable Points: {user.get_available_points()}")  # 105 + 42 = 147 points

    print("\n--- Day 180 Scheduled Maintenance Job Runs ---")
    user.purge_expired_points(current_date=today)
    
    print(f"Available Points after cleanup: {user.get_available_points()}")  # Only 42 points remain

    print("\n--- Redemptions ---")
    # Try buying a service/product
    user.redeem_points(30, "1-Month Premium Subscription")
    print(f"Remaining Balance: {user.get_available_points()}")