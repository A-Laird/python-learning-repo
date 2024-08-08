import streamlit as st
import pandas as pd
import plotly.express as px

############################## Utility functions ###########################

#def age_check(dob):
#    today = pd.to_datetime('today')
#
#    if dob + pd.DateOffset(years=6) > today:
#        return '0-5 years'
#    elif dob + pd.DateOffset(years=12) > today:
#        return '6-11 years'
#    elif dob + pd.DateOffset(years=18) > today:
#        return '12-17 years'
#    else:
#        return '18+ years'
def age_check(dob):
    #today = pd.to_datetime('today')
 
    if dob + pd.DateOffset(years=6) > ref_date: #today:
        return '0-5 years'
    elif dob + pd.DateOffset(years=12) > ref_date: #today:
        return '6-11 years'
    elif dob + pd.DateOffset(years=18) > ref_date: #today:
        return '12-17 years'
    else:
        return '18+ years'


def data_cleaner(df):
    df['SEX'] = df['SEX'].map({1:'Male',
                               2:'Female'})
    
    df['DOB'] = pd.to_datetime(df['DOB'], format="%d/%m/%Y", errors='coerce')

    df['AGE RANGE'] = df['DOB'].apply(age_check)

    df.drop(['CHILD', 'UPN', 'MOTHER', 'MC_DOB'], axis=1, inplace=True)

    ethnic_list = list(df['ETHNIC'].unique())

    return df, ethnic_list

################################### plot functions ##########################

def gender_plot(df):
    fig =px.histogram(df, 
                      x='SEX', 
                      title='903 cohort breakdown via sex',
                      labels={'SEX':'Sex'})
    return fig

def age_pie(df):
    fig = px.pie(df,
                 names='AGE RANGE',
                 title='903 age ranges')
    return fig
############################ Main App Cose #################################

st.title('903 Header Analysis Tool')

file = st.file_uploader('Please upload 903 header for analysis')

# if file !=None:   "same as below, if statement needed or error when no file uploaded"
if file:
    unclean_df = pd.read_csv(file)

    df, ethnic_list = data_cleaner(unclean_df)

    ref_date = st.sidebar.date_input(
        label='Set reference date',
        value=pd.to_datetime('today')
    )

    chosen_ethnicities = st.sidebar.multiselect('Choose ethnicities to view breakdown by:',
                   options=ethnic_list,
                   default=ethnic_list)
    
    age_range = st.sidebar.slider(
        label='Select age range for visualisations',
        min_value=0,
        max_value=25,
        value=(0, 25)
    )
    st.write(f'Selected referecne date: {ref_date}')
    st.write(f'Lower age bound: {age_range[0]}')
    st.write(f'Upper age bound: {age_range[1]}')

    df = df[(pd.to_datetime('today') - pd.DateOffset(years=age_range[0]) >= df['DOB']) & (
        pd.to_datetime('today') - pd.DateOffset(years=age_range[1]) <= df['DOB']
    )]
   # replaced with the above 
   # min_age = 5
   # max_age = 16
    
   # df = df[(pd.to_datetime('today') - pd.DateOffset(years=min_age) >= df['DOB']) & (
   #     pd.to_datetime('today') - pd.DateOffset(years=max_age) <= df['DOB']
  #  )]
    
    df = df[df['ETHNIC'].isin(chosen_ethnicities)]


    st.dataframe(df)

    gender_bar = gender_plot(df)
    st.plotly_chart(gender_bar)

    age_pie_fig = age_pie(df)
    st.plotly_chart(age_pie_fig)

    #changed today to ref_date and broke it