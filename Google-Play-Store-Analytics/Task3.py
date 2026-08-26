import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def show_Task3():

    df = pd.read_csv("googleplaystore.csv")

    df["Installs"] = (
        df["Installs"]
        .astype(str)
        .str.replace(",", "", regex = False)
        .str.replace("+", "", regex = False)

    ) 

    df["Installs"] = pd.to_numeric(df["Installs"], errors = "coerce")

    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace("$", "", regex = False)
    )

    df["Price"] = pd.to_numeric(df["Price"], errors = "coerce")

    df["Size"] = df["Size"].astype(str)

    df = df[df["Size"].str.contains("M", na = False)]

    df["Size"] = (
        df["Size"]
        .str.replace("M", "", regex = False)
    )
    df["Size"] = pd.to_numeric(df["Size"], errors = "coerce")

    df["Revenue"] = df["Installs"] * df["Price"]

    filtered_df = df[
        (df["Installs"] > 10000) &
        (df["Revenue"] > 10000) &
        (df["Size"] > 15) &
        (df["Content Rating"] == "Everyone")
    ].copy()

    filtered_df["Android Ver"] = (
        filtered_df["Android Ver"]
        .astype(str)
        .str.extract(r'(\d+\.\d+)')
    )

    filtered_df["Android Ver"] = pd.to_numeric(
        filtered_df["Android Ver"],
        errors = "coerce"
    )

    filtered_df = filtered_df[
        filtered_df["Android Ver"] > 4.0
    ]

    filtered_df = filtered_df[
        filtered_df["App"].str.len() <=30
    ]

    top3_categories = (
        filtered_df.groupby("Category")["Installs"]
        .mean()
        .sort_values(ascending = False)
        .head(3)
        .index
    )

    filtered_df = filtered_df[
        filtered_df["Category"].isin(top3_categories)
    ]

    print(filtered_df.head())
    print(filtered_df["Category"].unique())

    chart_df = (
        filtered_df.groupby("Category", as_index = False)
        .agg({
            "Installs": "mean",
            "Revenue": "sum"
        })
    )

    print(chart_df)

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(specs=[[{"secondary_y" : True}]])

    fig.add_trace(
        go.Bar(
            x = chart_df["Category"],
            y = chart_df["Installs"],
            name = "Average Installs",
            marker = dict(
                color = "#2F80ED",
                line = dict(color = "#4FC3F7", width = 2)
            ),
            opacity=0.90
        ),
        secondary_y = False
    )

    fig.add_trace(
        go.Scatter(
            x = chart_df["Category"],
            y = chart_df["Revenue"],
            name = "Revenue",
            mode = "lines+markers",
            line = dict
            (color = "#00E5FF", 
            width = 4,
            shape = "spline",
            smoothing = 0.6 ),
            marker = dict(
                size = 10,
                color = "#00E5FF",
                line = dict(color = "white", width = 2)
            )
        ),
        secondary_y= True
    )
            
        
        

    fig.update_layout(
        title = {
            "text" : "📈 Average Installs & Estimated Revenue<br>"
            " Across Top 3 App Categories ",
            "x" : 0.5,
            "xanchor" : "center",
            "font" : dict(
                family = "Arial",
                size = 24,
                color = "white"
            ),
            

        },

        template = "plotly_dark",

        # width = 1350,
        height = 850,

        paper_bgcolor = "#1E1E1E",
        plot_bgcolor = "#1E1E1E",

        barmode = "group",

        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1,
            xanchor = "center",
            x = 0.5,
            bgcolor="rgba(0,0,0,0)",
            font = dict(size = 13)
        ),

        margin = dict(
            l = 60,
            r = 60,
            t = 90,
            b = 60
        ),
        hovermode = "x unified"

    )


    fig.update_xaxes(
        title_text = "App Categories",
        tickangle = -15,
        showgrid = False,
        showline = True,
        linewidth = 2,
        linecolor = "#4FC3F7",

        tickfont = dict(
             color="white",
             size=12
        ),

        title_font=dict(
             color="white",
             size=14
        )
    )

    fig.update_yaxes(
        title_text = "Average Installs",
        secondary_y = False,
        showgrid = True,
        gridcolor = "#2b2b2b",
        showline = True,
        linewidth = 2,
        linecolor = "#4FC3F7",

        tickfont=dict(
             color="white",
             size=12
        ),
        title_font = dict(
             color="white",
             size = 14
        ),

        zeroline = False,
        tickformat = ",.0f"

    )

    fig.update_yaxes(
        title_text = "Revenue ($)",
        secondary_y = True,
        showgrid = False,
        showline = True,
        linewidth = 2,
        linecolor="#4FC3F7",

        tickfont = dict(
             color ="white",
             size=12
        ),

        title_font=dict(
             color="white",
             size=14
        ),

        zeroline = False,
        tickprefix = "$",
        tickformat = ",.0f"
    )



    fig.update_traces(
        hovertemplate = "<br>%{x}</b><br>%{fullData.name}: %{y:,.0f}<extra></extra>",

        hoverlabel = dict(
             bgcolor="#1b1b1b",
             bordercolor="#2f80ed",
             font=dict(
                  color="white",
                  size=13
             )
        )
    )
    fig.show()

    from datetime import datetime
    import pytz

    ist = pytz.timezone("Asia/Kolkata")
    hour = datetime.now(ist).hour

    if 13 <= hour < 14:
         st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
             "This visualization is available only between 1:00 PM and 2:00 PM IST"
        )     
        
        

    fig.write_html(
        "charts/Task3.html",
        full_html=False,
        include_plotlyjs = "cdn")  
    
    return fig


