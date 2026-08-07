THRESHOLD = 100.0  # Rs. 100 limit

def send_push_notification(user_id: str, balance: float):
    """Mock function representing your FCM/APNs push notification service."""
    payload = {
        "title": "Low Balance Alert",
        "body": f"Your account balance is Rs. {balance:.2f}, which is below Rs. {THRESHOLD}. Please recharge.",
        "data": {"type": "LOW_BALANCE_ALERT"}
    }
    print(f"[PUSH SENT to {user_id}]: {payload['body']}")


def process_transaction(user_account: dict, new_balance: float):
    """
    Evaluates balance changes and sends a notification if balance drops below threshold.
    """
    user_account["balance"] = new_balance

    # Trigger push if balance drops below 100 AND user hasn't been notified yet
    if new_balance < THRESHOLD and not user_account.get("low_balance_notified", False):
        send_push_notification(user_account["user_id"], new_balance)
        user_account["low_balance_notified"] = True  # Prevent spamming on next transaction

    # Reset the flag if the user tops up above 100 Rs.
    elif new_balance >= THRESHOLD and user_account.get("low_balance_notified", False):
        user_account["low_balance_notified"] = False


# --- Example Usage ---
user = {
    "user_id": "usr_9876",
    "balance": 250.0,
    "low_balance_notified": False
}

# 1. Spent Rs. 180 (Balance: 70 -> Below threshold)
process_transaction(user, 70.0)

# 2. Spent Rs. 20 (Balance: 50 -> Still below, but alert flag prevents duplicate push)
process_transaction(user, 50.0)

# 3. Top-up Rs. 100 (Balance: 150 -> Resets notification flag)
process_transaction(user, 150.0)


# End of file
