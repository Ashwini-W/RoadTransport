

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import snowflake.connector
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
from matplotlib.ticker import MaxNLocator

# @st.cache(allow_output_mutation=True)
# def load_data(): 

#     df = pd.read_csv("dataset/YearlyFreightandPassengerMovement_RoadTransport_1999to2019.csv")
#     print(df.head())    
#     return df




def show_analysis2_page():

    # data = load_data()
    # st.dataframe(data) 



    def get_snowflake_connection():
        conn = snowflake.connector.connect( 
            user=st.secrets["user"],
            password=st.secrets["password"],
            account=st.secrets["account"],
            database=st.secrets["database"],
            warehouse='COMPUTE_WH',
            schema='ACCOUNTADMIN'
        )
        return conn

    conn = get_snowflake_connection()
    st.write("Fetching data from Snowflake...")
    # query = "SELECT CURRENT_VERSION()"
    query1= "SELECT * from ROADTRASPORT.FREIGHTANDPASSENGETABLE.FREIGHPASSENGER_T"
    #st.write(query1)
    cursor = conn.cursor()
    try:
        cursor.execute(query1)
        # version = cursor.fetchone()
        data_snow =cursor.fetchall()
        df_data=pd.DataFrame(data_snow)
        df_data.columns = ['YEAR', 'FREIGHT', 'PASSENGER', 'GDPRATE']
        st.markdown("""
        The dataset contains columns lie Year, Freight(Heavy goods transported in bulk),Passenger and GDP Rate
        """)
        st.write(df_data)

        freightPassenger_analysis(df_data)
    finally:
        cursor.close()
        conn.close()


def freightPassenger_analysis(df_data):
        data=df_data
        st.title("Freight, Passenger Movement & GDP Growth Overlay for 1999 to 2018")

        fig, ax1 = plt.subplots(figsize=(14, 5))

        ax1.set_xlabel('YEAR')
        ax1.set_ylabel('Freight & Passenger Movement (Billion)', color='tab:blue')
        ax1.plot(data['YEAR'], data['FREIGHT'], label='Freight Movement', color='tab:blue', marker='o')
        ax1.plot(data['YEAR'], data['PASSENGER'], label='Passenger Movement', color='tab:green', marker='o')
        ax1.tick_params(axis='y', labelcolor='tab:blue', labelsize=8)
        ax1.legend(loc='upper left', fontsize=8)
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

        ax2 = ax1.twinx()
        ax2.set_ylabel('GDP Growth Rate', color='tab:red')
        ax2.plot(data['YEAR'], data['GDPRATE'], label='GDP Growth Rate', color='tab:red', linestyle='--', marker='x')
        ax2.tick_params(axis='y', labelcolor='tab:red', labelsize=8)
        ax2.legend(loc='upper right', fontsize=8)

        
        plt.xticks(rotation=45,fontsize=8)
        plt.title('Overlay of Freight & Passenger Movement with GDP Growth Rate')

        st.pyplot(fig)

        st.markdown('''
    1. Freight movement shows a steady upward trend across the years, indicating consistent growth in the transportation of goods. That means there an expanding eonomy,trade practices,and improve in infrastructe.
    2. Passenger movement also increases steadily, but its rate of growth appears faster than freight movement in some periods.This shows increase in urbanization along with strong economy.
    3. The upward trends in both freight and passenger movement suggest that road transport plays a vital role in economic development.
    4. Higher GDP growth coincides with increased freight and passenger movement (e.g., during strong economic periods). Lower GDP growth sees slower increases in movement, suggesting some correlation between economic activity and transport usage.      
    5. If the passenger growth rate is consistently higher than the freight growth rate, this indicates:
    Rapid urbanization or increased mobility needs as people increasingly rely on road transport for commuting, especially in rapidly growing region.
    Greater focus on passenger transport infrastructure or services compared to freight.

    **OBSERVTION:** The 2014-2016 oil price collapse news had a significant impact on global petrol (gasoline) prices, driven by a sharp decline in crude oil prices.
    https://thedocs.worldbank.org/en/doc/910311512412250749-0050022017/original/GlobalEconomicProspectsJan2018TopicalIssueoilpricecollapse.pdf.
    
    Petrol prices closely track crude oil prices, as crude oil is the primary raw material for petrol. Lower petrol prices reduced transportation costs leading to more usage of transport vehicles at cheaper prices .
    ''')

        data['Freight Growth Rate (%)'] = data['FREIGHT'].pct_change() * 100
        data['Passenger Growth Rate (%)'] = data['PASSENGER'].pct_change() * 100

        figa, ax = plt.subplots(figsize=(14, 6))

        ax.plot(data['YEAR'], data['Freight Growth Rate (%)'], label='Freight Growth Rate (%)', color='blue', marker='o')

        ax.plot(data['YEAR'], data['Passenger Growth Rate (%)'], label='Passenger Growth Rate (%)', color='green', marker='o')

        ax.set_xlabel('YEAR', fontsize=12)
        ax.set_ylabel('Growth Rate (%)', fontsize=12)
        ax.set_title('Year-on-Year Growth Rates: Freight vs. Passenger Movement', fontsize=14)
        ax.legend(fontsize=10)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.xticks(rotation=45)
        plt.grid(alpha=0.5)
        plt.tight_layout()

        st.pyplot(figa)













































