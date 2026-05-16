from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD, LpStatus, value

# Data definitions
items = ["A", "B", "C", "D", "E", "F", "G", "H"]

utility = {
    "A": 60,
    "B": 80,
    "C": 90,
    "D": 75,
    "E": 30,
    "F": 75,
    "G": 60,
    "H": 30,
}

weight = {
    "A": 10,
    "B": 20,
    "C": 30,
    "D": 15,
    "E": 5,
    "F": 18,
    "G": 12,
    "H": 8,
}

volume = {
    "A": 2,
    "B": 3,
    "C": 4,
    "D": 3,
    "E": 1,
    "F": 3,
    "G": 2,
    "H": 2,
}

cost = {
    "A": 25,
    "B": 40,
    "C": 55,
    "D": 20,
    "E": 10,
    "F": 35,
    "G": 30,
    "H": 15,
}

medical_items = ["A", "B", "C"]
food_items = ["D", "E"]
fragile_items = ["A", "B", "F"]
refrigerated_items = ["B", "C"]


def solve_cargo_optimization(
    max_weight=65,
    max_volume=12,
    max_cost=120,
    min_medical=2,
    min_food=1,
    max_fragile=2,
    max_refrigerated=2,
    min_items=4,
):
    model = LpProblem("Humanitarian_Cargo_Optimization", LpMaximize)

    x = LpVariable.dicts("Select", items, cat="Binary")

    model += lpSum(utility[i] * x[i] for i in items)

    model += lpSum(weight[i] * x[i] for i in items) <= max_weight
    model += lpSum(volume[i] * x[i] for i in items) <= max_volume
    model += lpSum(cost[i] * x[i] for i in items) <= max_cost

    if min_medical > 0:
        model += lpSum(x[i] for i in medical_items) >= min_medical

    if min_food > 0:
        model += lpSum(x[i] for i in food_items) >= min_food

    if max_fragile is not None:
        model += lpSum(x[i] for i in fragile_items) <= max_fragile

    if max_refrigerated is not None:
        model += lpSum(x[i] for i in refrigerated_items) <= max_refrigerated

    if min_items > 0:
        model += lpSum(x[i] for i in items) >= min_items

    solver = PULP_CBC_CMD(msg=False)
    model.solve(solver)

    status = LpStatus[model.status]
    selected_items = [i for i in items if x[i].varValue == 1]
    total_weight = sum(weight[i] * (x[i].varValue or 0) for i in items)
    total_volume = sum(volume[i] * (x[i].varValue or 0) for i in items)
    total_cost = sum(cost[i] * (x[i].varValue or 0) for i in items)
    total_utility = value(model.objective)

    return {
        "status": status,
        "selected_items": selected_items,
        "total_weight": total_weight,
        "total_volume": total_volume,
        "total_cost": total_cost,
        "total_utility": total_utility,
    }
