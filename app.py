import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Risavika LNG Dashboard", layout="wide")
st.title("📊 Risavika LNG – Customer Segment Dashboard")

segments = [
    {"Segment": "Maritime Export - Spot Delivery",   "Price (€/MWh)": 40, "Cost (€/MWh)": 43, "Volume (ktpa)": 20},
    {"Segment": "Industry - Off-grid",               "Price (€/MWh)": 45, "Cost (€/MWh)": 45, "Volume (ktpa)": 15},
    {"Segment": "Maritime Local - Ferries",          "Price (€/MWh)": 50, "Cost (€/MWh)": 42, "Volume (ktpa)": 40},
    {"Segment": "Industry - CHP",                    "Price (€/MWh)": 50, "Cost (€/MWh)": 44, "Volume (ktpa)": 17},  
    {"Segment": "Maritime Export. - Hub Bunkering",   "Price (€/MWh)": 55, "Cost (€/MWh)": 44, "Volume (ktpa)": 25},
    {"Segment": "Onshore Tankers - Local",           "Price (€/MWh)": 58, "Cost (€/MWh)": 48, "Volume (ktpa)": 23},
    {"Segment": "Maritime Local. - OSVs",             "Price (€/MWh)": 60, "Cost (€/MWh)": 43, "Volume (ktpa)": 35},
    {"Segment": "Onshore Tankers - Highway",         "Price (€/MWh)": 60, "Cost (€/MWh)": 49, "Volume (ktpa)": 22},
    {"Segment": "Road Export - Germany Fleets",      "Price (€/MWh)": 68, "Cost (€/MWh)": 51, "Volume (ktpa)": 20},
    {"Segment": "Road Export - Sweden Fleets",       "Price (€/MWh)": 70, "Cost (€/MWh)": 47, "Volume (ktpa)": 25},
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

fig, ax = plt.subplots(figsize=(16, 8))
for i in range(len(edited_df)):
    color = 'lightblue' if margins[i] >= 0 else 'lightcoral'
    ax.bar(lefts[i], prices[i], width=volumes[i], align='edge', color=color, edgecolor='black')
    ax.hlines(costs[i], lefts[i], lefts[i] + volumes[i], colors='black', linestyles='dashed')
   # Add segment names **inside** the bars
for i in range(len(edited_df)):
    color = 'white' if margins[i] >= 0 else 'black'  # ensure contrast
    ax.text(
        lefts[i] + volumes[i]/2,                     # horizontal center of bar
        prices[i] / 2,                                # vertical mid-point of bar
        names[i],                                     # just the segment name
        ha='center', va='center',
        fontsize=8, color='black', rotation=45
    )
    ax.text(
    lefts[i] + volumes[i] / 2,
    prices[i] + 0.5,  # Slightly above the bar
    f"Competing Cost : {prices[i]}€/MWh\nCost at RLP: {costs[i]}€/MWh",
    ha='center', va='bottom',
    fontsize=6, color='black'
)

ax.set_xlim(0, cumulative_volume[-1])
ax.set_xlabel("LNG Volume (ktpa)")
ax.set_ylabel("Unit cost of direct substitute and cost to serve at RLP\n(€/MWh)")
ax.set_title("Demand Curve with Segment-Specific Cost to Serve")

import matplotlib.patches as mpatches
legend_handles = [
    mpatches.Patch(color='lightblue', label='Positive Margin'),
    mpatches.Patch(color='lightcoral', label='Negative Margin'),
    plt.Line2D([0], [0], color='black', linestyle='dashed', label='Cost to Serve at RLP')
]
ax.legend(handles=legend_handles, loc='upper left')
st.pyplot(fig)
st.caption("Edit the table above to explore different customer pricing and cost-to-serve assumptions.")
