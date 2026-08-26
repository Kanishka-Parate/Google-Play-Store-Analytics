import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
import pytz
import re

def show_Task6():
    
    df = pd.read_csv("googleplaystore.csv")
    print(df.columns)

    df["Rating"] = pd.to_numeric(df["Rating"], errors = "coerce")

    df["Reviews"] = pd.to_numeric(df["Reviews"], errors = "coerce")

    df["Size"] = df["Size"].astype(str)
    df["Size"] = df["Size"].apply(
           lambda x: float(x.replace("M", "")) if "M" in x
           else float(x.replace("K", ""))/ 1024 if "K" in x
           else None)
    df["Size"].between(20,80)
    

    df["Size"] = pd.to_numeric(df["Size"], errors = "coerce")

    df["Installs"] = (
        df["Installs"]
        .astype(str)
        .str.replace(",", "", regex = False)
        .str.replace("+", "", regex = False)

    )

    df["Installs"]  = pd.to_numeric(df["Installs"], errors = "coerce")

    print(df[["Rating", "Reviews", "Size", "Installs"]].dtypes)

    filtered_df = df[
        (df["Rating"] >= 4.2) &
        (df["Reviews"] > 1000) &
        (df["Size"].between(20,80)) &
        (df["Category"].str.startswith(("T", "P"), na = False)) &
        (~df["App"].str.contains(r"\d", regex = True, na = False))
    ].copy()

    print(filtered_df.shape)

    print(filtered_df[["App", "Category", "Rating", "Reviews", "Size"]].head())

    print("Rating >=4.2 :", df[df["Rating"] >=4.2].shape)
    print("Reviews > 1000 :", df[df["Reviews"] > 1000].shape)
    print("Size between 20 and 80 :",
        df[df["Size"].between(20,80)].shape)
    print("Category starts with T or P :",
        df[df["Category"].str.startswith(("T", "P"), na = False)].shape)
    print("App without numbers : ", 
        df[~df["App"].str.contains(r"\d",regex = True, na = False)].shape)


    print(df["Reviews"].head(10))
    print(df["Reviews"].dtype)
    print(df["Reviews"].max())

    df["Last Updated"] = pd.to_datetime(
        df["Last Updated"],
        errors = "coerce"
    )

    filtered_df["Last Updated"] = pd.to_datetime(
        filtered_df["Last Updated"],
        errors = "coerce"
    )

    filtered_df["Month"] = filtered_df["Last Updated"].dt.month_name()

    month_order = [
        "January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December"
    ] 

    filtered_df["Month"] = pd.Categorical(
        filtered_df["Month"],
        categories= month_order,
        ordered = True
    )

    print(filtered_df["Category"].unique())

    print(filtered_df[["Last Updated", "Month"]].head())

    filtered_df["Category"] = filtered_df["Category"].replace({
        "TRAVEL_AND_LOCAL" : "Voyage et Local",
        "PRODUCTIVITY": "Productividad",
        "PHOTOGRAPHY" : "写真"
    })

    print(filtered_df["Category"].unique())

    area_df = (
        filtered_df
        .groupby(["Category", "Month"], as_index = False)["Installs"]
        .sum()
    )

    area_df = area_df.sort_values(
        by = ["Category", "Month"],
        key = lambda x: x.cat.codes if str(x.dtype) == "category" else x
    )

    all_months = filtered_df["Month"].cat.categories

    area_df = (
        area_df
        .set_index(["Category", "Month"])
        .unstack(fill_value = 0)
        .stack(future_stack = True)
        .reset_index()
    )

    area_df.columns = ["Category", "Month", "Installs"]

    print(area_df.head())


    area_df["Month"] = pd.Categorical(
        area_df["Month"],
        categories=month_order,
        ordered = True
    )

    area_df = area_df.sort_values(["Category", "Month"])

    area_df["Cumulative_Installs"] = (
        area_df
        .groupby("Category")["Installs"]
        .cumsum()
    )

    area_df["MoM_Growth"] = (
           area_df.groupby("Category")["Installs"].pct_change()
    )

    fig = px.area(
        area_df,
        x = "Month",
        y = "Cumulative_Installs",
        color = "Category",
        # title = "📈 Monthly Cumulative Installs by Category",
        category_orders={
            "Month": month_order
        },
        color_discrete_sequence = [
            "#7DD3FC",
            "#38BDF8",
            "#0EA5E9",
            "#0284C7",
            "#0369A1",
            "#075985"
        ]
    )

    growth_df = area_df[area_df["MoM_Growth"] > 0.25]

    fig.add_scatter(
           x = growth_df["Month"],
           y = growth_df["Cumulative_Installs"],
           mode="markers",
           marker= dict(
                  size = 12,
                  color = "#FFFFFF",
                  line = dict(
                         color = "#FF4D6D",
                         width = 3
                  )
           ),
           name = ">25% Growth",
           hovertemplate=
           "<b>%{x}</b><br>" +
           "Cumulative Installs: %{y:,}<br>" +
           "Growth >25%<extra></extra>"
    )

    print(area_df.head(20))

    print(
        area_df.groupby("Category")["Cumulative_Installs"].max()
    )

    fig.update_traces(
           opacity = 0.75,
           line=dict(width = 3))
    
    fig.update_layout(
           template="plotly_dark",

           paper_bgcolor="#121212",
           plot_bgcolor="#121212",

           height=850,

           title={
                  "text": "📈 Monthly Cumulative Installs by Category",
                  "x": 0.5,
                  "font": dict(
                         size = 28,
                         color="#ffffff"
                  )
           },

           font=dict(
                  family="Arial",
                  size=13,
                  color ="white"
           ),

           legend=dict(
                  orientation ="h",
                  yanchor="bottom",
                  y=0.99,
                  xanchor="center",
                  x=0.5,
                  font=dict(
                         color="white",
                         size=12
                  ),
                  bgcolor="rgba(0,0,0,0)"
           ),

           margin=dict(
                  l=50,
                  r=50,
                  t=90,
                  b=50
           ),

           hoverlabel=dict(
                  bgcolor="#1B1B1B",
                  bordercolor="#2F80ED",
                  font_size=13,
                  font_color="white"
           )
    )

    fig.update_xaxes(
           showgrid=True,
           gridcolor="#2B2B2B",
           showline=True,
           linewidth=2,
           linecolor="#4FC3F7"
    )

    fig.update_yaxes(
           showgrid = True,
           gridcolor="#2B2B2B",
           showline=True,
           linewidth=2,
           linecolor="#4FC3F7"
    )



    # fig.show()

    from datetime import datetime 
    import pytz

    ist = pytz.timezone("Asia/Kolkata")
    hour = datetime.now(ist).hour

    if 16 <= hour < 18:
           st.plotly_chart(fig, use_container_width = True)

    else:
           st.info(
                  "This visualization is available only between 4:00 PM and 6:00 PM IST"
           )       

    fig.write_html(
        "charts/Task6.html",
        full_html=False,
        include_plotlyjs = "cdn")
    
    return fig