'''   DELETEE

    # Filter relevant columns for passenger vehicles and total transport
    data_filtered = data[['Year', 'Light Motor Vehicles (Passengers) (VI) - Three seaters', 
                        'Light Motor Vehicles (Passengers) (VI) - Four to six seaters', 
                        'Total Transport (I TO VII)']]

    # Rename columns for convenience
    data_filtered.columns = ['Year', 'LMV_Pass_3_Seaters', 'LMV_Pass_4_to_6_Seaters', 'Total_Transport']

    # Create features and labels for regression
    X = data_filtered[['LMV_Pass_3_Seaters', 'LMV_Pass_4_to_6_Seaters']]
    y = data_filtered['Total_Transport']

    # Split the data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a linear regression model
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    # Make predictions
    y_pred = regressor.predict(X_test)

    # Streamlit app layout
    st.title("Predicting Public Transport Demand based on Passenger Vehicles")
    st.write("This app uses vehicle registration data to predict the demand for public transport based on passenger vehicles.")

    # Scatter plot for passenger vehicles vs total transport
    st.subheader("Scatter Plot: Light Motor Passenger Vehicles vs Total Transport")
    plt.figure(figsize=(6, 4))
    plt.scatter(data_filtered['LMV_Pass_3_Seaters'], data_filtered['Total_Transport'], label='3 Seaters', color='blue')
    plt.scatter(data_filtered['LMV_Pass_4_to_6_Seaters'], data_filtered['Total_Transport'], label='4 to 6 Seaters', color='green')
    plt.xlabel("Light Motor Vehicles (Passengers)")
    plt.ylabel("Total Transport Demand")
    plt.legend()
    plt.title("Passenger Vehicles vs Total Transport")
    st.pyplot(plt)

    # Bar graph for total passenger vehicles per year
    st.subheader("Bar Graph: Total Passenger Vehicles per Year")
    data_filtered['Total_LMV_Pass'] = data_filtered['LMV_Pass_3_Seaters'] + data_filtered['LMV_Pass_4_to_6_Seaters']
    data_grouped = data_filtered.groupby('Year')['Total_LMV_Pass', 'Total_Transport'].sum().reset_index()

    # Plotting the bar graph
    fig, ax1 = plt.subplots(figsize=(8, 6))

    ax1.bar(data_grouped['Year'], data_grouped['Total_LMV_Pass'], color='blue', alpha=0.6, label='Total LMV Passenger Vehicles')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Total LMV Passenger Vehicles', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis to plot Total Transport
    ax2 = ax1.twinx()
    ax2.plot(data_grouped['Year'], data_grouped['Total_Transport'], color='green', marker='o', label='Total Transport Demand')
    ax2.set_ylabel('Total Transport Demand', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    fig.tight_layout()
    st.pyplot(fig)

    # Regression Model Predictions
    st.subheader("Regression Model: Predicting Total Transport Demand")
    plt.figure(figsize=(6, 4))
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', lw=2)
    plt.xlabel("Actual Total Transport Demand")
    plt.ylabel("Predicted Total Transport Demand")
    plt.title("Predicted vs Actual Total Transport Demand")
    st.pyplot(plt)

'''
