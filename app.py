import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Risavika LNG Dashboard", layout="wide")
st.title("📊 Risavika LNG – Customer Segment Dashboard")

segments = [
    {"Segment": "Maritime Export - Hub Bunkering",   "Price (€/MWh)": 35, "Cost (€/MWh)": 46, "Volume (ktpa)": 25},
    {"Segment": "Maritime Export - Spot Delivery",   "Price (€/MWh)": 36, "Cost (€/MWh)": 47, "Volume (ktpa)": 20},
    {"Segment": "Maritime Local - Ferries",          "Price (€/MWh)": 41, "Cost (€/MWh)": 43, "Volume (ktpa)": 40},
    {"Segment": "Maritime Local - OSVs",             "Price (€/MWh)": 42, "Cost (€/MWh)": 43, "Volume (ktpa)": 35},
    {"Segment": "Industry - CHP",                    "Price (€/MWh)": 47, "Cost (€/MWh)": 42, "Volume (ktpa)": 17},
    {"Segment": "Road Export - Sweden Fleets",       "Price (€/MWh)": 48, "Cost (€/MWh)": 43, "Volume (ktpa)": 27},
    {"Segment": "Industry - Off-grid",               "Price (€/MWh)": 49, "Cost (€/MWh)": 46, "Volume (ktpa)": 15},
    {"Segment": "Road Export - Germany Fleets",      "Price (€/MWh)": 51, "Cost (€/MWh)": 47, "Volume (ktpa)": 20},
    {"Segment": "Onshore Tankers - Highway",         "Price (€/MWh)": 53, "Cost (€/MWh)": 48, "Volume (ktpa)": 22},
    {"Segment": "Onshore Tankers - Local",           "Price (€/MWh)": 58, "Cost (€/MWh)": 48, "Volume (ktpa)": 23},
]
df = pd.DataFrame(segments)

st.subheader("🧾 Input Table: Prices, Costs, and Volumes")
edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
edited_df["Margin (€/MWh)"] = edited_df["Price (€/MWh)"] - edited_df["Cost (€/MWh)"]

volumes = edited_df["Volume (ktpa)"].to_numpy()
prices = edited_df["Price (€/MWh)"].to_numpy()
costs = edited_df["Cost (€/MWh)"].to_numpy()
margins = edited_df["Margin (€/MWh)"].to_numpy()
names = edited_df["Segment"].to_list()

cumulative_volume = np.cumsum(volumes)
lefts = np.insert(cumulative_volume[:-1], 0, 0)

fig, ax = plt.subplots(figsize=(14, 7))
for i in range(len(edited_df)):
    color = 'lightblue' if margins[i] >= 0 else 'lightcoral'
    ax.bar(lefts[i], prices[i], width=volumes[i], align='edge', color=color, edgecolor='black')
    ax.hlines(costs[i], lefts[i], lefts[i] + volumes[i], colors='black', linestyles='dashed')
    ax.text(lefts[i] + volumes[i]/2, prices[i] + 1,
            f"{names[i]}\nPrice: {prices[i]}€/MWh\nCost: {costs[i]}€/MWh",
            rotation=90, ha='center', va='bottom', fontsize=12)

ax.set_xlim(0, cumulative_volume[-1])
ax.set_xlabel("LNG Volume (ktpa)")
ax.set_ylabel("Price / Cost (€/MWh)")
ax.set_title("Demand Curve with Segment-Specific Cost to Serve")

import matplotlib.patches as mpatches
legend_handles = [
    mpatches.Patch(color='lightblue', label='Positive Margin'),
    mpatches.Patch(color='lightcoral', label='Negative Margin'),
    plt.Line2D([0], [0], color='black', linestyle='dashed', label='Cost to Serve')
]
ax.legend(handles=legend_handles, loc='upper left')
st.pyplot(fig)

st.caption("Edit the table above to explore different customer pricing and cost-to-serve assumptions.")
