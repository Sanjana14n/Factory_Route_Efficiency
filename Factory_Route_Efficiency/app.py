import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Factory Route Efficiency Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

.stApp{
background-color:#F5F7FA;
}

section[data-testid="stSidebar"]{
background-color:#1E293B;
}

section[data-testid="stSidebar"] *{
color:white;
}

div[data-testid="metric-container"]{
background:white;
padding:15px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,.15);
border-left:6px solid #2563EB;
}

h1,h2,h3{
color:#1E3A8A;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

.main-title{
font-size:42px;
font-weight:700;
color:white;
text-align:center;
padding:20px;
border-radius:15px;
background:linear-gradient(90deg,#1E3C72,#2A5298);
box-shadow:0px 5px 20px rgba(0,0,0,0.2);
}

.subtitle{
text-align:center;
font-size:18px;
color:gray;
margin-top:10px;
margin-bottom:25px;
}

</style>

<div class="main-title">
📦 Factory-to-Customer Shipping Route Efficiency Analysis
</div>

<div class="subtitle">
Unified Mentor Internship Project | Nassau Candy Distributor Logistics Dashboard
</div>

""", unsafe_allow_html=True)


@st.cache_data
def load_data():

    df = pd.read_csv("Nassau Candy Distributor.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d-%m-%Y"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        format="%d-%m-%Y"
    )

    df["Shipping Lead Time"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    factory_map = {

        "Wonka Bar - Nutty Crunch Surprise":"Lot's O' Nuts",
        "Wonka Bar - Fudge Mallows":"Lot's O' Nuts",
        "Wonka Bar -Scrumdiddlyumptious":"Lot's O' Nuts",

        "Wonka Bar - Milk Chocolate":"Wicked Choccy's",
        "Wonka Bar - Triple Dazzle Caramel":"Wicked Choccy's",

        "Laffy Taffy":"Sugar Shack",
        "SweeTARTS":"Sugar Shack",
        "Nerds":"Sugar Shack",
        "Fun Dip":"Sugar Shack",
        "Fizzy Lifting Drinks":"Sugar Shack",

        "Everlasting Gobstopper":"Secret Factory",

        "Hair Toffee":"The Other Factory",

        "Lickable Wallpaper":"Secret Factory",
        "Wonka Gum":"Secret Factory",

        "Kazookles":"The Other Factory"
    }

    df["Factory"] = df["Product Name"].map(factory_map)

    df["Route"] = (
        df["Factory"] +
        " ➜ " +
        df["State/Province"]
    )

    max_days = df["Shipping Lead Time"].max()

    df["Efficiency Score"] = (
        100 -
        (
            df["Shipping Lead Time"] /
            max_days
        ) * 100
    ).round(2)

    return df


df = load_data()

st.sidebar.markdown("""
# ⚙ Dashboard Filters

---

Use the filters below to analyze shipping performance.

""")
start_date = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max()
)

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

states = st.sidebar.multiselect(
    "State",
    sorted(df["State/Province"].unique()),
    default=sorted(df["State/Province"].unique())
)

ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    sorted(df["Ship Mode"].unique()),
    default=sorted(df["Ship Mode"].unique())
)

filtered = df[
    (df["Order Date"] >= pd.Timestamp(start_date)) &
    (df["Order Date"] <= pd.Timestamp(end_date)) &
    (df["Region"].isin(regions)) &
    (df["State/Province"].isin(states)) &
    (df["Ship Mode"].isin(ship_modes))
]

if filtered.empty:
    st.warning("No data available.")
    st.stop()
# -----------------------------------------------------
# KPI SECTION
# -----------------------------------------------------

st.markdown("""
# 📊 Dashboard Overview

Analyze logistics performance across factories, routes, regions and ship modes.

""")
total_orders = len(filtered)
total_sales = filtered["Sales"].sum()
total_profit = filtered["Gross Profit"].sum()
avg_lead = filtered["Shipping Lead Time"].mean()
avg_efficiency = filtered["Efficiency Score"].mean()

delay_percent = (
    filtered["Shipping Lead Time"] > 5
).mean() * 100

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

st.markdown("""
<style>

.metric-card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 5px 15px rgba(0,0,0,.12);
text-align:center;
margin-bottom:10px;
}

.metric-card h2{
font-size:18px;
color:#666;
}

.metric-card h1{
color:#1565C0;
font-size:34px;
}

</style>
""",unsafe_allow_html=True)
c1.markdown(f"""
<div class="metric-card">
<h2>📦 Orders</h2>
<h1>{total_orders:,}</h1>
</div>
""",unsafe_allow_html=True)

c2.markdown(f"""
<div class="metric-card">
<h2>💰 Sales</h2>
<h1>${total_sales:,.0f}</h1>
</div>
""",unsafe_allow_html=True)

c3.markdown(f"""
<div class="metric-card">
<h2>💵 Profit</h2>
<h1>${total_profit:,.0f}</h1>
</div>
""",unsafe_allow_html=True)

c4.markdown(f"""
<div class="metric-card">
<h2>🚚 Lead Time</h2>
<h1>{avg_lead:.2f}</h1>
</div>
""",unsafe_allow_html=True)

c5.markdown(f"""
<div class="metric-card">
<h2>⚠ Delay</h2>
<h1>{delay_percent:.2f}%</h1>
</div>
""",unsafe_allow_html=True)

c6.markdown(f"""
<div class="metric-card">
<h2>⭐ Efficiency</h2>
<h1>{avg_efficiency:.2f}</h1>
</div>
""",unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------------------------
# ROUTE SUMMARY
# -----------------------------------------------------

route_summary = (
    filtered
    .groupby("Route")
    .agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Min_Lead=("Shipping Lead Time", "min"),
        Max_Lead=("Shipping Lead Time", "max"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Efficiency=("Efficiency Score", "mean")
    )
    .reset_index()
)

route_summary = route_summary.sort_values(
    "Avg_Lead_Time"
)

st.markdown("""
## 🏆 Route Performance Leaderboard

Top performing shipping routes based on lead time.

""")

st.dataframe(
    route_summary,
    use_container_width=True,
    hide_index=True
)

# -----------------------------------------------------
# TOP 10 ROUTES
# -----------------------------------------------------

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🥇 Top 10 Efficient Routes")

    top_routes = route_summary.head(10)

    fig = px.bar(
        top_routes,
        x="Avg_Lead_Time",
        y="Route",
        orientation="h",
        color="Efficiency",
        text="Shipments"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("🚨 Bottom 10 Inefficient Routes")

    bottom_routes = (
        route_summary
        .sort_values(
            "Avg_Lead_Time",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        bottom_routes,
        x="Avg_Lead_Time",
        y="Route",
        orientation="h",
        color="Avg_Lead_Time",
        text="Shipments"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")
# -----------------------------------------------------
# SHIP MODE ANALYSIS
# -----------------------------------------------------

st.markdown("""
## 🚚 Ship Mode Performance

Analyze shipping performance across different ship modes.
""")

ship_mode = (
    filtered
    .groupby("Ship Mode")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead=("Shipping Lead Time", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        ship_mode,
        x="Ship Mode",
        y="Avg_Lead",
        color="Ship Mode",
        text="Orders",
        title="Average Shipping Lead Time"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        ship_mode,
        names="Ship Mode",
        values="Orders",
        hole=0.45,
        title="Shipment Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------
# FACTORY PERFORMANCE
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 🏭 Factory Performance Dashboard
""")
factory_summary = (
    filtered
    .groupby("Factory")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead=("Shipping Lead Time", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Efficiency=("Efficiency Score", "mean")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        factory_summary,
        x="Factory",
        y="Avg_Lead",
        color="Efficiency",
        text="Orders",
        title="Factory Lead Time"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.bar(
        factory_summary,
        x="Factory",
        y="Sales",
        color="Factory",
        text="Sales",
        title="Factory Sales"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------
# REGIONAL ANALYSIS
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 🌍 Regional Bottleneck Analysis

Identify regions with the slowest shipping performance.
""")

region_summary = (
    filtered
    .groupby("Region")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead=("Shipping Lead Time", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        region_summary,
        x="Region",
        y="Avg_Lead",
        color="Avg_Lead",
        text="Orders",
        title="Average Lead Time by Region"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.scatter(
        region_summary,
        x="Orders",
        y="Avg_Lead",
        size="Sales",
        color="Profit",
        hover_name="Region",
        title="Regional Performance"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------
# STATE ANALYSIS
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 📍 State Performance

Analyze shipping performance by state or province.
""")

state_summary = (
    filtered
    .groupby("State/Province")
    .agg(
        Orders=("Order ID", "count"),
        Avg_Lead=("Shipping Lead Time", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

state_summary = state_summary.sort_values(
    "Avg_Lead",
    ascending=False
)

fig = px.bar(
    state_summary.head(20),
    x="State/Province",
    y="Avg_Lead",
    color="Avg_Lead",
    text="Orders",
    title="Top 20 Slowest States"
)

fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
# -----------------------------------------------------
# MONTHLY SHIPPING TREND
# -----------------------------------------------------

st.markdown("""
## 📈 Monthly Shipping Trend

Analyze shipping performance over time.
""")

monthly = filtered.copy()

monthly["Month"] = (
    monthly["Order Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_summary = (
    monthly
    .groupby("Month")
    .agg(
        Orders=("Order ID","count"),
        Avg_Lead=("Shipping Lead Time","mean"),
        Sales=("Sales","sum"),
        Profit=("Gross Profit","sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.line(
        monthly_summary,
        x="Month",
        y="Avg_Lead",
        markers=True,
        title="Monthly Average Shipping Lead Time"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.line(
        monthly_summary,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------
# GEOGRAPHIC ANALYSIS
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 🗺 Geographic Shipping Analysis

Analyze shipping performance across different geographic regions.
""")

geo_summary = (
    filtered
    .groupby(["Region","State/Province"])
    .agg(
        Orders=("Order ID","count"),
        Avg_Lead=("Shipping Lead Time","mean"),
        Sales=("Sales","sum")
    )
    .reset_index()
)

fig = px.treemap(
    geo_summary,
    path=["Region","State/Province"],
    values="Orders",
    color="Avg_Lead",
    hover_data=["Sales"],
    title="Region → State Shipping Performance"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------
# ROUTE DRILL DOWN
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 🔍 Route Drill Down

Analyze shipping performance for a specific route.
""")
selected_route = st.selectbox(
    "Select Route",
    sorted(filtered["Route"].dropna().unique())
)

route_data = filtered[
    filtered["Route"] == selected_route
]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Orders",
    len(route_data)
)

c2.metric(
    "Avg Lead",
    f"{route_data['Shipping Lead Time'].mean():.2f}"
)

c3.metric(
    "Sales",
    f"${route_data['Sales'].sum():,.0f}"
)

c4.metric(
    "Profit",
    f"${route_data['Gross Profit'].sum():,.0f}"
)

st.dataframe(
    route_data,
    use_container_width=True
)

# -----------------------------------------------------
# SHIPMENT TIMELINE
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 🕒 Shipment Timeline

Visualize the timeline of shipments for the selected route.
""")

timeline = route_data.sort_values(
    "Order Date"
)

fig = px.scatter(
    timeline,
    x="Order Date",
    y="Shipping Lead Time",
    color="Ship Mode",
    size="Sales",
    hover_data=[
        "Order ID",
        "Customer ID",
        "State/Province"
    ],
    title="Shipment Timeline"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# SHIPPING LEAD TIME DISTRIBUTION
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 📊 Shipping Lead Time Distribution

Analyze the distribution of shipping lead times across different ship modes.
""")

fig = px.histogram(
    filtered,
    x="Shipping Lead Time",
    color="Ship Mode",
    nbins=20,
    marginal="box",
    title="Lead Time Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# ROUTE EFFICIENCY RANKING
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## ⭐ Route Efficiency Ranking

Top performing routes based on efficiency scores.
""")
efficiency = (
    filtered
    .groupby("Route")
    .agg(
        Orders=("Order ID","count"),
        Efficiency=("Efficiency Score","mean")
    )
    .reset_index()
    .sort_values(
        "Efficiency",
        ascending=False
    )
)

st.dataframe(
    efficiency,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
# -----------------------------------------------------
# DOWNLOAD REPORTS
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 📥 Download Reports
""")

route_csv = route_summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Route Summary",
    data=route_csv,
    file_name="route_summary.csv",
    mime="text/csv"
)

filtered_csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=filtered_csv,
    file_name="filtered_dataset.csv",
    mime="text/csv"
)

# -----------------------------------------------------
# SUMMARY STATISTICS
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 📈 Summary Statistics
""")

st.dataframe(
    filtered.describe(include="all"),
    use_container_width=True
)

# -----------------------------------------------------
# BUSINESS INSIGHTS
# -----------------------------------------------------

st.markdown("---")
st.markdown("""
## 💡 Key Business Insights
""")

fastest = route_summary.loc[
    route_summary["Avg_Lead_Time"].idxmin()
]

slowest = route_summary.loc[
    route_summary["Avg_Lead_Time"].idxmax()
]

best_factory = factory_summary.loc[
    factory_summary["Efficiency"].idxmax()
]

worst_factory = factory_summary.loc[
    factory_summary["Efficiency"].idxmin()
]

highest_sales_region = region_summary.loc[
    region_summary["Sales"].idxmax()
]

most_delayed_region = region_summary.loc[
    region_summary["Avg_Lead"].idxmax()
]

best_ship_mode = ship_mode.loc[
    ship_mode["Avg_Lead"].idxmin()
]

worst_ship_mode = ship_mode.loc[
    ship_mode["Avg_Lead"].idxmax()
]

st.success(f"""
🏆 **Fastest Route:** {fastest['Route']}

Average Lead Time: **{fastest['Avg_Lead_Time']:.2f} Days**
""")

st.error(f"""
🚨 **Slowest Route:** {slowest['Route']}

Average Lead Time: **{slowest['Avg_Lead_Time']:.2f} Days**
""")

col1, col2 = st.columns(2)

with col1:

    st.info(f"""
🏭 **Best Factory**

Factory: **{best_factory['Factory']}**

Efficiency Score: **{best_factory['Efficiency']:.2f}**
""")

    st.success(f"""
🚚 **Best Ship Mode**

Mode: **{best_ship_mode['Ship Mode']}**

Average Lead Time: **{best_ship_mode['Avg_Lead']:.2f} Days**
""")

with col2:

    st.warning(f"""
🏭 **Factory Needing Improvement**

Factory: **{worst_factory['Factory']}**

Efficiency Score: **{worst_factory['Efficiency']:.2f}**
""")

    st.error(f"""
🚚 **Slowest Ship Mode**

Mode: **{worst_ship_mode['Ship Mode']}**

Average Lead Time: **{worst_ship_mode['Avg_Lead']:.2f} Days**
""")

st.info(f"""
🌍 **Highest Sales Region:** {highest_sales_region['Region']}

Total Sales: **${highest_sales_region['Sales']:,.2f}**
""")

st.warning(f"""
⚠️ **Most Delayed Region:** {most_delayed_region['Region']}

Average Lead Time: **{most_delayed_region['Avg_Lead']:.2f} Days**
""")

# -----------------------------------------------------
# RECOMMENDATIONS
# -----------------------------------------------------

st.markdown("---")
st.subheader("📌 Business Recommendations")

st.markdown("""
### Logistics Recommendations

- Optimize the routes with the highest average lead times.
- Increase usage of the fastest ship modes for high-value orders.
- Investigate bottlenecks in states with high shipping delays.
- Benchmark low-performing factories against the best-performing factory.
- Improve inventory planning for regions with high demand.
- Monitor monthly shipping trends to prepare for seasonal spikes.
- Use route efficiency scores to prioritize logistics improvements.
- Continuously monitor shipment performance through this dashboard.
""")

# -----------------------------------------------------
# PROJECT INFORMATION
# -----------------------------------------------------

st.markdown("---")

st.info("""
### 📦 Project Information

**Title:** Factory-to-Customer Shipping Route Efficiency Analysis

**Organization:** Nassau Candy Distributor

**Internship:** Unified Mentor

**Technology Stack**
- Python
- Pandas
- Streamlit
- Plotly
- NumPy

This dashboard provides operational insights into shipping efficiency, regional performance, route optimization, and logistics bottlenecks.
""")

# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------

st.markdown("---")

st.caption(
    "© 2026 | Factory-to-Customer Shipping Route Efficiency Analysis | Unified Mentor Internship Project"
)
# -----------------------------------------------------
# FACTORY DASHBOARD
# -----------------------------------------------------

st.markdown("---")
st.subheader("🏭 Factory Performance Dashboard")

factory_summary = (
    filtered.groupby("Factory")
    .agg(
        Orders=("Order ID", "count"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Avg_Lead=("Shipping Lead Time", "mean"),
        Efficiency=("Efficiency Score", "mean")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        factory_summary,
        x="Factory",
        y="Sales",
        color="Efficiency",
        text="Orders",
        title="Sales by Factory"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        factory_summary,
        x="Factory",
        y="Avg_Lead",
        color="Avg_Lead",
        text="Efficiency",
        title="Average Lead Time by Factory"
    )
    st.plotly_chart(fig, use_container_width=True)
    # -----------------------------------------------------
# FACTORY LOCATION MAP
# -----------------------------------------------------

st.markdown("---")
st.subheader("🗺 Factory Locations")

factory_coordinates = pd.DataFrame({
    "Factory":[
        "Lot's O' Nuts",
        "Wicked Choccy's",
        "Sugar Shack",
        "Secret Factory",
        "The Other Factory"
    ],
    "Latitude":[
        32.881893,
        32.076176,
        48.119140,
        41.446333,
        35.117500
    ],
    "Longitude":[
        -111.768036,
        -81.088371,
        -96.181150,
        -90.565487,
        -89.971107
    ]
})

fig = px.scatter_mapbox(
    factory_coordinates,
    lat="Latitude",
    lon="Longitude",
    hover_name="Factory",
    zoom=3,
    height=500
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin=dict(l=0,r=0,t=0,b=0)
)

st.plotly_chart(fig, use_container_width=True)
# -----------------------------------------------------
# EFFICIENCY GAUGE
# -----------------------------------------------------

st.markdown("---")
st.subheader("⭐ Overall Route Efficiency")

fig = go.Figure(go.Indicator(

    mode="gauge+number",

    value=filtered["Efficiency Score"].mean(),

    title={"text":"Efficiency Score"},

    gauge={
        "axis":{"range":[0,100]},
        "bar":{"color":"green"},
        "steps":[
            {"range":[0,40],"color":"red"},
            {"range":[40,70],"color":"orange"},
            {"range":[70,100],"color":"lightgreen"}
        ]
    }

))

st.plotly_chart(fig,use_container_width=True)
# -----------------------------------------------------
# TOP STATES
# -----------------------------------------------------

st.markdown("---")
st.subheader("🏆 Best Performing States")

best_states = (
    filtered.groupby("State/Province")
    .agg(
        Avg_Lead=("Shipping Lead Time","mean"),
        Orders=("Order ID","count")
    )
    .reset_index()
    .sort_values("Avg_Lead")
    .head(10)
)

fig = px.bar(
    best_states,
    x="Avg_Lead",
    y="State/Province",
    orientation="h",
    color="Avg_Lead",
    text="Orders"
)

st.plotly_chart(fig,use_container_width=True)
# -----------------------------------------------------
# FILTER SUMMARY
# -----------------------------------------------------

st.markdown("---")
st.subheader("📋 Current Filters")

st.info(f"""
**Regions:** {len(regions)}

**States:** {len(states)}

**Ship Modes:** {len(ship_modes)}

**Orders Selected:** {len(filtered)}
""")