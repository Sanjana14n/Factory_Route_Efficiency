import pandas as pd
import numpy as np

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("Nassau Candy Distributor.csv")

# -----------------------------
# DATE CONVERSION
# -----------------------------

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d-%m-%Y"
)

# -----------------------------
# SHIPPING LEAD TIME
# -----------------------------

df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# -----------------------------
# FACTORY MAPPING
# -----------------------------

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

# -----------------------------
# EFFICIENCY SCORE
# -----------------------------

max_days = df["Shipping Lead Time"].max()

df["Efficiency Score"] = (
    100 -
    (
        df["Shipping Lead Time"] /
        max_days
    ) * 100
).round(2)

# -----------------------------
# DATA INFORMATION
# -----------------------------

print("=" * 80)
print("DATASET INFORMATION")
print("=" * 80)

print(df.info())

print("=" * 80)

print(df.describe(include="all"))

# -----------------------------
# MISSING VALUES
# -----------------------------

print("=" * 80)
print("MISSING VALUES")
print("=" * 80)

print(df.isnull().sum())

# -----------------------------
# SHIP MODE ANALYSIS
# -----------------------------

print("=" * 80)
print("SHIP MODE ANALYSIS")
print("=" * 80)

ship_mode = (
    df.groupby("Ship Mode")
    .agg(
        Orders=("Order ID","count"),
        Avg_Lead=("Shipping Lead Time","mean"),
        Sales=("Sales","sum"),
        Profit=("Gross Profit","sum")
    )
)

print(ship_mode)

# -----------------------------
# REGION ANALYSIS
# -----------------------------

print("=" * 80)
print("REGION ANALYSIS")
print("=" * 80)

region = (
    df.groupby("Region")
    .agg(
        Orders=("Order ID","count"),
        Avg_Lead=("Shipping Lead Time","mean"),
        Sales=("Sales","sum"),
        Profit=("Gross Profit","sum")
    )
)

print(region)

# -----------------------------
# STATE ANALYSIS
# -----------------------------

print("=" * 80)
print("STATE ANALYSIS")
print("=" * 80)

state = (
    df.groupby("State/Province")
    .agg(
        Orders=("Order ID","count"),
        Avg_Lead=("Shipping Lead Time","mean"),
        Sales=("Sales","sum")
    )
)

print(state)

# -----------------------------
# FACTORY ANALYSIS
# -----------------------------

print("=" * 80)
print("FACTORY ANALYSIS")
print("=" * 80)

factory = (
    df.groupby("Factory")
    .agg(
        Orders=("Order ID","count"),
        Avg_Lead=("Shipping Lead Time","mean"),
        Sales=("Sales","sum"),
        Profit=("Gross Profit","sum"),
        Efficiency=("Efficiency Score","mean")
    )
)

print(factory)

# -----------------------------
# ROUTE ANALYSIS
# -----------------------------

print("=" * 80)
print("TOP 10 FASTEST ROUTES")
print("=" * 80)

routes = (
    df.groupby("Route")
    .agg(
        Shipments=("Order ID","count"),
        Avg_Lead=("Shipping Lead Time","mean"),
        Sales=("Sales","sum"),
        Profit=("Gross Profit","sum"),
        Efficiency=("Efficiency Score","mean")
    )
    .sort_values("Avg_Lead")
)

print(routes.head(10))

print("=" * 80)
print("BOTTOM 10 SLOWEST ROUTES")
print("=" * 80)

print(routes.tail(10))

# -----------------------------
# MONTHLY ANALYSIS
# -----------------------------

df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

monthly = (
    df.groupby("Month")
    .agg(
        Orders=("Order ID","count"),
        Sales=("Sales","sum"),
        Avg_Lead=("Shipping Lead Time","mean")
    )
)

print("=" * 80)
print("MONTHLY TREND")
print("=" * 80)

print(monthly)

# -----------------------------
# SAVE OUTPUTS
# -----------------------------

routes.to_csv("route_summary.csv")

factory.to_csv("factory_summary.csv")

region.to_csv("region_summary.csv")

state.to_csv("state_summary.csv")

ship_mode.to_csv("ship_mode_summary.csv")

monthly.to_csv("monthly_summary.csv")

print("=" * 80)
print("CSV FILES GENERATED SUCCESSFULLY")
print("=" * 80)

print("""
Generated Files:

✓ route_summary.csv
✓ factory_summary.csv
✓ region_summary.csv
✓ state_summary.csv
✓ ship_mode_summary.csv
✓ monthly_summary.csv
""")