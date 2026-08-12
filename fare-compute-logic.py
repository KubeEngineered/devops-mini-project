def calculate_taxi_fare(
    distance_km: float, time_of_day_hour: int, demand_level: str
) -> float:
    # 1. Base Rates
    base_fare = 30.0  # Flat starting fare
    per_km_rate = 15.0  # Cost per kilometer

    # 2. Time-of-day Multiplier
    # Morning rush (8-10 AM) or evening rush (5-8 PM) -> 1.2x
    # Late night (11 PM-5 AM) -> 1.3x
    if 8 <= time_of_day_hour <= 10 or 17 <= time_of_day_hour <= 20:
        time_multiplier = 1.2
    elif time_of_day_hour >= 23 or time_of_day_hour < 5:
        time_multiplier = 1.3
    else:
        time_multiplier = 1.0

    # 3. Demand / Surge Multiplier
    surge_factors = {"low": 1.0, "medium": 1.2, "high": 1.6, "extreme": 2.0}
    demand_multiplier = surge_factors.get(demand_level.lower(), 1.0)

    # 4. Total Calculation
    distance_cost = distance_km * per_km_rate
    subtotal = (base_fare + distance_cost) * time_multiplier
    total_fare = subtotal * demand_multiplier

    return round(total_fare, 2)


# Example Usage:
# 12.5 km trip, at 8 PM (rush hour), under high demand
fare = calculate_taxi_fare(distance_km=12.5, time_of_day_hour=20, demand_level="high")
print(f"Total Fare: ₹{fare}")  # Output: ₹417.6



# End of file
# Code will be tested in CI pipeline stage in Github Actions
