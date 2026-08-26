print("hello world")
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime 
import pytz

def show_Task1(): 

    df = pd.read_csv("googleplaystore.csv")
    print(df.head())
    print(df.info())
    print(df.isnull().sum())

    df = df.drop_duplicates() # removves duplicates rows
    df = df.dropna(subset=["Rating"])  # removes rows where rating is missing

    df["Reviews"] = pd.to_numeric(df["Reviews"], errors = "coerce")  # convert reviews into numbers

    df["Installs"] = (df["Installs"].str.replace(",","", regex = False).str.replace("+", "", regex = False)) # Remove commas and +

    df["Installs"] = pd.to_numeric(df["Installs"], errors = "coerce") # remove commas and +


    # convert size into MB
    def convert_size(size):
        if pd.isna(size):
            return np.nan
        if size == "Varies with device":
            return np.nan
        if "M" in size:
            return float(size.replace("M", ""))
        if "k" in size:
            return float(size.replace("k", ""))/1024
        
        return np.nan

    df["Size_MB"] = df["Size"].apply(convert_size)


    # Convert last updated
    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors = "coerce")
    df["Update_Month"] = df["Last Updated"].dt.month_name()


    # Applying filters
    filtered_df = df[(df["Rating"] >= 4.0) &
                    (df["Size_MB"] >=10) &
                    (df["Update_Month"] == "January")]

    # st.info("""
    # ### 🔍 Applied Filters
    # ⭐ Rating : **4.0 and above**
    # 📦 App Size : **10 MB and above**
    # 📅 Last Updated : **January**
    # """)


    # Calculate total installs for each company
    top_categories = (filtered_df.groupby("Category")["Installs"].sum()
                    .sort_values(ascending = False).head(10))

    print(top_categories)

    # keep only the top 10 catgories
    top10_df = filtered_df[filtered_df["Category"].isin(top_categories.index)]


    # create summary statistics
    summary = (top10_df.groupby("Category")
            .agg(
                Average_Rating = ("Rating", "mean"),
                Total_Reviews = ("Reviews", "sum")
            )
            .reset_index())

    print(summary)

    # Grouped bar chart


    import plotly.graph_objects as go
    fig = go.Figure()

        # average rating
    fig.add_trace(
        go.Bar(
        x = summary["Category"],
        y = summary["Average_Rating"],
        name = "Average Rating",
        text = summary["Average_Rating"].round(2),
        textposition = "outside",
        textfont = dict(size=18, color="white", family="Arial Black"),
        cliponaxis= False,
        marker = dict(
            color = "#38BDF8",
            line = dict(color = "white", width = 1)),
        hovertemplate = "<b>%{x}</b><br>"
        "Average Rating : %{y:.2f} ⭐<extra></extra>" ,   
        
        yaxis = "y",
        offsetgroup="rating"
    )
    
    )    

        # total reviews
    fig.add_trace(
        go.Bar(
        x = summary["Category"],
        y = summary["Total_Reviews"],
        name = "Total Reviews",
        text = summary["Total_Reviews"].apply(lambda x: f"{x/1_000_000:.1f}M" if x >= 1_000_000
                                              else f"{x/1_000:.1f}k" if x >= 1_000
                                              else f"{x:,.0f}"),
        textposition = "outside",
        textfont= dict(size=18, color="white", family="Arial Black"),
        cliponaxis= False,
        marker = dict(
            color = "#1D4ED8",
            line = dict(color = "black", width = 1)),
        hovertemplate =
        "<b>%{x}</b><br>"
        "Reviews : %{y:,.0f}<extra></extra>",  
        
        yaxis = "y2",
        offsetgroup="reviews"
        )
    )
    
    

    fig.update_layout(
        title = {
            "text" : "📊 Top 10 Categories by Installs<br><sup>Average Rating vs Total Reviews Analysis</sup>",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(
                 size=24,
                 color="white"
            )
            
            
        },
        xaxis = dict(
            title = "App Category",
            tickangle = -30
        ),    
        yaxis = dict( 
            title = "Average Reviews ⭐ ",
            range = [3.8,5],
            showgrid = True,
            gridcolor = "#2B2B2B"
        ),

        yaxis2 = dict(
            title = "Total Reviews",
            overlaying = "y",
            side = "right",
            showgrid = False
        ) ,

        barmode = "group",

        template = "plotly_dark",

        height = 850,
        # width = 1200,

        plot_bgcolor = "#121212",

        paper_bgcolor = "#121212",

        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1,
            xanchor = "center",
            x = 0.5,
            font = dict(size = 12, color = "white")
        ),

        margin = dict(
            l = 50,
            r = 50,
            t = 120,
            b= 60
        ),
        hoverlabel = dict(
            bgcolor = "#1B1B1B",
            bordercolor = "#2F80ED",
            font_size = 13,
            font_color = "white"
        ),
        bargap = 0.35,
        bargroupgap = 0.15
    )

    fig.update_xaxes(
         showline=True,
         linewidth=2,
         linecolor="#4FC3F7"
    )

    fig.update_yaxes(
         showline=True,
         linewidth=2,
         linecolor="#4FC3F7"
        #  secondary_y=False 
         
    )


    fig.update_traces(
        opacity = 0.9
    )

    # fig.show()

    from datetime import datetime
    import pytz

    

    ist = pytz.timezone("Asia/Kolkata")
    hour =  datetime.now(ist).hour

    

    if 15 <= hour < 17:
        st.plotly_chart(fig, use_container_width = True)
    else:
        st.info(
            "This visualization is available only between 3:00 PM and 5:00 PM IST."
        )  
    
    # if __name__=="__main__":
    #      print("Calling function")
    #      show_Task1()

    fig.write_html(
        "charts/Task1.html",
        full_html=False,
        include_plotlyjs = "cdn"
    )

    return fig

# if __name__=="__main__":
#          print("Calling function")
#          show_Task1()

    
    
