import streamlit as st
from model import (
    solve_cargo_optimization,
    items,
    utility,
    weight,
    volume,
    cost,
    medical_items,
    food_items,
    fragile_items,
    refrigerated_items,
)


def build_results_table(selected_items):
    return [
        {
            "Item": item,
            "Utility": utility[item],
            "Weight": weight[item],
            "Volume": volume[item],
            "Cost": cost[item],
            "Medical": item in medical_items,
            "Food": item in food_items,
            "Fragile": item in fragile_items,
            "Refrigerated": item in refrigerated_items,
        }
        for item in selected_items
    ]


st.set_page_config(
    page_title="Humanitarian Air Cargo Optimization",
    page_icon="✈️",
    layout="centered",
)

st.title("Humanitarian Air Cargo Optimization")
st.write(
    "Use this interactive model to choose the best combination of cargo items while respecting weight, volume, budget, and humanitarian constraints."
)

with st.sidebar.expander("Capacity & Budget Settings", expanded=True):
    max_weight = st.number_input("Maximum weight capacity", min_value=1, value=65, step=1)
    max_volume = st.number_input("Maximum volume capacity", min_value=1, value=12, step=1)
    max_cost = st.number_input("Maximum budget", min_value=1, value=120, step=1)

with st.sidebar.expander("Humanitarian Constraints", expanded=True):
    min_medical = st.number_input(
        "Minimum medical items", min_value=0, max_value=len(medical_items), value=2, step=1
    )
    min_food = st.number_input(
        "Minimum food items", min_value=0, max_value=len(food_items), value=1, step=1
    )
    max_fragile = st.number_input(
        "Maximum fragile items", min_value=0, max_value=len(fragile_items), value=2, step=1
    )
    max_refrigerated = st.number_input(
        "Maximum refrigerated items",
        min_value=0,
        max_value=len(refrigerated_items),
        value=2,
        step=1,
    )
    min_items = st.number_input(
        "Minimum total items", min_value=0, max_value=len(items), value=4, step=1
    )

if st.button("Run Optimization"):
    results = solve_cargo_optimization(
        max_weight=max_weight,
        max_volume=max_volume,
        max_cost=max_cost,
        min_medical=min_medical,
        min_food=min_food,
        max_fragile=max_fragile,
        max_refrigerated=max_refrigerated,
        min_items=min_items,
    )

    st.subheader("Optimization Results")
    st.write("**Status:**", results["status"])

    if results["status"] == "Optimal":
        st.metric("Maximum Utility", results["total_utility"])
        st.metric("Total Weight", f"{results['total_weight']} / {max_weight}")
        st.metric("Total Volume", f"{results['total_volume']} / {max_volume}")
        st.metric("Total Cost", f"{results['total_cost']} / {max_cost}")

        utilization_cols = st.columns(3)
        utilization_cols[0].metric(
            "Weight Utilization",
            f"{(results['total_weight'] / max_weight) * 100:.1f}%",
        )
        utilization_cols[1].metric(
            "Volume Utilization",
            f"{(results['total_volume'] / max_volume) * 100:.1f}%",
        )
        utilization_cols[2].metric(
            "Budget Utilization",
            f"{(results['total_cost'] / max_cost) * 100:.1f}%",
        )

        st.write("### Selected Cargo Items")
        st.table(build_results_table(results["selected_items"]))
    else:
        st.warning(
            "No feasible solution found for the current constraints. Try relaxing capacity or requirement settings."
        )

st.write("---")
st.write("### Item Definitions")
item_table = [
    {
        "Item": i,
        "Utility": utility[i],
        "Weight": weight[i],
        "Volume": volume[i],
        "Cost": cost[i],
        "Medical": i in medical_items,
        "Food": i in food_items,
        "Fragile": i in fragile_items,
        "Refrigerated": i in refrigerated_items,
    }
    for i in items
]
st.dataframe(item_table)
