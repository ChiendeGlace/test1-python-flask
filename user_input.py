import sqlite3

def get_user_input():
    print("📝 Fill in the info and I’ll generate your DPM workout plan!")

    # Połączenie z bazą
    conn = sqlite3.connect("trening.db")
    cursor = conn.cursor()

    # Wczytaj wszystkie dostępne wartości z bazy
    cursor.execute("SELECT name FROM equipment")
    equipment_options = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM goals")
    goal_options = [row[0] for row in cursor.fetchall()]

    # plan_type (nie z bazy – to styl planu)
    plan_style_options = ["Full Body", "Push-Pull", "Upper-Lower", "Custom"]

    print("\n🔧 Training style:")
    for i, p in enumerate(plan_style_options, 1):
        print(f"{i}. {p}")
    plan_style_index = int(input("Choose your plan type (number): "))
    plan_type = plan_style_options[plan_style_index - 1]

    print("\n🎯 Training goals:")
    for i, g in enumerate(goal_options, 1):
        print(f"{i}. {g}")
    goal_index = int(input("Choose your goal (number): "))
    goal = goal_options[goal_index - 1]

    print("\n📦 Available equipment:")
    for i, item in enumerate(equipment_options, 1):
        print(f"{i}. {item}")
    selected = input("Enter numbers of equipment you have (e.g. 1,3,5): ")
    selected_ids = [int(x.strip()) for x in selected.split(",") if x.strip().isdigit()]
    available_equipment = [equipment_options[i - 1] for i in selected_ids if 0 < i <= len(equipment_options)]

    # Preferencje ogólne
    free_weights = input("Do you want to train with free weights? (yes/no): ").strip().lower() == "yes"
    machines = input("Do you want to use machines? (yes/no): ").strip().lower() == "yes"
    bodyweight = input("Do you want bodyweight exercises? (yes/no): ").strip().lower() == "yes"

    # Sesja
    training_days_per_week = int(input("\nHow many days per week do you want to train? (1–7): "))
    session_length = int(input("How long should one session be (in minutes)? e.g. 45: "))
    engagement_level = input("Engagement level (low/medium/high): ").strip().lower()

    conn.close()

    return {
        "free_weights": free_weights,
        "machines": machines,
        "bodyweight": bodyweight,
        "available_equipment": available_equipment,
        "training_days_per_week": training_days_per_week,
        "session_length": session_length,
        "engagement_level": engagement_level,
        "goal": goal,
        "plan_type": plan_type
    }