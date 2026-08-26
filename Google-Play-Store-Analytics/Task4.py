import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from  datetime import datetime
import pytz

def show_Task4():

    df = pd.read_csv("googleplaystore.csv")

    df["Reviews"] = pd.to_numeric(df["Reviews"], errors = "coerce")

    df["Installs"] = (
        df["Installs"]
        .astype(str)
        .str.replace(",", "", regex = False)
        .str.replace("+", "", regex = False)
    )

    df["Installs"] = pd.to_numeric(df["Installs"], errors = "coerce")

    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors = "coerce")

    filtered_df = df[df["Reviews"] > 500].copy()

    filtered_df = filtered_df[
        ~filtered_df["App"].str.upper().str.startswith(("X", "Y", "Z"), na = False)
    ]

    filtered_df = filtered_df[
        filtered_df["Category"].str.upper().str.startswith(("E", "C", "B"), na = False)
    ]

    filtered_df = filtered_df[
        ~filtered_df["App"].str.upper().str.contains("S", na = False)
    ]

    filtered_df = filtered_df.dropna(subset = ["Last Updated"])

    print(filtered_df.shape)
    print(filtered_df.head())


    filtered_df["Month"] = filtered_df["Last Updated"].dt.to_period("M").astype(str)

    # top_categories = (
    #     filtered_df.groupby("Category")["Installs"]
    #     .sum()
    #     .nlargest(5)
    #     .index
    # )

    # filtered_df = filtered_df[
    #     filtered_df["Category"].isin(top_categories)
    # ]

    trend_df = (
        filtered_df.groupby(["Month", "Category"], as_index = False)["Installs"]
        .sum()
    )

    trend_df = trend_df.sort_values(["Category", "Month"])

    trend_df["MoM_Growth"] = (
        trend_df.groupby("Category")["Installs"]
        .pct_change()
    )

    print(trend_df.head())
    print(trend_df.tail())

    translation = {
        "BEAUTY" : "सौंदर्य",
        "BUSINESS" : "வணிகம்",
        "DATING" : "Dating"
    }

    trend_df["Category"] = trend_df["Category"].str.upper().replace(translation)

    trend_df["Category"] = trend_df["Category"].replace({
        "DATING": "Partnersuche"
    })

    colors = {
        "GAME": "#00E5FF",
        "COMMUNICATION": "#2F80ED",
        "TOOLS": "#7C3AED",
        "PRODUCTIVITY": "#00C896",
        "SOCIAL": "#F59E0B"
    }

    fig = go.Figure()
    for category in trend_df["Category"].unique():

        temp = trend_df[trend_df["Category"] == category]

        fig.add_trace(
            go.Scatter(
                x = temp["Month"],
                y = temp["Installs"],
                mode = "lines+markers",
                name = category,
                line = dict(width = 3, 
                            color = colors.get(category, "#2F80ED"),
                            shape ="spline",
                            smoothing = 0.6),
                marker = dict(size = 9,
                            color = colors.get(category, "#2F80ED"),
                            line = dict(color = "white", width = 2)),
                hovertemplate = "<b>%{fullData.name}</b><br>"+
                "Month: %{x}<br>"+
                "Installs: %{y:,}<extra></extra>"              
                
            )
        )

        growth = temp[temp["MoM_Growth"] > 0.20]

        if not growth.empty:
            fig.add_trace(
                go.Scatter(
                    x = growth["Month"],
                    y = growth["Installs"],
                    mode = "lines",
                    line = dict(
                         color=colors.get(category, "#2F80ED"),
                         width=0
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(255, 77, 109, 0.18)",
                    name=">20% Growth",
                    showlegend=False,
                    hovertemplate=
                         "<b>%{x}</b><br>"+
                         "Installs: %{y:,}<br>"+
                         "Growth >20%<extra></extra>"
                    
                )

    

                
                
                
                    

                # name = ">20% Growth",
                # showlegend = False,
                # hovertemplate = 
                # "<b>%{x}</b><br>" +
                # "Installs : %{y:,}<br>" +
                # "Growth >20%<extra></extra>"
            )
                   
    
            
            

    fig.update_layout(
        title = {
            "text" : "📈 Monthly Install Trends by App Category",
            "x" : 0.5,
            "xanchor" : "center",
            "font" : dict(size = 24, color = "White")
        },

        template = "plotly_dark",
        height = 850,
        # width = 1300,
        hovermode = "x unified",

        xaxis_title = "Month",

        yaxis_title = "Total Installs",

        legend = dict(
            orientation = "h",
            y = -0.25,
            x = 0.5,
            xanchor = "center",
            title = ""
        ),

        font = dict(size = 14), 

        margin= dict(l = 50, r = 50, t = 80, b = 120)
    ),

    font = dict(
        family = "Arial",
        size = 13,
        color = "#2C3E50"
    )

    fig.update_xaxes(
        title = "Month",
        showline = True,
        linewidth = 2,
        linecolor = "#4FC3F7",
        tickangle = -30,
        showgrid = False
    )

    fig.update_yaxes(
        title = "Total Installs",
        showgrid = True,
        gridcolor = "#2e2e2e",
        zeroline = False,
        tickformat = ",.0f"
    )

    fig.update_traces(
         hoverlabel = dict(
              bgcolor="#1B1B1B",
              bordercolor="#2F80ED",
              font=dict(
                   color="white",
                   size =13
              )
         )
    )

    from datetime import datetime 
    import pytz


    ist = pytz.timezone("Asia/Kolkata")
    hour = datetime.now(ist).hour

    if 18 <= hour < 21:
        st.plotly_chart(fig, use_container_width = True)
    else:
        st.info("This visualization is available only between 6:00 PM and 9:00 PM IST")    

    fig.write_html(
        "charts/Task4.html",
        full_html=False,
        include_plotlyjs = "cdn")
    
    return fig



