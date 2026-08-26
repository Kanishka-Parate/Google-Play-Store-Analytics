import streamlit as st

from Task1 import show_Task1
from Task2 import show_Task2
from Task3 import show_Task3
from Task4 import show_Task4
from Task5 import show_Task5
from Task6 import show_Task6

st.set_page_config(
    page_title = "Google Play Store Analytics Dashboard",
    page_icon = "📱",
    layout = "wide"
)

st.title("📱 Google Play Store Analytics Dashboard")

st.markdown("""
            Welcome to the **Google Play Store Analytics Dashboard**.
            
            This dashboard contains six analytical visualization created using
            the Google Play Store dataset as part of the internship project.
            
            Use the sidebar to navigate between different tasks.
            """)

st.divider()

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select a Task",
    [
        "🏠 Home",
        "📊 Complete Dashboard",
        "📊 Task 1",
        "🌍 Task 2",
        "📈 Task 3",
        "📉 Task 4",
        "🫧 Task 5",
        "📅 Task 6"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
🎓 Internship Project
Tools Used:
1) Python
2) Pandas
3) Plotly
4) Streamlit
                
Dataset:
Google Play Store Dataset
""")

# if page == "🏠 Home":

    # st.title("📱 Google Play Store Analytics Dashboard")

    # st.success(
    #     "🎓 Insternship Project | Python , Pandas, Plotly, Streamlit"
    # )

# st.markdown("""
# ###  📌 Project Overview
# This dashboard presents six analytical visualization created
# using the Google Play Store dataset.
            
# ### Dashboard Features

# 📊 Category- wise Install Analysis
            
# 🌍 Global Install Distribution
            
# 📈 Revenue and Install Trends
            
# 📉 Monthly Install Trends
            
# 💬 User Sentiment Analysis
            
# 🗓️ Cumulative Install Analysis
            
# Use the sidebar to navigate between different tasks
# """)

#  st.divider()
if page == "🏠 Home":
    
    st.success(
        "🎓 Insternship Project | Python , Pandas, Plotly, Streamlit"
    ) 
    
    st.markdown("""
###  📌 Project Overview
This dashboard presents six analytical visualization created
using the Google Play Store dataset.
            
### Dashboard Features

📊 Category- wise Install Analysis
            
🌍 Global Install Distribution
            
📈 Revenue and Install Trends
            
📉 Monthly Install Trends
            
💬 User Sentiment Analysis
            
🗓️ Cumulative Install Analysis
            
Use the sidebar to navigate between different tasks
""")
    
    st.divider()

    st.header("Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Visualization", "6")

    with col2:
        st.metric("Dataset", "Google Play Store")

    with col3:
        st.metric("Tool", "Streamlit + Plotly")

    st.info(
        "Select any task from the sidebar to view its visualization"
    )    

elif page == "📊 Complete Dashboard":
    st.title ("📊 Complete Google Play Store Dashboard")

    st.markdown("All six analytical visualizations in one dashboard")

    st.divider()
    show_Task1()  

    st.divider()
    show_Task2()

    st.divider()
    show_Task3()

    st.divider()
    show_Task4()

    st.divider()
    show_Task5()

    st.divider()
    show_Task6()

elif page == "📊 Task 1":
    st.header("Task 1")
    st.write("Task 1 visualization will appear here.")
    show_Task1()

elif page == "🌍 Task 2":
    st.header("Task 2")
    st.write("Task 2 visualization will appear here.")
    show_Task2()

elif page == "📈 Task 3":
    st.header("Task 3")
    st.write("Task 3 visualization will appear here.")
    show_Task3()

elif page == "📉 Task 4":
    st.header("Task 4")
    st.write("Task 4 visualization will appear here.")
    show_Task4()

elif page == "🫧 Task 5":
    st.header("Task 5")
    st.write("Task 5 visualization will appear here.")
    show_Task5()

elif page == "📅 Task 6":
    st.header("Task 6")
    st.write("Task 6 visualization will appear here.")
    show_Task6()                                