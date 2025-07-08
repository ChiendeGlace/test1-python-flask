def generate_plan(user_input, conn):
    cursor = conn.cursor()

    plan_type_map = {
        "Full Body": ["Full Body"],
        "Push-Pull": ["Push", "Pull"],
        "Upper-Lower": ["Upper", "Lower"],
        "Custom": ["Full Body", "Core", "Cardio", "Push", "Pull", "Upper", "Lower"]
    }
    routine_names = plan_type_map.get(user_input["plan_type"], ["Full Body"])

    print("\n🎯 Active filters:")
    print(f"Goal: {user_input['goal']}")
    print(f"Plan Type: {user_input['plan_type']} → Days: {', '.join(routine_names)}")
    print(f"Available equipment: {', '.join(user_input['available_equipment'])}")
    print(f"Preferred types: ",
          f"{'Free Weights' if user_input['free_weights'] else ''} ",
          f"{'Machines' if user_input['machines'] else ''} ",
          f"{'Bodyweight' if user_input['bodyweight'] else ''}")

    query = """
    SELECT DISTINCT e.id
    FROM exercises e
    LEFT JOIN exercise_equipment ee ON e.id = ee.exercise_id
    LEFT JOIN equipment eq ON eq.id = ee.equipment_id
    LEFT JOIN exercise_goals eg ON e.id = eg.exercise_id
    LEFT JOIN goals g ON g.id = eg.goal_id
    LEFT JOIN exercise_routines er ON e.id = er.exercise_id
    LEFT JOIN routine_types rt ON rt.id = er.routine_type_id
    WHERE g.name = ?
      AND (e.type = 'free weights' AND ? OR
           e.type = 'machine' AND ? OR
           e.type = 'bodyweight' AND ?)
      AND (eq.name IN ({eq_placeholders}) OR eq.name IS NULL)
      AND (rt.name IN ({rt_placeholders}) OR rt.name IS NULL)
    """.format(
        eq_placeholders=",".join(["?"] * len(user_input["available_equipment"])),
        rt_placeholders=",".join(["?"] * len(routine_names))
    )

    params = [
        user_input["goal"],
        user_input["free_weights"],
        user_input["machines"],
        user_input["bodyweight"],
        *user_input["available_equipment"],
        *routine_names
    ]

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Zwracamy tylko listę ID ćwiczeń
    return [row[0] for row in rows]