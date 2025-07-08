import sqlite3
from collections import defaultdict

def select_exercises_covering_muscles(filtered_ids, conn, activation_threshold=120):
    cursor = conn.cursor()

    # Pobierz aktywacje mięśniowe tylko dla wybranych ćwiczeń
    placeholders = ",".join(["?"] * len(filtered_ids))
    query = f"""
    SELECT
        e.id,
        e.name,
        mg.name AS muscle_name,
        ema.activation_level
    FROM exercises e
    JOIN exercise_muscle_activation ema ON e.id = ema.exercise_id
    JOIN muscle_groups mg ON ema.muscle_group_id = mg.id
    WHERE e.id IN ({placeholders})
    """
    cursor.execute(query, filtered_ids)
    rows = cursor.fetchall()

    # Ćwiczenia z aktywacją mięśni
    exercises = defaultdict(lambda: {
        "name": "",
        "activations": defaultdict(int)
    })

    for ex_id, ex_name, muscle, activation in rows:
        exercises[ex_id]["name"] = ex_name
        exercises[ex_id]["activations"][muscle] += activation if activation else 0

    total_activation = defaultdict(int)
    chosen_exercises = []

    while True:
        # Sprawdź, które mięśnie jeszcze nie osiągnęły progu
        remaining = {
            m: activation_threshold - a
            for m, a in total_activation.items()
            if activation_threshold - a > 0
        }

        if len(total_activation) > 0 and all(a >= activation_threshold for a in total_activation.values()):
            break

        best_ex_id = None
        best_contribution = 0

        for ex_id, ex in exercises.items():
            if any(e["id"] == ex_id for e in chosen_exercises):
                continue

            # Ile nowe ćwiczenie wnosi do brakujących mięśni?
            contribution = sum(min(activation_threshold - total_activation.get(m, 0), a)
                               for m, a in ex["activations"].items()
                               if total_activation.get(m, 0) < activation_threshold)

            if contribution > best_contribution:
                best_contribution = contribution
                best_ex_id = ex_id

        if best_ex_id is None:
            break

        ex = exercises[best_ex_id]
        chosen_exercises.append({
            "id": best_ex_id,
            "name": ex["name"],
            "activations": dict(ex["activations"])
        })

        for m, val in ex["activations"].items():
            total_activation[m] += val

    return chosen_exercises, dict(total_activation)