import streamlit as st
import json
import pandas as pd
import plotly.express as px
from scraper import run_analysis
import os

# Set page config
st.set_page_config(page_title="HealthAI Radar - Investment Tracker", page_icon="🏥", layout="wide")

st.title("🏥 HealthAI Radar: Performance & Sector Tracker")

# Sidebar for Control
st.sidebar.header("Radar Controls")

# Timeline Slider - Step=1 to prevent skipping
days = st.sidebar.slider("Timeline (Days Lookback)", min_value=1, max_value=365, value=30, step=1)

if st.sidebar.button("Refresh Radar Data"):
    with st.spinner(f"Running Analysis for past {days} days..."):
        run_analysis(days)
        # Force streamlit to notice the file change by clearing internal state if needed
        st.success(f"Radar refreshed for {days} days!")

# Load data - No cache to ensure we see the fresh scraper output
def load_data():
    if not os.path.exists('companies_with_sentiment.json'):
        run_analysis(days)
    with open('companies_with_sentiment.json', 'r') as f:
        return json.load(f)

data = load_data()
df = pd.DataFrame(data)

# --- Color Coordination Logic ---
# Extract all unique categories and create a consistent color map
all_categories = sorted(list(set([cat for sublist in df['categories'] for cat in sublist])))
color_palette = px.colors.qualitative.Plotly + px.colors.qualitative.Safe
sector_color_map = {cat: color_palette[i % len(color_palette)] for i, cat in enumerate(all_categories)}

# For the Heat Map, we use the "Primary Sector" (first category in the list) for coloring
df['Primary Sector'] = df['categories'].apply(lambda x: x[0] if x else "Uncategorized")
# --------------------------------

# Sidebar Filter
selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + all_categories)

# Filter Logic
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['categories'].apply(lambda x: selected_category in x)]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Companies Tracked", len(filtered_df))
col2.metric("Mean Heat Score", round(filtered_df['heat_score'].mean(), 1))
col3.metric("Tracking Window", f"{days} Days")

st.divider()

# 1. Main Heat Map (Top, Wide)
st.subheader("🔥 Investment Heat Map")
st.markdown("Bar height represents the **Heat Score**. Bar color represents the **Primary Sector**.")
fig_heat = px.bar(filtered_df.sort_values(by='heat_score', ascending=False), 
                 x='name', y='heat_score', 
                 color='Primary Sector',
                 color_discrete_map=sector_color_map,
                 title=f"Company Performance ({days} Day Lookback)",
                 labels={'heat_score': 'Heat Score', 'name': 'Company', 'Primary Sector': 'Sector'})

fig_heat.update_layout(xaxis_tickangle=-45, height=500)
st.plotly_chart(fig_heat, width='stretch')

st.divider()

# 2. Sector Composition Treemap (Bottom, Wide)
st.subheader("📊 Sector Composition & Market Coverage")
st.markdown("Treemap size corresponds to **Heat Score**. Colors match the Heat Map above.")

# Explode categories for sector visualization
sector_list = []
for index, row in filtered_df.iterrows():
    for cat in row['categories']:
        sector_list.append({
            'Sector': cat, 
            'Company': row['name'], 
            'Heat': row['heat_score']
        })

sector_df = pd.DataFrame(sector_list)

fig_tree = px.treemap(sector_df, 
                     path=['Sector', 'Company'], 
                     values='Heat',
                     color='Sector', 
                     color_discrete_map=sector_color_map,
                     title="Market Share and Performance by Sector")

fig_tree.update_layout(height=700) # Bigger treemap
st.plotly_chart(fig_tree, width='stretch')

# Detailed Data View
with st.expander("View Raw Radar Feed"):
    st.dataframe(filtered_df[['name', 'categories', 'heat_score', 'latest_headlines']].sort_values(by='heat_score', ascending=False), 
                 width='stretch')

st.caption(f"Radar Data Window: {days} Days | Last Analysis Run: {data[0].get('last_updated', 'Unknown')}")