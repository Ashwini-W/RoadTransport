
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

import analysis2
import analysis3
import revenueGenerated
# import budget_analysis


st.set_page_config(layout="wide", page_title='PUBLIC TRANSIT')

st.title("ROAD PUBLIC TRANSIT")

# st.markdown('# Data Sources')
# st.markdown('''
# 1. **Transport** - The air quality data is taken from [data.gov.in](https://data.gov.in/). The data is collected using their
#             live API and is updated every hour.
# 2. **Tax Revenue Data** - The historical data is taken from [data.gov.in](https://data.gov.in/). The data is collected in various
#             files and then compiled into a single dataset for analysis.
# 3. **Road lengths Data** - The health data is taken from [data.gov.in](https://data.gov.in/). Which was then cleaned and processed to
#             make it usable for analysis.            
# ''')


with st.sidebar:
    selected = option_menu(
    menu_title = "",
    options=[ "State transport","Freight vs Passenger","Revenue"],
    icons=["house", "info-circle", "info-circle","info-circle"],
    menu_icon="cast",
    default_index = 0,
)

# if selected == "Vehicles trends in states ":
#     st.title(f"The  {selected}")
#     #st.image("constants/MentalHealthImage.jpg", caption="")
#     StateVehicles.show_analysis3_page()


if selected == "State transport":
    analysis3.show_analysis3_page()

elif selected == "Freight vs Passenger":
    analysis2.show_analysis2_page()


elif selected == "Revenue":
    revenueGenerated.show_analysis_page()