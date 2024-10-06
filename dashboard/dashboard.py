import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# page config
st.set_page_config(page_title="Bike-Sharing Dashboard",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide")
# load dataset
hour_df = pd.read_csv("https://github.com/andhikaprimaditama22/Dicoding-Capital-Bike-Sharing-Analysis/raw/refs/heads/main/dashboard/hour_clean.csv")

# convert dteday data type to date
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# create helper function
def create_total_rides_df(hour_df): 
    total_rides_df = hour_df['cnt'].sum()
    
    return total_rides_df

def create_casual_user_df(hour_df):
    casual_user_df = hour_df['casual'].sum()
    
    return casual_user_df
    
def create_registered_user_df(hour_df):
    registered_user_df = hour_df['registered'].sum()
    
    return registered_user_df
   
def create_hourly_rides_df(hour_df):
    hourly_bike_rides_df = hour_df.groupby("hr").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
})
    hourly_bike_rides_df = hourly_bike_rides_df.reset_index()
    
    return hourly_bike_rides_df

def create_monthly_rides_df(df):
    monthly_rides_df = hour_df.groupby("mnth").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    
    monthly_rides_df = monthly_rides_df.reset_index()
    monthly_rides_df = monthly_rides_df.melt(
        id_vars='mnth', 
        value_vars=['casual', 'registered'], 
        var_name='status', 
        value_name='count')
    
    monthly_rides_df['mnth'] = pd.Categorical(monthly_rides_df['mnth'],
                                             categories=['January', 'February', 'March', 'April', 
                                                         'May', 'June', 'July', 'August', 'September', 
                                                         'October', 'November', 'December'])
    
    monthly_rides_df = monthly_rides_df.sort_values('mnth')
    
    return monthly_rides_df

def create_weekly_rides_df(hour_df):
    weekly_rides_df = hour_df.groupby("weekday").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
    })
    
    weekly_rides_df = weekly_rides_df.reset_index()
    weekly_rides_df = weekly_rides_df.melt(
    id_vars='weekday', 
    value_vars=['casual', 'registered'], 
    var_name='status', 
    value_name='count')
    
    weekly_rides_df['weekday'] = pd.Categorical(weekly_rides_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 
                                                         'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekly_rides_df = weekly_rides_df.sort_values('weekday')

    return weekly_rides_df

def create_weather_rides_df(hour_df):
    weather_rides_df = hour_df.groupby("weathersit").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
    })
    
    weather_rides_df = weather_rides_df.reset_index()
    weather_rides_df = weather_rides_df.melt(
    id_vars='weathersit', 
    value_vars=['casual', 'registered'], 
    var_name='status', 
    value_name='count')
    
    weather_rides_df = weather_rides_df.sort_values(by=['count'], ascending=True)
    
    return weather_rides_df

def create_season_rides_df(hour_df):
    season_rides_df = hour_df.groupby("season").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
    })
    
    season_rides_df = season_rides_df.reset_index()
    season_rides_df = season_rides_df.melt(
    id_vars='season', 
    value_vars=['casual', 'registered'], 
    var_name='status', 
    value_name='count')
    
    season_rides_df = season_rides_df.sort_values(by=['count'], ascending=True)
    
    return season_rides_df

# filter component
min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

# sidebar
with st.sidebar:
    # adding a sidebar title and logo
    st.title("Capital Bikeshare")
    st.image("https://raw.githubusercontent.com/andhikaprimaditama22/Dicoding-Capital-Bike-Sharing-Analysis/main/dashboard/bikeshare.png")
    
    # retrive start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
# assign filter component to main_df
main_df = hour_df[
    (hour_df["dteday"] >= str(start_date)) &
    (hour_df["dteday"] <= str(end_date))
]      
    
# assign helper function that has been created to main_df
total_rides_df = create_total_rides_df(main_df)
casual_user_df = create_casual_user_df(main_df)
registered_user_df = create_registered_user_df(main_df)
hourly_rides_df = create_hourly_rides_df(main_df)
monthly_rides_df = create_monthly_rides_df(main_df)
weekly_rides_df = create_weekly_rides_df(main_df)
weather_rides_df = create_weather_rides_df(main_df)
season_rides_df = create_season_rides_df(main_df)

# main page
st.title("Bike-Sharing Dashboard :chart_with_upwards_trend:")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    total_rides = total_rides_df
    st.metric("Total Rides", value=total_rides)
with col2:
    casual_user = casual_user_df
    st.metric("Total Casual Rides", value=casual_user_df)
with col3:
    registered_user = registered_user_df
    st.metric("Total Registered Rides", value=registered_user_df)
 
# chart
fig1 = px.line(hourly_rides_df,
              x='hr',
              y=['casual', 'registered', 'cnt'],
              color_discrete_sequence=["skyblue", "orange", "red"],
              markers=True,
              title="Hourly Count of Bikeshare Rides").update_layout(xaxis_title='Hour', yaxis_title='Total Rides',)
fig1.update_layout(legend=dict(title='Legends'))
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(monthly_rides_df,
              x='mnth',
              y=['count'],
              color = 'status', 
              barmode='group',
              title='Monthly Count of Bikeshare Rides').update_layout(xaxis_title='Month', yaxis_title='Total Rides')

st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(weekly_rides_df,
              x='weekday',
              y=['count'],
              color = 'status', 
              barmode='group',
              title='Weekly Count of Bikeshare Rides').update_layout(xaxis_title='Day', yaxis_title='Total Rides')

st.plotly_chart(fig3, use_container_width=True)

fig4 = px.bar(weather_rides_df,
              x=['count'],
              y='weathersit',
              color = 'status',
              barmode='group',
              title='Bikeshare Rides by Weather').update_layout(xaxis_title='Total Rides', yaxis_title='Weather', showlegend=False)

fig5 = px.bar(season_rides_df,
              x=['count'],
              y='season',
              color = 'status',
              barmode='group',
              title='Bikeshare Rides by Season').update_layout(xaxis_title='Total Rides', yaxis_title='Season', showlegend=False)
fig5.update_layout(
    yaxis=dict(side='right', autorange='reversed'),
    xaxis=dict(autorange='reversed')
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig4, use_container_width=True)
right_column.plotly_chart(fig5, use_container_width=True)

st.caption('Copyright ©, created by Andhika Primaditama')