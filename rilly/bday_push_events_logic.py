from datetime import date, datetime
from typing import List, Dict


class RillyNotificationService:
    """Mock notification provider for sending Email, SMS, and Push Notifications."""
    
    @staticmethod
    def send_email(email: str, name: str):
        subject = f"🎉 Happy Birthday, {name}! Special Gift Inside from Rilly"
        body = f"Hi {name},\n\nThe Rilly team wishes you a wonderful birthday! Check your app for a special workout reward."
        print(f"  [EMAIL] Sent to '{email}' | Subject: {subject}")

    @staticmethod
    def send_sms(phone: str, name: str):
        message = f"Rilly: Happy Birthday {name}! 🎈 Enjoy 500 bonus step points credited to your account today."
        print(f"  [SMS] Sent to '{phone}' | Msg: {message}")

    @staticmethod
    def send_push_notification(user_id: str, name: str):
        title = f"Happy Birthday, {name}! 🎂"
        body = "Open Rilly to claim your birthday activity badge."
        print(f"  [PUSH] Sent to User ID '{user_id}' | Title: {title}")


class RillyUser:
    def __init__(self, user_id: str, name: str, email: str, phone: str, dob: date):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.dob = dob  # date(YYYY, MM, DD)
        self.last_birthday_wish_year = None  # Tracks last year a wish was sent

    def is_birthday_today(self, today: date = None) -> bool:
        """Checks if today matches the user's month and day of birth."""
        today = today or date.today()
        
        # Handle leap year birthdays (Feb 29) during non-leap years
        if self.dob.month == 2 and self.dob.day == 29:
            is_leap_year = (today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0))
            if not is_leap_year and today.month == 2 and today.day == 28:
                return True

        return self.dob.month == today.month and self.dob.day == today.day


class RillyBirthdayEngine:
    def __init__(self, notifier: RillyNotificationService):
        self.notifier = notifier

    def process_daily_birthday_wishes(self, users: List[RillyUser], current_date: date = None):
        """
        Scheduled daily batch job. Scans all user profiles and sends multi-channel
        birthday notifications if today is their birthday.
        """
        current_date = current_date or date.today()
        print(f"\n==========================================")
        print(f" Running Daily Birthday Job for: {current_date}")
        print(f"==========================================")

        wishes_sent_count = 0

        for user in users:
            # Check if today is the user's birthday and if they haven't been wished yet this year
            if user.is_birthday_today(current_date):
                if user.last_birthday_wish_year == current_date.year:
                    print(f"ℹ️ {user.name} already received birthday wishes for {current_date.year}. Skipping.")
                    continue

                print(f"\n🎂 Sending Birthday Wishes to {user.name} ({user.user_id})...")
                
                # Trigger all 3 communication channels
                self.notifier.send_email(user.email, user.name)
                self.notifier.send_sms(user.phone, user.name)
                self.notifier.send_push_notification(user.user_id, user.name)

                # Record execution to avoid duplicate messaging
                user.last_birthday_wish_year = current_date.year
                wishes_sent_count += 1

        print(f"\n✓ Completed: Sent birthday wishes to {wishes_sent_count} user(s).")


# --- Demo / Testing the Birthday Logic ---
if __name__ == "__main__":
    # Sample User Database
    user_db = [
        RillyUser("usr_101", "Aditya", "aditya@example.com", "+919876543210", dob=date(1988, 5, 24)),
        RillyUser("usr_102", "Rahul", "rahul@example.com", "+919123456789", dob=date(1995, 10, 8)),
        RillyUser("usr_103", "Priya", "priya@example.com", "+919988776655", dob=date(1992, 12, 15)),
    ]

    engine = RillyBirthdayEngine(notifier=RillyNotificationService())

    # Simulate running the scheduled job on October 8
    today_simulated = date(2026, 10, 8)
    engine.process_daily_birthday_wishes(user_db, current_date=today_simulated)

    # Re-running on the same day tests duplicate suppression
    engine.process_daily_birthday_wishes(user_db, current_date=today_simulated)