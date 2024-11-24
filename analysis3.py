
import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objs as go

import plotly.express as px
import geopandas as gpd

# st.set_page_config(layout="wide")

@st.cache
def load_data(): 

    df = pd.read_csv("dataset/TotalregisteredTransportVehicle2018to19.csv")
    print(df.head())    
    return df



def generate_road_construction_conclusions(state, dominant_vehicle_type, total_vehicles):
    conclusions = []


    # Bulky Heavy-Duty Roads and Highways
    if dominant_vehicle_type in ["Multiaxled/Articulated Vehicles (I)", "Trucks and Lorries (II)"]:
        conclusions.append(
            f"Since {state} has a high concentration of {dominant_vehicle_type}, "
            "it requires high-quality concrete roads designed for heavy loads. "
            "Regular maintenance schedules should also be implemented to prevent wear and tear."
        )
        conclusions.append(
            f"To accommodate the high bulky/loaded vehicles movement in {state}, Dedicated Freight Corridors (a high speed and high capacity corridor that is exclusively meant for loaded vehicles and not for passenger vehicles) "
            "should be developed. These can reduce congestion and traffic on public roads and have safety for other passenger vehicles."
        )
        conclusions.append(
            f"Rest areas with large parking lots and driver amenities (e.g., restrooms, eateries) "
            f"should be established along major highways in {state} to support truck drivers."
        )
        conclusions.append(
            f"High truck activity in {state} may cause congestion for passenger vehicles. "
            "Dedicated bus lanes and expanded metro/rail connectivity should be prioritized to improve public transit."
        )
        conclusions.append(
            f"To manage the traffic created by {dominant_vehicle_type} in {state}, advanced traffic management systems "
            "like intelligent signals and weigh-in-motion sensors should be implemented."
        )
        conclusions.append(
            f"With the high number of {dominant_vehicle_type} in {state}, alternative fuels like CNG or electric trucks "
            "should be promoted, along with strict emission checks to reduce pollution."
        )
        conclusions.append(
            f"Improved road connectivity to industrial hubs in {state} is essential. Ring roads and access roads "
            "should connect warehouses, ports, and airports to support bulky vehicles movement."
        )


    #Light private 3 4 Urban Road Network Expansion
    if dominant_vehicle_type in ["Light Motor Vehicles (Passengers) (VI) - Three Seaters","Light Motor Vehicles (Passengers) (VI) - Four to six seaters",
    "Taxis (V) - Motor cabs","Taxis (V) - Maxi cabs", "Taxis (V) - Other taxis"]:
        conclusions.append(
            f"In {state}, the high number of {dominant_vehicle_type} indicates a need for expanding urban road networks. "
            "Focus should be on creating well-maintained city roads and suburban links to handle frequent passenger transit."
        )
        conclusions.append(
            f"To manage the large number of {dominant_vehicle_type} in {state}, dedicated lanes for three-seaters and four-seaters public taxis"
            "can reduce congestion and ensure smoother traffic flow."
        )
        conclusions.append(
            f"Passenger vehicles like {dominant_vehicle_type} often require designated pickup/drop-off points in busy areas. "
            f"Constructing waiting areas in {state} can enhance passenger convenience."
        )
        conclusions.append(
            f"The huge count of {dominant_vehicle_type} in {state} suggests strong public transit demand. "
            "Integrating three-seater and four-seater services with metro, buses, and rail systems can improve connectivity."
        )
        conclusions.append(
            f"To prevent road blockages caused by idle {dominant_vehicle_type}, dedicated parking zones and "
            "better traffic management systems should be implemented in {state}."
        )
        conclusions.append(
            f"Since {dominant_vehicle_type} is widely used in {state}, promoting eco-friendly alternatives like "
            "electric/V,CNG three-seaters four-seaters can reduce emissions and enhance sustainability."
        )

    return conclusions


