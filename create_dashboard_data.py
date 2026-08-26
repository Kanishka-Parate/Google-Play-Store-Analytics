import pandas as pd
import json

df = pd.read_csv("googleplaystore.csv")

df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

df["Installs"] = (
    df["Installs"]
    .astype(str)
    .str.replace(",","", regex=False)
    .str.replace("+","", regex=False)
)

df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

df["Last Updated"] = pd.to_datetime(
    df["Last Updated"],
    errors = "coerce"
)

df["Month"] = df["Last Updated"].dt.month_name()

data = []

for _, row in df.iterrows():

    data.append({
        "category": row["Category"],
        "month": row["Month"],
        "rating": None if pd.isna (row["Rating"]) else row["Rating"],
        "reviews": None if pd.isna(row["Reviews"]) else row["Reviews"],
        "installs": None if pd.isna(row["Installs"]) else row["Installs"]
    })

with open("dashboard_data.json", "w") as file:
    json.dump(data,file, indent=4)

print("dashboard_data.json created successfully!")        