import sqlite3
from helpers import get_names, compute_activation
from user_config import user_input_1
from gen_plan import generate_plan

def update_routine(action, exercise_id, chosen, filtered_ids):
    if action == "add":
        if exercise_id in filtered_ids and exercise_id not in chosen:
            chosen.append(exercise_id)
    elif action == "remove":
        if exercise_id in chosen:
            chosen.remove(exercise_id)
    return chosen

def process_update(action, ex_id, chosen):
    conn = sqlite3.connect("trening.db")
    filtered_ids = generate_plan(user_input_1, conn)

    chosen = update_routine(action, ex_id, chosen, filtered_ids)
    chosen_named = get_names(chosen)
    activation = compute_activation(chosen, conn)
    available = get_names([i for i in filtered_ids if i not in chosen])
    conn.close()

    return {
        "current": chosen_named,
        "available": available,
        "activation": activation,
        "chosen": chosen
    }