import sqlite3

def get_names(ids):
    if not ids:
        return []
    placeholders = ",".join(["?"] * len(ids))
    with sqlite3.connect("trening.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name FROM exercises WHERE id IN ({placeholders})", ids)
        return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

def compute_activation(chosen_ids, conn):
    cursor = conn.cursor()
    if not chosen_ids:
        return {}
    placeholders = ",".join(["?"] * len(chosen_ids))
    query = f"""
    SELECT mg.name, SUM(ema.activation_level)
    FROM exercise_muscle_activation ema
    JOIN muscle_groups mg ON mg.id = ema.muscle_group_id
    WHERE ema.exercise_id IN ({placeholders})
    GROUP BY mg.name
    """
    cursor.execute(query, chosen_ids)
    return {row[0]: row[1] for row in cursor.fetchall()}
