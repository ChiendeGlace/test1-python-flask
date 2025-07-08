# Konfiguracja 1 – push/pull, siła, wolne ciężary + drążek
user_input_1 = {
    "free_weights": True,
    "machines": False,
    "bodyweight": True,
    "available_equipment": ["Barbell", "Dumbbell", "Pull-Up Bar", "Dip Bars", "Bench", "Bodyweight"],
    "training_days_per_week": 4,
    "session_length": 90,
    "engagement_level": "high",
    "goal": "Strength",
    "plan_type": "Push-Pull"
}

# Konfiguracja 2 – full body, hipertrofia, maszyny + hantle
user_input_2 = {
    "free_weights": True,
    "machines": True,
    "bodyweight": False,
    "available_equipment": ["Dumbbell", "Cable Machine", "Smith Machine", "Bench"],
    "training_days_per_week": 3,
    "session_length": 60,
    "engagement_level": "medium",
    "goal": "Hypertrophy",
    "plan_type": "Full Body"
}

# Konfiguracja 3 – upper/lower, funkcjonalność, masa ciała
user_input_3 = {
    "free_weights": False,
    "machines": False,
    "bodyweight": True,
    "available_equipment": ["Bodyweight", "Pull-Up Bar", "Parallettes"],
    "training_days_per_week": 5,
    "session_length": 45,
    "engagement_level": "low",
    "goal": "Functional Fitness",
    "plan_type": "Upper-Lower"
}

# Konfiguracja 4 – split, endurance, cardio maszyny
user_input_4 = {
    "free_weights": False,
    "machines": True,
    "bodyweight": True,
    "available_equipment": ["Treadmill", "Stationary Bike", "Rowing Machine", "Bodyweight"],
    "training_days_per_week": 6,
    "session_length": 40,
    "engagement_level": "medium",
    "goal": "Endurance",
    "plan_type": "Custom"
}

# Konfiguracja 5 – siła + hipertrofia, sprzęt domowy
user_input_5 = {
    "free_weights": True,
    "machines": False,
    "bodyweight": True,
    "available_equipment": ["Dumbbell", "Kettlebell", "Resistance Band", "Pull-Up Bar", "Bodyweight"],
    "training_days_per_week": 3,
    "session_length": 75,
    "engagement_level": "high",
    "goal": "Strength",
    "plan_type": "Upper-Lower"
}