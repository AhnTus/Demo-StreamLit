import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
#Đọc file:
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")
movies_data.info()
movies_data.dropna()
#Hiển thị phần header 
st.title ("Interactive Dashboard")
st.subheader("Interact with this dashboard using the widgets on the sidebar")
#Lọc dữ liệu chỉ lấy duy nhất
years = movies_data['year'].unique().tolist()
genres = movies_data['genre'].unique().tolist()
scores = movies_data['score'].unique().tolist()

            ###Side bar### 
#Chọn giá trị
st.sidebar.title("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range")
min_value = 1.00
max_value = 10.00
filter_score = st.sidebar.slider('Choose a value::', min_value, max_value,value=(3.00, 4.00))
#Chọn thể loại
st.sidebar.title("Select your preferred genre(s) and year to view the movies released that year and on that genre")
filter_genres = st.sidebar.multiselect('Choose Genre:', genres,default = ['Drama'])
#Chọn năm 
#Năm bên slidebar
filter_year = st.sidebar.selectbox('Choose a year:',years,0)
#Lọc theo điểm số (Score)
score_info = (movies_data['score'].between(*filter_score))
#Lọc theo thể loại và năm 
year_info = (movies_data['genre'].isin(filter_genres))&(movies_data['year'] == filter_year)

            ###Phần biểu đồ visualization### 
#table và biểu đồ linechart
table1, linechart2 = st.columns([2,3])
with table1:
    st.write(" Lists of movies filtered by year and Genre ")
    dataframe_genre_year = movies_data[year_info].groupby(['name', 'genre'])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    st.dataframe(dataframe_genre_year, width = 600)
with linechart2:
    st.write(" User score of movies and their genre ")
    dataframe_count_year = movies_data[score_info].groupby('genre')['score'].count()
    dataframe_count_year = dataframe_count_year.reset_index()
    figpx = px.line(dataframe_count_year, x = 'genre', y = 'score')
    st.plotly_chart(figpx)

#Biểu đồ bar chart
st.write("""Average Movie Budget, Grouped by Genre""")
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']
fig = plt.figure(figsize = (20, 10))
plt.bar(genre, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing The Average Budget of Movies in Each Genre')
st.pyplot(fig)