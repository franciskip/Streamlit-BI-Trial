import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
# st.set_page_config(layout='wide')
# from streamlit_card import card
from st_card_component import card_component as card

from PIL import Image

# Page setting
st.set_page_config(layout="wide")

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    @st.cache
    def load_data():
                df = pd.read_csv("store_modified.csv")
                df['Order Date'] = pd.to_datetime(df['Order Date'])
                df['Ship Date'] = pd.to_datetime(df['Ship Date'])
                return df
                # df.index.name = "Date"
                # print(df.index.name)
    df = load_data()
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Home","Dashboard", "About Me"],
            icons=['house', 'bar-chart-line', 'person-lines-fill'],
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "color": "black",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
    
    if selected == 'Home':
        st.title('Dashboard of Sales and Profit')
        st.markdown("<h3 style='text-align: center; color: green; background: #D3D3D3; margin: 3px'>Super Store Dataset</h1>", unsafe_allow_html=True)
        st.write(df)

        st.markdown("<h3 style='text-align: center; color: green; background: #D3D3D3; margin: 3px'>Super Store Dataset Size</h1>", unsafe_allow_html=True)
        row_col, columns_col = st.columns(2)
        rows = f"Number of rows: **{df.shape[0]}**"
        cols = f"Number of columns: **{df.shape[1]}**"
        with row_col:
            st.markdown(rows)
        with columns_col:
            st.markdown(cols)
    elif selected == "Dashboard":
        st.title('Dashboard of Sales and Profit')
        st.markdown("<h3 style='text-align: center;  margin: 3px'>Sales and Profits Primary KPIs</h1>", unsafe_allow_html=True)

        year_list = [2014, 2015, 2016, 2017, "All"]
        year_slider = st.select_slider('Select Year', year_list)
        
        if year_slider == "All":
            df1 = df
        elif year_slider == 2014:
            df1 = df[df["Year"]==2014]
        elif year_slider == 2015:
            df1 = df[df["Year"]==2015]
        elif year_slider == 2016:
            df1 = df[df["Year"]==2016]
        else:
            df1 = df[df["Year"]==2017]
        col1, col2, col3, col4 = st.columns(4)

        st.markdown("""
            <style>
            div[data-testid="metric-container"] {
            background-color: rgba(28, 131, 225, 0.1);
            border: 1px solid rgba(28, 131, 225, 0.1);
            padding: 5% 5% 5% 10%;
            border-radius: 5px;
            color: rgb(30, 103, 119);
            overflow-wrap: break-word;
            }

            /* breakline for metric text         */
            div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
            overflow-wrap: break-word;
            white-space: break-spaces;
            color: green;
            font-size: 20px;
            }
            </style>
            """
            , unsafe_allow_html=True)

        with col1:
            st.metric(label="Total Sales", value=df1['Sales'].sum().round(0))
        with col2:
            st.metric(label="Average Sales", value=df1['Sales'].mean().round(0))
        with col3:
            st.metric(label="Total Profit", value=df1['Profit'].sum().round(0))
        with col4:
            st.metric(label="Average Profit", value=df1['Profit'].mean().round(0))

        st.markdown("<h3 style='text-align: center;  margin: 3px'>Analysis of Sales and Profits Based on Region, Segment, and Category</h1>", unsafe_allow_html=True)
       
        year = ['All',2014, 2015, 2016, 2017]
        option = st.selectbox('Select Year', year)
        if option == 'All':
            df1 = df
        elif option == 2014:
            df1 = df[df["Year"]==2014]
        elif option == 2015:
            df1 = df[df["Year"]==2015]
        elif option == 2016:
            df1 = df[df["Year"]==2016]
        else:
            df1 = df[df["Year"]==2017]
        year, seg, cat = st.columns(3)
        with year:
            def year_donut():
                fig = px.pie(df1, values='Sales', names='Region', title='Sales by region', hole=0.5)
                fig.update_traces(textinfo = 'percent + value', textfont_size=15)
                fig.update_layout(title_text = "Total Sales by Region", title_x = 0.3)
                fig.update_layout(legend = dict(
                    orientation = 'h', 
                    yanchor = 'bottom', 
                    y = -0.1, 
                    xanchor = 'center', 
                    x = 0.5
                ))
                st.plotly_chart(fig, use_container_width=True)
            year_donut()
        
        with seg:
            def seg_donut():
                fig = px.pie(df1, values='Sales', names='Segment', title='Sales by Segment', hole=0.5)
                fig.update_traces(textinfo = 'percent + value', textfont_size=15)
                fig.update_layout(title_text = "Total Sales by Segment", title_x = 0.5)
                fig.update_layout(legend = dict(
                    orientation = 'h', 
                    yanchor = 'bottom', 
                    y = -0.3, 
                    xanchor = 'center', 
                    x = 0.7
                ))
                st.plotly_chart(fig, use_container_width=True)
            seg_donut()

        with cat:
            def cat_donut():
                fig = px.pie(df1, values='Sales', names='Category', title='Sales by Category', hole=0.5, template='seaborn',labels={'Sales':'Total Sales'})
                fig.update_traces(textinfo = 'percent + value', textfont_size=15)
                fig.update_layout(title_text = "Total Sales by Category", title_x = 0.5)
                fig.update_layout(legend = dict(
                    orientation = 'h', 
                    yanchor = 'bottom', 
                    y = -0.1, 
                    xanchor = 'center', 
                    x = 0.5
                ))
                st.plotly_chart(fig, use_container_width=True)
            cat_donut()

        st.markdown("<hr/>",unsafe_allow_html=True)
        r, s, c = st.columns(3)
        with r:
            def r_donut():
                fig = px.pie(df1, values='Profit', names='Region', title='Profit by region', hole=0.5, template='ggplot2', labels={'Profit':'Total Profit'})
                fig.update_traces(textinfo = 'percent + value', textfont_size=15)
                fig.update_layout(title_text = "Total Profit by Region", title_x = 0.7)
                fig.update_layout(legend = dict(
                    orientation = 'h', 
                    yanchor = 'bottom', 
                    y = -0.1, 
                    xanchor = 'center', 
                    x = 0.5
                ))
                st.plotly_chart(fig, use_container_width=True)
            r_donut()
        
        with s:
            def s_donut():
                fig = px.pie(df1, values='Profit', names='Segment', title='Profit by Segment', hole=0.5, template='plotly',labels={'Profit':'Total Profit'})
                fig.update_traces(textinfo = 'percent + value', textfont_size=15)
                fig.update_layout(title_text = "Total Profit by Segment", title_x = 0.7)
                fig.update_layout(legend = dict(
                    orientation = 'h', 
                    yanchor = 'bottom', 
                    y = -0.1, 
                    xanchor = 'center', 
                    x = 0.5
                ))
                st.plotly_chart(fig, use_container_width=True)
            s_donut()

        with c:
            def c_donut():
                fig = px.pie(df1, values='Profit', names='Category', title='Profit by Segment', hole=0.5, template='seaborn',labels={'Profit':'Total Profit'})
                fig.update_traces(textinfo = 'percent + value', textfont_size=15)
                fig.update_layout(title_text = "Total Profit by Category", title_x = 0.7)
                fig.update_layout(legend = dict(
                    orientation = 'h', 
                    yanchor = 'bottom', 
                    y = -0.1, 
                    xanchor = 'center', 
                    x = 0.5
                ))
                st.plotly_chart(fig, use_container_width=True)
            c_donut()

        st.markdown('<hr/>', unsafe_allow_html=True)

       
        df_q = df1.groupby("Quarter")[["Sales", "Profit"]].mean().round(2)
        def combo_chart():
            fig = px.line(df_q, x=df_q.index, y='Profit', height=500, width=900, markers=True, text = "Profit", color=px.Constant("Average Profit"),
            color_discrete_sequence=['yellow'], labels={'Profit':'Average Profit'}, template = 'seaborn')
            fig.update_traces(textposition = "top center", marker_size=10)
            fig.add_bar(x=df_q.index, y=df_q['Sales'], name='Average Sales', text = df_q['Sales'], textposition='outside', marker={'color':'purple'})
            fig.update_layout(title_text = "Quarterly Average Sales and Profit", title_x = 0.5)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            st.plotly_chart(fig)
        combo_chart()

        st.markdown("<h3 style='text-align: center;  margin: 3px'>Top and Bottom 5 States in terms of Average Sales and Profits</h1>", unsafe_allow_html=True)
       # year selector for top states
        year_selector = ['All',2014, 2015, 2016, 2017]
        y_option = st.selectbox('Select Year', year_selector, key='top states') # year option
        if y_option == 'All':
            df2 = df
        elif y_option == 2014:
            df2 = df[df["Year"]==2014]
        elif y_option == 2015:
            df2 = df[df["Year"]==2015]
        elif y_option == 2016:
            df2 = df[df["Year"]==2016]
        else:
            df2 = df[df["Year"]==2017]

        # region selector for top states
        year_selector = ['All','West', 'East', 'Central', 'South']
        y_option = st.selectbox('Select Region', year_selector, key='region selector') # year option
        if y_option == 'All':
            df3 = df2
        elif y_option == 'West':
            df3 = df2[df2["Region"]=="West"]
        elif y_option == 'East':
            df3 = df2[df2["Region"]=='East']
        elif y_option == 'Central':
            df3 = df2[df2["Region"]=='Central']
        else:
            df3 = df2[df2["Region"]=='South']

        top_selling_col, bottom_selling_col = st.columns(2)

        df_states = df3.groupby("State")[["Sales", "Profit"]].mean().round(2)
        df_states_top = df_states.nlargest(5, 'Sales').sort_values(by='Sales',ascending=False)
        df_states_bottom = df_states.nsmallest(5, 'Sales').sort_values(by='Sales', ascending=True)

        with top_selling_col:
            def horizontal_bar():
                fig = px.bar(df_states_top, x="Sales", y=df_states_top.index, orientation='h', height=300, 
                             width=600, text='Sales', color=df_states_top.index, 
                labels={'Sales':'Average Sales'}, template='ggplot2')
                fig.update_traces(textposition = "outside")
                fig.update_layout(title_text = "Top 5 selling states", title_x = 0.5)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig)
            horizontal_bar()

        with bottom_selling_col:
            def horizontal_bar():
                fig = px.bar(df_states_bottom, x="Sales", y=df_states_bottom.index, orientation='h',color=df_states_bottom.index,
                             height=300, width=600, text='Sales', 
                labels={'Sales':'Average Sales'}, template='ggplot2')
                fig.update_traces(textposition = "outside")
                fig.update_layout(title_text = "Bottom 5 selling states", title_x = 0.5)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig)
            horizontal_bar()

        st.markdown('<hr/>', unsafe_allow_html=True)
        high_profit, low_profit = st.columns(2)
        with high_profit:
            df_states_top_profit = df_states.nlargest(5, 'Profit').sort_values(by='Profit', ascending=False)
            def horizontal_bar():
                fig = px.bar(df_states_top_profit, x="Profit", y=df_states_top_profit.index, 
                             orientation='h', height=300, width=600, text='Profit', color=df_states_top_profit.index, 
                labels={'Profit':'Average Profit'}, template='seaborn')
                fig.update_traces(textposition = "outside")
                fig.update_layout(title_text = "Top 5 Profit making states", title_x = 0.5)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig)
            horizontal_bar()

        with low_profit:
            df_states_bottom_profit = df_states.nsmallest(5, 'Profit').sort_values(by='Profit', ascending=False)
            def horizontal_bar():
                fig = px.bar(df_states_bottom_profit, x="Profit", y=df_states_bottom_profit.index, orientation='h', height=300, width=600, text='Profit', color_discrete_sequence=['brown'], 
                labels={'Profit':'Average Profit'}, template='seaborn')
                fig.update_traces(textposition = "outside")
                fig.update_layout(title_text = "5 Least profitable states", title_x = 0.5)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig)
            horizontal_bar()

        st.markdown("<h3 style='text-align: center;  margin: 3px'>Top and Bottom 5 Profitable Product Sub-Categories</h1>", unsafe_allow_html=True)
       # year selector for top states
        category = ['All','Technology', 'Furniture', "Office Supplies"]
        category_option = st.selectbox('Select Category', category, key='categories') # year option
        if category_option == 'All':
            df4 = df3
        elif category_option == 'Technology':
            df4 = df3[df3["Category"]=='Technology']
        elif category_option == 'Furniture':
            df4 = df3[df3["Category"]=='Furniture']
        else:
            df4 = df3[df3["Category"]=='Office Supplies']

        df_categories = df4.groupby("Sub-Category")[["Sales", "Profit"]].mean().round(2)
        df_categories_top = df_categories.nlargest(5, 'Profit').sort_values(by='Profit')
        df_categories_bottom = df_categories.nsmallest(5, 'Profit').sort_values(by='Profit', ascending=False)

        top_cat, bottom_cat = st.columns(2)
        with top_cat:
            def horizontal_bar():
                fig = px.bar(df_categories_top, x="Profit", y=df_categories_top.index, orientation='h', height=300, width=600, text='Profit', color_discrete_sequence=['orange'], 
                labels={'Profit':'Average Profit'}, template='seaborn')
                fig.update_traces(textposition = "outside")
                fig.update_layout(title_text = "Top 5 Profit making Sub-Categories", title_x = 0.5)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig)
            horizontal_bar()

        with bottom_cat:
            def horizontal_bar():
                fig = px.bar(df_categories_bottom, x="Profit", y=df_categories_bottom.index, orientation='h', height=300, width=600, text='Profit', color_discrete_sequence=['pink'], 
                labels={'Profit':'Average Profit'}, template='seaborn')
                fig.update_traces(textposition = "outside")
                fig.update_layout(title_text = "5 Least profitable Sub-Categories", title_x = 0.5)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig)
            horizontal_bar()

    elif selected == "About Me":
        st.title("FRANCIS KIPKOGEI")
        fk_img = Image.open("profile-img.webp")
        st.markdown("<h3 style='text-align: center; color: green; background: #D3D3D3; margin: 3px'>My Profile</h1>", unsafe_allow_html=True)
        img,  desc =st.columns(2)
        with img:
            st.image(fk_img)
        with desc:
            st.markdown("<h4 style='text-align: center; color: green; margin: 3px'>Data Scientist|Actuarial Scientist|Data Analyst</h4>", unsafe_allow_html=True)
            st.markdown('<p style="text-align: justify;">Data scientist experience and familiar with designing and implementing projects, gathering, cleaning, and organizing data for use by technical and non-technical personnel. Advanced understanding of statistical, research, algebraic and other analytical techniques. Highly organized, motivated, and diligent with significant background in Statistics, Data Analysis, Data Mining, Machine learning, Artificial Intelligence and data intuition. Moreover, I am proficient to an advanced level in using Python, R, SPSS, MS Excel, SQL, Power BI.</p>', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: green; background: #D3D3D3; margin: 3px'>My Experience</h1>", unsafe_allow_html=True)
        stepwise, Zalego,RSSB,CIDRA= st.columns(4)
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        with stepwise:
            st.markdown('##### Senior Data Scientist')
            st.write("Company: Zalda, Stepwise Inc")
            st.write('From: 01/01/2022 - todate')
            st.markdown("<div style='text-align: center; color: green;font-weight: bold;'>Responsibilities</div>", unsafe_allow_html=True)
            st.write("Lead Data Scienst")
            # st.write("Content Developer for DS/DA course")
            st.write("Machine Learning")
            st.write("Data Analysis")
            st.write("Give recommendation based on insights from data")
        with Zalego:
            st.markdown('##### Data Scientist')
            st.write("Company: Zalego Academy, Stepwise Inc")
            st.write('From: 01/04/2021 - todate')
            st.markdown("<div style='text-align: center; color: green;font-weight: bold;'>Responsibilities</div>", unsafe_allow_html=True)
            st.write("Data Science/Data Analysis Technical Instructor")
            st.write("Content Developer for DS/DA course")
            st.write("Machine Learning")
            st.write("Data Analysis")
            st.write("Give recommendation based on insights from data")
        with RSSB:
            st.markdown('##### Data Scientist   Intern')
            st.write("Company: Rwanda Social Security Board, Kigali, Rwanda")
            st.write('From: 01/01/2020 - 01/05/2020')
            st.markdown("<div style='text-align: center; color: green;font-weight: bold;'>Responsibilities</div>", unsafe_allow_html=True)
            # st.write("Data Science/Data Analysis Technical Instructor")
            st.write("Content Developer for DS/DA course")
            st.write("Machine Learning")
            st.write("Data Analysis")
            st.write("Give recommendation based on insights from data")
        st.markdown("<h3 style='text-align: center; color: green; background: #D3D3D3; margin: 3px'>My Skills</h1>", unsafe_allow_html=True)
        with CIDRA:
            st.markdown('##### Data Analyst')
            st.write("Company: CIDRA, Kigali, Rwanda")
            st.write('From: 01/01/2019 - 01/12/2019')
            st.markdown("<div style='text-align: center; color: green;font-weight: bold;'>Responsibilities</div>", unsafe_allow_html=True)
            # st.write("Data Science/Data Analysis Technical Instructor")
            st.write("Content Developer for DS/DA course")
            st.write("Machine Learning")
            st.write("Data Analysis")
            st.write("Give recommendation based on insights from data")
        s1, s2, s3= st.columns(3)
        with s1:
            st.markdown('##### Programming Languages and Packages')
            x = ['Python', 'R', 'SQL',  "MS Excel", 'SPSS','SAS']
            for i in x:
                st.markdown(
                    f'<span style="background-color:#00C4EB;color: #FFFFFF;padding: 0.5em 1em;position: relative;text-decoration: none;font-weight:bold;cursor: pointer;">{i}</span>', unsafe_allow_html=True)
        with s2:
            st.markdown('##### Data Analysis')
            x = ['Data Cleaning','EDA','Data Wrangling', 'Descriptive Analysis', 'Inferential Statistics (A/B Testing', 'Times Series Analysis', 'Predictive Analysis']
            for i in x:
                st.markdown(
                    f'<span style="background-color:#00C4EB;color: #FFFFFF;padding: 0.6em 1em;position: relative;text-decoration: none;font-weight:bold;cursor: pointer;">{i}</span>', unsafe_allow_html=True)
        
        with s3:
            st.markdown('##### Visualization')
            x = ['Power BI', 'Plotly', 'Seaborn', 'GGplot 2','Pandas']
            for i in x:
                st.markdown(
                    f'<span style="background-color:#00C4EB;color: #FFFFFF;padding: 0.5em 1em;position: relative;text-decoration: none;font-weight:bold;cursor: pointer;">{i}</span>', unsafe_allow_html=True)
        s4, s5, s6= st.columns(3)
        with s4:
            st.markdown('##### ML&DL')
            x = ['Sklearn','Keras','TensorFlow', 'Pytorch', 'NumPy', 'Pandas']
            for i in x:
                st.markdown(
                    f'<span style="background-color:#00C4EB;color: #FFFFFF;padding: 0.6em 1em;position: relative;text-decoration: none;font-weight:bold;cursor: pointer;">{i}</span>', unsafe_allow_html=True)
        
        with s5:
            st.markdown('##### AI')
            x = ['NLP', 'Neural Networks']
            for i in x:
                st.markdown(
                    f'<span style="background-color:#00C4EB;color: #FFFFFF;padding: 0.5em 1em;position: relative;text-decoration: none;font-weight:bold;cursor: pointer;">{i}</span>', unsafe_allow_html=True)
        with s6:
            st.markdown('##### WEB APP')
            x = ['Flask', 'Streamlit', 'Heroku']
            for i in x:
                st.markdown(
                    f'<span style="background-color:#00C4EB;color: #FFFFFF;padding: 0.5em 1em;position: relative;text-decoration: none;font-weight:bold;cursor: pointer;">{i}</span>', unsafe_allow_html=True)
              
        st.markdown("<h3 style='text-align: center; color: green; background: #D3D3D3; margin: 3px'>Education</h1>", unsafe_allow_html=True)
        st.markdown("<h4 <span style = color:green;'>Course:</span>Master of Science in Data Science</h4>", unsafe_allow_html=True)
        st.markdown("<h6 <span'>School:</span> ACE-DS, University of Rwanda - Rwanda</h6>", unsafe_allow_html=True)
        st.markdown("<h6 <span'></span>From: Oct-2018 to Dec-2020</h6>", unsafe_allow_html=True)
        st.markdown("<h6 <span'>Dissertation:</span> Tree-based and Logistic Regression Machine Learning Models for Business Success Prediction in Rwanda</h6>", unsafe_allow_html=True)
        st.write(" ")
        

        st.markdown("<h4 <span style = color:green;'>Course:</span>Master of Science in Financial Engineering</h4>", unsafe_allow_html=True)
        st.markdown("<h6 <span'>School:</span>WorldQuant University, Louisiana, USA</h6>", unsafe_allow_html=True)
        st.markdown("<h6 <span'></span>From: April-2019 to Feb-2021</h6>", unsafe_allow_html=True)
        st.markdown("<h6 <span'></span>Dissertation: Comparison of Traditional Time Series techniques and Machine Learning models in Stock Market Price Prediction</h6>", unsafe_allow_html=True)
        st.write(" ")

        st.markdown("<h4 <span style = color:green;'>Course:</span> BSc. Actuarial Science </h4>", unsafe_allow_html=True)
        st.markdown("<h6 <span'>School:</span> Moi University</h6>", unsafe_allow_html=True)
        st.markdown("<h6 <span'></span>From: Jan-2013 to Dec-2016</h6>", unsafe_allow_html=True)
        st.write("Achieved: First Class Honors")

        st.markdown("<h3 style='text-align: center; color: green; background: #D3D3D3; margin: 3px'>Certifications</h1>", unsafe_allow_html=True)
        x = ['AWS Machine Learning  (NANODREE)- Udacity', 'AWS Machine Learning  (NANODREE)- Udacity']        
        for i in x:
                st.markdown(
                    f'<span style="background-color:#00C4EB;color: #FFFFFF;padding: 0.5em 1em;position: margin:5px; relative;text-decoration: none;font-weight:bold;cursor: pointer;">{i}</span>', unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; color: green; background: #D3D3D3; margin: 3px'>Contact Me</h1>", unsafe_allow_html=True)
        st.markdown("<h4> Phone: +254707825181</h4>", unsafe_allow_html=True)
        st.markdown("<h4> Email: francisyego4@gmail.com", unsafe_allow_html=True)
    

if __name__ == '__main__':
    main()
