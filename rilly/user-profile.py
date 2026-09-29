def calculate_daily_nutrients(age: int, weight_kg: float, height_cm: float, gender: str, activity_level: float = 1.2):
    """
    Suggests daily macronutrient and basic mineral guidelines.
    
    gender: 'male' or 'female'
    activity_level: 
        1.2   - Sedentary (little or no exercise)
        1.375 - Lightly active (light exercise 1-3 days/week)
        1.55  - Moderately active (moderate exercise 3-5 days/week)
        1.725 - Very active (hard exercise 6-7 days/week)
    """
    gender_clean = gender.strip().lower()
    
    # 1. Calculate Basal Metabolic Rate (BMR) via Harris-Benedict Formula
    if gender_clean == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender_clean == 'female':
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    # Total Daily Energy Expenditure (TDEE)
    tdee = bmr * activity_level

    # 2. Calculate Macronutrients (4 kcal/g protein, 4 kcal/g carbs, 9 kcal/g fat)
    # Typical balance: 25% Protein, 50% Carbs, 25% Fat
    protein_g = (tdee * 0.25) / 4
    carbs_g = (tdee * 0.50) / 4
    fat_g = (tdee * 0.25) / 9

    # 3. Recommended Dietary Allowance (RDA) for Key Minerals
    if gender_clean == 'male':
        calcium_mg = 1000 if age <= 70 else 1200
        iron_mg = 8
        sodium_mg = 2300  # Upper safe limit guideline
        potassium_mg = 3400
    else:
        calcium_mg = 1000 if age <= 50 else 1200
        iron_mg = 18 if age <= 50 else 8
        sodium_mg = 2300
        potassium_mg = 2600

    return {
        "calories_kcal": round(tdee, 1),
        "macronutrients_grams": {
            "protein": round(protein_g, 1),
            "carbohydrates": round(carbs_g, 1),
            "fats": round(fat_g, 1)
        },
        "minerals_mg": {
            "calcium": calcium_mg,
            "iron": iron_mg,
            "sodium": sodium_mg,
            "potassium": potassium_mg
        }
    }


# Example Usage:
user_profile = {
    "age": 28,
    "weight_kg": 70.0,
    "height_cm": 175.0,
    "gender": "male"
}

recommendations = calculate_daily_nutrients(**user_profile)

print(f"Daily Energy Need: {recommendations['calories_kcal']} kcal\n")
print("Macronutrients:")
for macro, amount in recommendations["macronutrients_grams"].items():
    print(f"  - {macro.capitalize()}: {amount} g")

print("\nKey Mineral Guidelines:")
for mineral, amount in recommendations["minerals_mg"].items():
    print(f"  - {mineral.capitalize()}: {amount} mg")