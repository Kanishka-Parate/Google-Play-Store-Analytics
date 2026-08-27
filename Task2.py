import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
import pytz


def show_Task2(): 

    country_df = pd.read_csv("countries of the world.csv")
    print(country_df.columns)

    iso_df = pd.read_csv("wikipedia-iso-country-codes.csv")
    print(iso_df.columns)

    app_df = pd.read_csv("googleplaystore.csv")
    country_df = pd.read_csv("countries of the world.csv")
    iso_df = pd.read_csv("wikipedia-iso-country-codes.csv")
    country_stats = pd.read_csv("app_country_stats.csv")

    print(country_df.columns)
    print(iso_df.columns)
    print(country_stats.columns)

    app_df["Installs"] = (
        app_df["Installs"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
    )

    app_df["Installs"] = pd.to_numeric(
        app_df["Installs"],
        errors="coerce"
    )

    print(app_df["Installs"].head())
    print(app_df["Installs"].dtype)

    filtered_df = app_df[
        app_df["Installs"] > 1000000
    ].copy()

    filtered_df["Category"] = (
        filtered_df["Category"]
        .astype(str)
        .str.strip()
    )

    filtered_df = filtered_df[
        ~filtered_df["Category"]
        .str.upper()
        .str.startswith(
            ("A", "C", "G", "S"),
            na=False
        )
    ]

    top5_categories = (
        filtered_df
        .groupby("Category", as_index=False)["Installs"]
        .sum()
        .sort_values(
            by="Installs",
            ascending=False
        )
        .head(5)
    )

    print("Top 5 Categories:")
    print(top5_categories)

    country_stats["min_installs"] = pd.to_numeric(
        country_stats["min_installs"],
        errors="coerce"
    )

    country_stats["country"] = (
        country_stats["country"]
        .astype(str)
        .str.strip()
    )

    country_stats["category"] = (
        country_stats["category"]
        .astype(str)
        .str.strip()
    )

    map_df = country_stats[
        country_stats["category"].isin(
            top5_categories["Category"]
        )
    ].copy()

    map_df = map_df[
        map_df["min_installs"] > 1000000
    ].copy()

    map_df["Country"] = (
        map_df["country"]
        .str.title()
    )

    map_df["Category"] = map_df["category"]
    map_df["Installs"] = map_df["min_installs"]

    map_df["Installs (Millions)"] = (
        map_df["Installs"] / 1000000
    ).round(2)

    print("Final Map Data:")
    print(map_df.head())

    fig = px.choropleth(
        map_df,
        locations="Country",
        locationmode = "country names",
        color = "Installs",
        hover_name = "Country",
        hover_data = {
            "Category": True,
            "Installs": ":,",
            "Installs (Millions)": " : .2f"
        },
        color_continuous_scale = [
             "#0B1F33",
             "#103D60",
             "#1E5F9A",
             "#2F80ED",
             "#64B5F6"
        ],
        projection = "natural earth"
        
    )

    fig.update_layout(

        title = dict(
            text = "🌍 Global Installs by Top 5 App Categories",
            x = 0.5,
            font = dict(size = 26, color = "white"),
            xanchor = "center"
    ),
        template="plotly_dark",

        paper_bgcolor = "#121212",
        plot_bgcolor = "#121212",

        font=dict(
             color="white",
             family="Arial"
        ),

        # width = 1200,
        height = 850,


          
        legend=dict(
             orientation="h",
             yanchor="bottom",

             y=1.02,
             xanchor="center",
             x=0.5,
             bgcolor="rgba(0,0,0,0)"
        ),  
        margin = dict(l=40, r=40, t=80, b=40),

        coloraxis_colorbar=dict(
            title="Installs",
            thickness=18,
            len=0.70
        )
    )


    fig.update_geos(
            bgcolor = "#121212",
            showframe = False,
            showcoastlines = True,
            coastlinecolor = "#5f6368",
            coastlinewidth = 1.3,
            showcountries = True,
            countrycolor = "#6a6a6a",
            showland = True,
            landcolor = "#161616",
            showocean = True,
            oceancolor = "#071c33",
            showlakes = True,
            lakecolor = "#0A192F",
            projection_type = "natural earth",
            countrywidth = 1,
            fitbounds = False,
            projection_scale=1.0,
            center = dict(lat=15, lon=0)
    
            
    )
    
    fig.update_traces(
         hoverlabel=dict(
              bgcolor="#202020",
              bordercolor="#2F80ED",

              font=dict(
                   color="white",
                   size=14
              )
         )
    )

    

    

    

    country_stats["min_installs"] = pd.to_numeric(
        country_stats["min_installs"],
        errors = "coerce"
    )

    country_stats["country"] = country_stats["country"].str.lower().str.strip()

    

    
    
    from datetime import datetime
    import pytz

    ist = pytz.timezone("Asia/kolkata")
    hour = datetime.now(ist).hour

    if 18 <= hour < 20:
        st.plotly_chart(fig, use_container_width = True)
        
    else:
        st.info("⏰ This visualization is available only between 6:00 PM and 8:00 PM IST.") 

    fig.write_html(
        "charts/Task2.html",
        full_html=False,
        include_plotlyjs = "cdn")
    
    return fig






