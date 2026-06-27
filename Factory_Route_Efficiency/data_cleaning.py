import pandas as pd

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("Nassau Candy Distributor.csv")

# -----------------------------
# Convert Dates
# -----------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# -----------------------------
# Shipping Lead Time
# -----------------------------
df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# Remove invalid lead times
df = df[df["Shipping Lead Time"] >= 0]

# -----------------------------
# Remove Missing Values
# -----------------------------
df = df.dropna(subset=["Ship Date"])

# -----------------------------
# Standardize Text Columns
# -----------------------------
cols = [
    "Ship Mode",
    "Country/Region",
    "City",
    "State/Province",
    "Division",
    "Region",
    "Product Name"
]

for col in cols:
    df[col] = df[col].astype(str).str.strip()

# -----------------------------
# Factory Mapping
# -----------------------------
factory_map = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

df["Factory"] = df["Product Name"].map(factory_map)

# -----------------------------
# Factory Coordinates
# -----------------------------
factory_coords = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.119140, -96.181150),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.117500, -89.971107)
}

df["Factory Latitude"] = df["Factory"].map(
    lambda x: factory_coords.get(x, (None, None))[0]
)

df["Factory Longitude"] = df["Factory"].map(
    lambda x: factory_coords.get(x, (None, None))[1]
)

# -----------------------------
# Route Definition
# -----------------------------
df["Route"] = (
    df["Factory"] +
    " → " +
    df["State/Province"]
)

# -----------------------------
# Delay Flag
# -----------------------------
THRESHOLD = 5

df["Delayed"] = df["Shipping Lead Time"] > THRESHOLD

# -----------------------------
# Route Efficiency Score
# -----------------------------
max_days = df["Shipping Lead Time"].max()

df["Efficiency Score"] = (
    100 - (
        df["Shipping Lead Time"] / max_days
    ) * 100
).round(2)

# -----------------------------
# Save Cleaned Dataset
# -----------------------------
df.to_csv("cleaned_dataset.csv", index=False)

print(df.head())

print("\nDataset Shape:", df.shape)

print("\nCleaning Completed Successfully!")