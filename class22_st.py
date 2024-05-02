import streamlit as st 
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")

df = pd.read_excel("superstore_modified.xlsx")
all_states = sorted(df["State"].unique())
target_states = st.multiselect("Choose target states", all_states, all_states)
df = df[df["State"].isin(target_states)]


col1, col2 = st.columns([7, 3])
with col1: # for figure 1
    profit_ratio_state = df.groupby("State")["Profit"].sum() / df.groupby("State")["Sales"].sum() # series
    profit_ratio_state = profit_ratio_state.reset_index(name="ProfitRatio") # data frame
    fig1 = px.choropleth(locations=profit_ratio_state["State"],
             locationmode="USA-states", scope="usa", 
              color=profit_ratio_state["ProfitRatio"],
             color_continuous_scale="Viridis")
    st.plotly_chart(fig1, use_container_width=True)

with col2: # for figure 2
    a = df.groupby("Category")["Profit"].sum()
    b = df.groupby("Category")["Sales"].sum()
    
    profit_ratio_category = a/b 
    profit_ratio_category = profit_ratio_category.reset_index(name="ProfitRatio")
    fig2 = px.bar(profit_ratio_category, x="Category", y="ProfitRatio",
      color="Category")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns([5,5])
with col3: # for figure 3
    df["YearMonth"] = pd.to_datetime(df["Order Date"]).dt.strftime("%Y-%m")
    a = df.groupby(["Category", "YearMonth"])["Profit"].sum()
    b = df.groupby(["Category", "YearMonth"])["Sales"].sum()
    profit_ratio_category_ym = a/b
    profit_ratio_category_ym = profit_ratio_category_ym.reset_index(name="ProfitRatio")
    fig3 = px.line(profit_ratio_category_ym, x="YearMonth", y="ProfitRatio",
       color="Category")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.treemap(df, path=[px.Constant("all"), "Category", "Sub-Category"], 
                  values='Sales')
    st.plotly_chart(fig4, use_container_width=True)





    