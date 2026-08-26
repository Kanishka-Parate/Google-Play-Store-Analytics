import pandas as pd
import numpy as np

df = pd.read_csv("googleplaystore.csv")

df = df.drop_duplicates()
df = df.dropna(subset = ["Rating"])

df["Reviews"] = pd.to_numeric(
    df["Reviews"],
    errors = "coerce"
)

df["Installs"] = (
    df["Installs"]
    .astype(str)
    .str.replace(",", "", regex = False)
    .str.replace("+", "", regex = False)

)

df["Installs"] = pd.to_numeric(
    df["Installs"],
    errors = "coerce"
)

total_apps = df["App"].nunique()
total_installs = int(df["Installs"].sum())
avg_rating = round(df["Rating"].mean(), 2)
total_reviews = int(df["Reviews"].sum())

# print(total_apps)
# print(total_installs)
# print(avg_rating)
# print(total_reviews)


import json

kpi_data = {
    "total_apps": total_apps,
    "total_installs": total_installs,
    "avg_rating": avg_rating,
    "total_reviews": total_reviews
}

with open("kpi_data.json", "w") as file:
    json.dump(kpi_data, file)
