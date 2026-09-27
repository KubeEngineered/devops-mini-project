from datetime import datetime, time, timedelta

class RillyNutritionTracker:
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Define target nudge times
        self.meal_schedules = {
            "breakfast": time(8, 30),
            "lunch": time(13, 0),
            "dinner": time(20, 0)
        }
        # In-memory storage: { "YYYY-MM-DD": { "breakfast": {...}, ... } }
        self.logs = {}

    def check_meal_nudge(self, window_minutes: int = 30) -> dict:
        """
        Checks if current time aligns with a meal schedule and if the meal hasn't been logged yet.
        `window_minutes` allows the nudge to remain active for a brief period past the target time.
        """
        now = datetime.now()
        current_date_str = now.strftime("%Y-%m-%d")
        current_time = now.time()

        today_logs = self.logs.get(current_date_str, {})

        for meal, target_time in self.meal_schedules.items():
            # Calculate start and end boundary for the nudge window
            window_start = datetime.combine(now.date(), target_time)
            window_end = window_start + timedelta(minutes=window_minutes)

            if window_start <= now <= window_end:
                if meal not in today_logs:
                    return {
                        "should_nudge": True,
                        "meal": meal,
                        "message": f"Time for {meal.capitalize()}! Don't forget to log your meal in Rilly to track your daily macros 🥗"
                    }

        return {
            "should_nudge": False,
            "meal": None,
            "message": "No pending meal logging nudges right now."
        }

    def log_meal(self, meal_type: str, carbs_g: float, protein_g: float, fat_g: float, date_str: str = None):
        """
        Logs macros for a given meal. Defaults to today's date if not specified.
        """
        meal_type = meal_type.lower()
        if meal_type not in self.meal_schedules:
            raise ValueError(f"Invalid meal type. Must be one of {list(self.meal_schedules.keys())}")

        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        if date_str not in self.logs:
            self.logs[date_str] = {}

        self.logs[date_str][meal_type] = {
            "carbs_g": max(0.0, float(carbs_g)),
            "protein_g": max(0.0, float(protein_g)),
            "fat_g": max(0.0, float(fat_g)),
            "logged_at": datetime.now().isoformat()
        }

    def get_daily_totals(self, date_str: str = None) -> dict:
        """
        Calculates daily total intake of carbs, proteins, and fats in grams, 
        plus total caloric intake (Carbs/Protein = 4 kcal/g, Fat = 9 kcal/g).
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        today_meals = self.logs.get(date_str, {})

        total_carbs = sum(meal["carbs_g"] for meal in today_meals.values())
        total_protein = sum(meal["protein_g"] for meal in today_meals.values())
        total_fat = sum(meal["fat_g"] for meal in today_meals.values())

        total_calories = (total_carbs * 4) + (total_protein * 4) + (total_fat * 9)

        return {
            "date": date_str,
            "meals_logged": list(today_meals.keys()),
            "totals": {
                "carbs_g": round(total_carbs, 1),
                "protein_g": round(total_protein, 1),
                "fat_g": round(total_fat, 1),
                "calories_kcal": round(total_calories, 1)
            }
        }


# Example Usage:
if __name__ == "__main__":
    tracker = RillyNutritionTracker(user_id="user_101")

    # 1. Check for pending nudges
    nudge_status = tracker.check_meal_nudge()
    print("[Rilly Nudge Status]", nudge_status["message"])

    # 2. Simulate logging meals throughout the day
    tracker.log_meal(meal_type="breakfast", carbs_g=45.0, protein_g=20.0, fat_g=10.0)
    tracker.log_meal(meal_type="lunch", carbs_g=60.0, protein_g=35.0, fat_g=15.0)
    tracker.log_meal(meal_type="dinner", carbs_g=30.0, protein_g=40.0, fat_g=12.0)

    # 3. Calculate daily macro totals
    daily_summary = tracker.get_daily_totals()
    print("\n--- Daily Macro Summary ---")
    print(f"Date: {daily_summary['date']}")
    print(f"Meals Logged: {', '.join(daily_summary['meals_logged'])}")
    print(f"Carbohydrates : {daily_summary['totals']['carbs_g']}g")
    print(f"Protein       : {daily_summary['totals']['protein_g']}g")
    print(f"Fats          : {daily_summary['totals']['fat_g']}g")
    print(f"Total Energy  : {daily_summary['totals']['calories_kcal']} kcal")
