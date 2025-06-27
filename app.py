import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches

st.set_page_config(page_title="Risavika LNG Dashboard", layout="wide")
st.title("📊 Risavika LNG – Customer Segment Dashboard")

segments = [
    {"Segment": "Maritime Export - Spot Delivery",   "Price (€/MWh)": 37.9, "Cost (€/MWh)": 42.7, "Volume (ktpa)": 20},
    {"Segment": "Industry - Off-grid",               "Price (€/MWh)": 37.6, "Cost (€/MWh)": 44.8, "Volume (ktpa)": 15},
    {"Segment": "Industry - CHP",                    "Price (€/MWh)": 37.9, "Cost (€/MWh)": 43.9, "Volume (ktpa)": 17},  
     {"Segment": "Maritime Local - Ferries",          "Price (€/MWh)": 40.6, "Cost (€/MWh)": 43.8, "Volume (ktpa)": 40},
    {"Segment": "Maritime Export - Hub Bunkering",   "Price (€/MWh)": 41.3, "Cost (€/MWh)": 44.8, "Volume (ktpa)": 25},
    {"Segment": "Onshore Tankers - Local",           "Price (€/MWh)": 38.8, "Cost (€/MWh)": 44.9, "Volume (ktpa)": 23},
    {"Segment": "Maritime Local - OSVs",             "Price (€/MWh)": 39.8, "Cost (€/MWh)": 41.6, "Volume (ktpa)": 35},
    {"Segment": "Onshore Tankers - Highway",         "Price (€/MWh)": 41.5, "Cost (€/MWh)": 46.9, "Volume (ktpa)": 22},
    {"Segment": "Road Export - Germany Fleets",      "Price (€/MWh)": 41.6, "Cost (€/MWh)": 49.6, "Volume (ktpa)": 20},
    {"Segment": "Road Export - Sweden Fleets",       "Price (€/MWh)": 42.5, "Cost (€/MWh)": 49.6, "Volume (ktpa)": 25},
]

df = pd.DataFrame(segments)

st.subheader("📋 Input Table: Prices, Costs, and Volumes")
edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
edited_df["Margin (€/MWh)"] = edited_df["Price (€/MWh)"] - edited_df["Cost (€/MWh)"]

# Sidebar filters
st.sidebar.header("🔎 Filter Segments")
volume_threshold = st.sidebar.slider("Minimum Volume (ktpa)", min_value=0, max_value=int(df["Volume (ktpa)"].max()), value=0)
margin_option = st.sidebar.radio("Margin Type", options=["All", "Positive Margin", "Negative Margin"], index=0)
segment_keywords = ["Maritime", "Industry", "Onshore", "Road"]
segment_types = st.sidebar.multiselect("Segment Categories", options=segment_keywords, default=segment_keywords)

# Apply filters
filtered_df = edited_df[edited_df["Volume (ktpa)"] >= volume_threshold]
if margin_option == "Positive Margin":
    filtered_df = filtered_df[filtered_df["Margin (€/MWh)"] > 0]
elif margin_option == "Negative Margin":
    filtered_df = filtered_df[filtered_df["Margin (€/MWh)"] < 0]
filtered_df = filtered_df[filtered_df["Segment"].str.contains('|'.join(segment_types))]
# Sort by increasing price
filtered_df = filtered_df.sort_values(by="Cost (€/MWh)", ascending=True).reset_index(drop=True)

# Chart prep
volumes = filtered_df["Volume (ktpa)"].to_numpy()
prices = filtered_df["Price (€/MWh)"].to_numpy()
costs = filtered_df["Cost (€/MWh)"].to_numpy()
margins = filtered_df["Margin (€/MWh)"].to_numpy()
names = filtered_df["Segment"].to_list()

cumulative_volume = np.cumsum(volumes)
lefts = np.insert(cumulative_volume[:-1], 0, 0)

fig, ax = plt.subplots(figsize=(16, 8))
for i in range(len(filtered_df)):
    color = 'lightblue' if margins[i] >= 0 else 'lightcoral'
    ax.bar(lefts[i], prices[i], width=volumes[i], align='edge', color=color, edgecolor='black')
    ax.hlines(costs[i], lefts[i], lefts[i] + volumes[i], colors='black', linestyles='dashed')
    ax.text(lefts[i] + volumes[i]/2, prices[i]/2, names[i], ha='center', va='center', fontsize=8, color='black', rotation=45)
    ax.text(lefts[i] + volumes[i]/2, prices[i] + 1.5, f"Competing Cost: {prices[i]}€/MWh\nCost at RLP: {costs[i]}€/MWh", ha='center', va='bottom', fontsize=6, color='black')

ax.set_xlim(0, cumulative_volume[-1] if len(cumulative_volume) > 0 else 1)
ax.set_xlabel("LNG Volume (ktpa)")
ax.set_ylabel("Unit cost of direct substitute and cost to serve at RLP (\u20ac/MWh)")
ax.set_title("Demand Curve with Segment-Specific Cost to Serve")

legend_handles = [
    mpatches.Patch(color='lightblue', label='Positive Margin'),
    mpatches.Patch(color='lightcoral', label='Negative Margin'),
    plt.Line2D([0], [0], color='black', linestyle='dashed', label='Cost to Serve at RLP')
]
ax.legend(handles=legend_handles, loc='upper left')

st.pyplot(fig)
st.caption("Edit the table above to explore different customer pricing and cost-to-serve assumptions.")
