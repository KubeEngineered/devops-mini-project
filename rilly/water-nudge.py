from datetime import datetime, time

def get_water_nudge(last_drank_time: datetime = None) -> dict:
    """
    Evaluates current time and last drink time to nudge the user for 250ml water.
    
    Active window: 06:00 AM to 10:00 PM
    Interval: Every 60 minutes
    """
    now = datetime.now()
    current_time = now.time()
    
    start_time = time(6, 0)   # 6:00 AM
    end_time = time(22, 0)    # 10:00 PM
    
    # Check if current time is outside the active daily window
    if not (start_time <= current_time <= end_time):
        return {
            "should_nudge": False,
            "message": "You're outside your daily hydration goal hours. Rest up for tomorrow!"
        }

    # If the user hasn't logged water today yet, prompt them
    if last_drank_time is None:
        return {
            "should_nudge": True,
            "message": "Welcome to Rilly! Time for your first 250ml cup of water today 💧"
        }

    # Calculate minutes since last logged drink
    time_diff_minutes = (now - last_drank_time).total_seconds() / 60

    if time_diff_minutes >= 60:
        return {
            "should_nudge": True,
            "message": "Time to hydrate! Grab a 250ml cup of water to hit your hourly Rilly goal 💧"
        }
    else:
        minutes_left = int(60 - time_diff_minutes)
        return {
            "should_nudge": False,
            "message": f"You're all set for now! Next 250ml nudge in {minutes_left} minutes."
        }


# Example Usage:
if __name__ == "__main__":
    from datetime import timedelta
    
    # Simulated case: Last drank 65 minutes ago
    last_sip = datetime.now() - timedelta(minutes=65)
    
    nudge = get_water_nudge(last_sip)
    if nudge["should_nudge"]:
        print(f"[Rilly Alert] {nudge['message']}")
    else:
        print(f"[Rilly Status] {nudge['message']}")
