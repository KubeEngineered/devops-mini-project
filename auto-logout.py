from datetime import datetime, timedelta, timezone


def check_session_validity(last_active_at: datetime) -> dict:
    """Checks if user session is valid or expired (> 15 days)."""
    current_time = datetime.now(timezone.utc)
    inactivity_limit = timedelta(days=15)

    # Calculate time passed since last activity
    if current_time - last_active_at > inactivity_limit:
        return {
            "status": "LOGOUT",
            "message": "Session expired due to 15 days of inactivity. Please log in again.",
        }

    return {"status": "ACTIVE", "message": "Session valid."}


# --- Example Usage ---

# 1. User last opened app 16 days ago
last_active = datetime.now(timezone.utc) - timedelta(days=16)
session = check_session_validity(last_active)

if session["status"] == "LOGOUT":
    # Clear local Auth token / Session cookie and redirect to Login UI
    print(session["message"])
else:
    # Update last_active_at timestamp in database/storage to current_time
    print("Welcome back!")


# End of file
