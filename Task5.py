import pandas as pd 
import plotly.express as px
import streamlit as st
from datetime import datetime
import pytz

def show_Task5():
    
    app_df = pd.read_csv("googleplaystore.csv")
    review_df = pd.read_csv("googleplaystore_user_reviews.csv")

    print(review_df.columns)

    app_df = app_df.drop_duplicates(subset = "App")

    app_df["Installs"] = (
        app_df["Installs"]
        .astype(str)
        .str.replace(",", "", regex = False)
        .str.replace("+", "", regex = False)
    )

    app_df["Installs"] = pd.to_numeric(app_df["Installs"], errors = "coerce")

    app_df["Rating"] = pd.to_numeric(app_df["Rating"], errors = "coerce")

    app_df["Reviews"] = pd.to_numeric(app_df["Reviews"], errors = "coerce")

    app_df["Size"] = app_df["Size"].astype(str)
    app_df["Size"] = app_df["Size"].apply(
             lambda x: float(x.replace("M", "")) if "M" in x
             else float(x.replace("k",""))/1024 if "k" in x
             else None
        )
     

    app_df["Size"] = pd.to_numeric(app_df["Size"], errors = "coerce")

    subjectivity_df = (
        review_df
        .groupby("App", as_index= False)["Sentiment_Subjectivity"]
        .mean()
    )

    merged_df = app_df.merge(
        subjectivity_df,
        on = "App",
        how = "left"
    )

    print(merged_df.columns)
    print(merged_df.head())

    required_categories = [
        "GAME",
        "BEAUTY",
        "BUSINESS",
        "COMICS",
        "COMMUNICATION",
        "DATING",
        "ENTERTAINMENT",
        "SOCIAL",
        "EVENTS"
    ]

    filtered_df = merged_df[
        (merged_df["Rating"] > 3.5) &
        (merged_df["Category"].isin(required_categories)) &
        (merged_df["Reviews"] > 500) &
        (merged_df["Installs"]> 50000) &
        (merged_df["Sentiment_Subjectivity"] > 0.5)
    ].copy()

    filtered_df = filtered_df[
        ~filtered_df["App"].str.contains("S", case = False, na = False)
    ]

    print(filtered_df.shape)

    print(filtered_df[
        ["App", "Category", "Rating", "Reviews", "Installs", "Sentiment_Subjectivity"]
    ].head())

    filtered_df["Category"] = filtered_df["Category"].replace({
        "BEAUTY": "सौंदर्य",
        "BUSINESS": "வணிகம்",
        "DATING": "Partnersuche"
    })

    print(filtered_df["Category"].unique())

    filtered_df["Color"] = filtered_df["Category"].apply(
        lambda x: "GAME" if x == "GAME" else "Other Categories"
    )

    print(filtered_df.shape)

    print(filtered_df[["Size", "Rating", "Installs"]].head())

    print(filtered_df["Size"].isna().sum())

    print(filtered_df["Size"].dtype)
    fig = px.scatter(
        filtered_df,
        x = "Size",
        y = "Rating",
        size = "Installs", 
        color = "Color",
        hover_name = "App",
        hover_data = {
            "Category": True,
            "Reviews": ":,",
            "Installs": ":,",
            "Size": ":.1f",
            "Rating": ":.1f"
        },
        color_discrete_map = {
            "GAME": "#F32d90",
            "Other Categories": "#1593E7"
        },
        size_max = 60,
        title = "📱 App Size vs Average Rating"
    )

    fig.update_layout(

        title = {
            "text": "📱 App Size vs Average Rating Analysis",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(
                size =  28,
                color = "#ffffff"
            )
        },

        template = "plotly_dark",

        # width = 1250,
        height = 850,

        paper_bgcolor = "#1e1e1e",
        plot_bgcolor = "#1e1e1e",

        xaxis_title = "<b> App Size (MB) </b>",

        yaxis_title = "<b>Average Rating</b>",

        font = dict(
            family = "Arial",
            size = 13,
            color = "white"
        ),

        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor  = "center",
            x = 0.5,
            title = "",
            bgcolor="rgba(0,0,0,0)"
        ),

        margin = dict(
            l = 50,
            r = 50,
            t = 80,
            b = 50
        )
    )

    fig.update_xaxes(
        showgrid = True,
        gridcolor = "#2e2e2e",
        showline = True,
        linewidth = 2,
        linecolor = "#4a4a4a"
    )

    fig.update_yaxes(
        showgrid = True,
        gridcolor = "#2e2e2e",
        showline = True,
        linewidth = 2,
        linecolor = "#4a4a4a"
    )

    fig.update_traces(
        marker = dict(
            opacity = 0.60,
            
            line = dict(
                width = 1,
                color = "white"
            )
        )
    )


    ist = pytz.timezone("Asia/Kolkata")
    hour = datetime.now(ist).hour

    if 17<= hour < 19:
        st.plotly_chart(fig, use_container_width=True)   
    else:
        print("This visualization is available only between 5:00 PM and 7:00 PM IST")    

    

    fig.write_html(
        "charts/Task5.html",
        full_html=False,
        include_plotlyjs = "cdn")
    
    return fig