def show_analysis3_page():

    st.title("")
    st.image("constants/Road-Transport.png", caption="")

    df = load_data()
    df = load_data()
    st.markdown("""
    The dataset contains information on road transport registered vehicles, with the columns such as Year and various other  mode of road vehicle types.
    """)
    st.dataframe(df) 




    if 'Year' in df.columns:
        years = df['Year'].unique()
    else:
        st.error("The dataset must contain a 'Year' column.")
        st.stop()

    vehicle_types = [col for col in df.columns if col not in ['Year', 'States/Union Territories']]

    # Streamlit inputs
    selected_year = st.radio("Select Year", years)
    selected_vehicle_types = st.multiselect(
        "Select Vehicle Transport Types",
        vehicle_types,
        default=vehicle_types[:2] 
    )
    filtered_data = df[df['Year'] == selected_year]

    if selected_vehicle_types:
        st.subheader(f"Compare the Transport Vehicles in {selected_year}")
        
        fig = go.Figure()
        
        for vehicle_type in selected_vehicle_types:
            if vehicle_type in filtered_data.columns:
                fig.add_trace(go.Scatter(
                    x=filtered_data['States/Union Territories'],
                    y=filtered_data[vehicle_type],
                    mode='lines+markers',
                    name=vehicle_type
                ))
            else:
                st.warning(f"{vehicle_type} not found in data.")

        fig.update_layout(
            title=f"Transport Vehicles in {selected_year}",
            xaxis_title="State",
            yaxis_title="Number of Vehicles",
            xaxis=dict(tickmode='linear', tickangle=45, title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            legend=dict(font=dict(size=12)),
            margin=dict(l=40, r=40, t=40, b=80),
            height=600,
            width=1200,
            
            
        )

        st.plotly_chart(fig, use_container_width=True)


        

    if not filtered_data.empty:
        st.subheader("Conclusion")
        st.write(f"For the year {selected_year} :")
        for vehicle_type in selected_vehicle_types:
            if vehicle_type in filtered_data.columns:
                max_value = filtered_data[vehicle_type].max()
                max_state = filtered_data.loc[filtered_data[vehicle_type].idxmax(), 'States/Union Territories']
                st.write(f"- The state with the highest number of {vehicle_type} is **{max_state}** with **{max_value} vehicles**.")
        total_counts = filtered_data[selected_vehicle_types].sum().sort_values(ascending=False)
        
        # cola,colb= st.columns(2)
        # # cola.metric("ABCCC ", "A+", "okkk", 'normal', help='ABC')
        # cola.metric("Total Sales", "₹200,000", "10% increase")
        # colb.metric("Revenue", "₹500,000", "5% decrease",'inverse')

    else:
        st.info("Please select at least one vehicle transport type.")


#--------------------------------------------   GEOSPATIAL choropleth and BAR GRAPH ---------------------------

    st.subheader(f"State wise distribution of the transport vehicles")
    geojson_path = "dataset/gadm41_IND_1.json"
    india_states = gpd.read_file(geojson_path)


    print(india_states['NAME_1'].unique())
    #st.write(india_states['NAME_1'].unique())

 

    c1, c2 = st.columns(2)
    with c1:
        selected_year = st.selectbox("Select the Year", df['Year'].unique())

    with c2:
        selected_vehicle_type = st.selectbox(
                "Select the Vehicle Transport type",
                [col for col in df.columns if col not in ['Year', 'States/Union Territories']]
            )


    state_to_id_map = {
    "Andaman & Nicobar Islands": "AndamanandNicobar",
    "Andhra Pradesh": "AndhraPradesh",
    "Arunachal Pradesh": "ArunachalPradesh",
    "Assam": "Assam",
    "Bihar": "Bihar",
    "Chandigarh": "Chandigarh",
    "Chhattisgarh": "Chhattisgarh",
    "Dadra & Nagar Haveli and Daman & Diu": "DadraandNagarHaveliandDamanandDiu",
    "Delhi": "NCTofDelhi",
    "Goa": "Goa",
    "Gujarat": "Gujarat",
    "Haryana": "Haryana",
    "Himachal Pradesh": "HimachalPradesh",
    "Jammu and Kashmir": "JammuandKashmir",
    "Jharkhand": "Jharkhand",
    "Karnataka": "Karnataka",
    "Kerala": "Kerala",
    "Ladakh": "Ladakh",
    "Lakshadweep": "Lakshadweep",
    "Madhya Pradesh": "MadhyaPradesh",
    "Maharashtra": "Maharashtra",
    "Manipur": "Manipur",
    "Meghalaya": "Meghalaya",
    "Mizoram": "Mizoram",
    "Nagaland": "Nagaland",
    "Odisha": "Odisha",
    "Puducherry": "Puducherry",
    "Punjab": "Punjab",
    "Rajasthan": "Rajasthan",
    "Sikkim": "Sikkim",
    "Tamil Nadu": "TamilNadu",
    "Telangana": "Telangana",
    "Tripura": "Tripura",
    "Uttar Pradesh": "UttarPradesh",
    "Uttarakhand": "Uttarakhand",
    "West Bengal": "WestBengal"
    }

    filtered_data = df[df['Year'] == selected_year].copy()
    filtered_data['State_GeoJSON'] = filtered_data['States/Union Territories'].map(state_to_id_map)


    merged_data = india_states.merge(
    filtered_data,
    left_on="NAME_1",
    right_on="State_GeoJSON",
    how="left"
    )

    if selected_vehicle_type in filtered_data.columns:
        fig = px.choropleth(
            merged_data,
            geojson=merged_data.__geo_interface__,
            locations="NAME_1",
            featureidkey="properties.NAME_1",
            color=selected_vehicle_type,
            hover_name="NAME_1",
            title=f"State-wise Distribution of {selected_vehicle_type} in {selected_year}",
            color_continuous_scale="Viridis",
            height=800,
            width=1000
        )

        fig.update_geos(
            fitbounds="locations",
            visible=False 
        )
        st.plotly_chart(fig, use_container_width=True)




        #---Bar graph
        fig_bar = px.bar(
            filtered_data.sort_values(by=selected_vehicle_type, ascending=False), 
            x="States/Union Territories",
            y=selected_vehicle_type,
            text=selected_vehicle_type,
            labels={selected_vehicle_type: "Number of Vehicles", "State": "State"},
            color=selected_vehicle_type,
            color_continuous_scale="Viridis"
        )

        fig_bar.update_layout(
            xaxis=dict(
            title="State", 
            tickangle=45,
            tickfont=dict(size=14),
            titlefont=dict(size=18)
            ),
            yaxis=dict(
            title="Number of Vehicles",
            tickfont=dict(size=14),
            titlefont=dict(size=18)
            ),
            height=600,
            width=1000,
            title=dict(x=0.5, font=dict(size=20)),
        )
        st.plotly_chart(fig_bar, use_container_width=True)


        ##----CONCLUSIONS
        
        sorted_data = filtered_data.sort_values(by=selected_vehicle_type, ascending=False)
        
        state_max1 = filtered_data.loc[filtered_data[selected_vehicle_type].idxmax(), 'States/Union Territories']
        top_states = sorted_data.head(5)  # top 5 states
        top_states_summary = ", ".join(f"{row['States/Union Territories']} ({row[selected_vehicle_type]:,.0f})" for _, row in top_states.iterrows())

        
        bottom_states = sorted_data.tail(5)  # bottom 5 states
        bottom_states_summary = ", ".join(f"{row['States/Union Territories']} ({row[selected_vehicle_type]:,.0f})" for _, row in bottom_states.iterrows())

        
        total_vehicles = sorted_data[selected_vehicle_type].sum()
        top_5_contribution = top_states[selected_vehicle_type].sum()
        top_5_percentage = (top_5_contribution / total_vehicles) * 100


        st.subheader("Conclusions")
        st.markdown(f"""
        ### Key Insights for {selected_vehicle_type} in {selected_year}:
        1. **Top 5 States**: {top_states_summary}.
        2. **States with the Lowest Counts**: {bottom_states_summary}.
        3. **Top 5 States Contribution**: {top_5_contribution:,.0f} vehicles, accounting for {top_5_percentage:.1f}% of the total..
        """)


        # ####--------
        state = state_max1
        dominant_vehicle_type = selected_vehicle_type
        conclusions2 = generate_road_construction_conclusions(state, dominant_vehicle_type, total_vehicles)

        st.subheader("Road Construction and Transit Suggestions")
        for idx, conclusion in enumerate(conclusions2, start=1):
            st.markdown(f"**{idx}. {conclusion}**")


    else:
        st.warning(f"{selected_vehicle_type} not found in the dataset.")



    st.markdown("""
    
    **Data source:** https://www.data.gov.in/
    """)
