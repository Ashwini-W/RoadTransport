

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


@st.cache(allow_output_mutation=True)
def load_data(): 

    df = pd.read_csv("dataset/Revenue from Taxes on Motor Vehicle and Passenger and Goodsfor1718_1819Statewise.csv")
    print(df.head())    
    return df


def show_analysis_page():

    st.title("Revenue generated through taxes trends")

    data = load_data()
    st.dataframe(data) 



    top_n = 5
    top_n = 5  
    def prepare_top_contributors(data, percentage_column, top_n):
        data = data.sort_values(by=percentage_column, ascending=False)
        top_states = data.iloc[:top_n]
        others = pd.DataFrame({
            'Name of State/UT': ['Others'],
            percentage_column: [data.iloc[top_n:][percentage_column].sum()]
        })
        final_data = pd.concat([top_states, others], ignore_index=True)
        return final_data['Name of State/UT'], final_data[percentage_column]

    state_names_2017_18, percentage_2017_18 = prepare_top_contributors(
        data,
        '2017-18 (Accounts) - Percentage of States/UTs Own Tax Revenue',
        top_n
    )

    state_names_2018_19, percentage_2018_19 = prepare_top_contributors(
        data,
        '2018-19 (Accounts) - Percentage of States/UTs Own Tax Revenue',
        top_n
    )

    st.title("Statewise Revenue Contribution Analysis (Top Contributors)")

    # Pie Chart for 2017-18
    fig_2017_18, ax1 = plt.subplots(figsize=(6, 4))
    ax1.pie(
        percentage_2017_18,
        labels=state_names_2017_18,
        autopct='%1.1f%%',
        startangle=60,
        textprops={'fontsize': 6}
    )
    ax1.set_title("Top Contributors to Revenue (2017-18)",fontsize=6)
    st.subheader("Top Contributors to Revenue (2017-18)")
    st.pyplot(fig_2017_18)

    # # Pie Chart for 2018-19
    fig_2018_19, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(
        percentage_2018_19,
        labels=state_names_2018_19,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 8}
    )
    ax2.set_title("Top Contributors to Revenue (2018-19)",fontsize=6)
    st.subheader("Top Contributors to Revenue (2018-19)")
    st.pyplot(fig_2018_19)


##------------------- PART 1
    data['Change in Percentage of Own Tax Revenue'] = (
        data['2018-19 (Accounts) - Percentage of States/UTs Own Tax Revenue'] -
        data['2017-18 (Accounts) - Percentage of States/UTs Own Tax Revenue']
    )

    sorted_data = data.sort_values(by='Change in Percentage of Own Tax Revenue', ascending=False)

    st.title("Change in Percentage of Own Tax Revenue from Vehicle-Related Taxes (2017-18 vs. 2018-19)")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(
        sorted_data['Name of State/UT'],
        sorted_data['Change in Percentage of Own Tax Revenue'],
        color='lightgreen'
    )
    ax.axhline(0, color='red', linewidth=1, linestyle='--')
    ax.set_xlabel("State/UT", fontsize=8)
    ax.set_ylabel("Change in Percentage of Own Tax Revenue (%)", fontsize=8)
    ax.set_title("Change in Percentage of Own Tax Revenue from Vehicle-Related Taxes", fontsize=8)
    plt.xticks(rotation=90,fontsize=6)
    plt.yticks(fontsize=6)
    plt.tight_layout()

    st.pyplot(fig)



# ------------PART 2


    data['Change in Tax on Goods and Pass.'] = (
        data['2018-19 (Accounts) - Tax on Goods and Pass.'] -
        data['2017-18 (Accounts) - Tax on Goods and Pass.']
    )

    sorted_data = data.sort_values(by='Change in Tax on Goods and Pass.', ascending=False)

    st.title("Change in Tax on Goods and Passenger Transportation (2017-18 vs. 2018-19)")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(
        sorted_data['Name of State/UT'],
        sorted_data['Change in Tax on Goods and Pass.'],
        color='skyblue'
    )
    ax.axhline(0, color='red', linewidth=1, linestyle='--')
    ax.set_xlabel("State/UT", fontsize=8)
    ax.set_ylabel("Change in Tax Revenue (₹)", fontsize=8)
    ax.set_title("Change in Tax on Goods and Passenger Transportation", fontsize=10)
    plt.xticks(rotation=90,fontsize=6)
    plt.yticks(fontsize=6)
    plt.tight_layout()

    st.pyplot(fig)

    st.subheader("Insights")
    st.write("""
 
    - Through pie chart we can see that **Jammu and Kashmir, Nagaland ,Bihar** are top contributors towards the tax revenues.
    - States with bars above the reference line have seen increase in vehicle-related taxes as a share of their total own tax revenue.
    - This could indicate growing vehicle ownership, increased economic activity related to transportation, or improved tax collection mechanisms.
    - Where as, States with bars below the reference line could result from reduced transportation activity, or potential unexecuted vehicle-related taxes policies.
    - Positive changes might reflect strong transportation-related economic growth, creating opportunities to further invest in sustainable transport and public infrastructure.
    """)

