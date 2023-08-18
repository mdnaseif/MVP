import streamlit as st
import requests
from prophet.serialize import model_from_json
import pandas as pd
import json
from streamlit_lottie import st_lottie
from datetime import datetime, timedelta
import time
import plotly.graph_objs as go
from pymongo import MongoClient
import plotly.express as px


# ------ DB CONFIG -----------
client = MongoClient("mongodb+srv://MDNASEIF:1928qpwO@mlops.la0z4v1.mongodb.net/?retryWrites=true&w=majority")
db = client.assin
collection = db["models"]


# ------ WEB SITTING -----------
st.set_page_config(page_title="SuitAi - Assin!", page_icon=":cactus:", layout="wide")


# ------ Graphic -----------
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie1 = load_lottie(
    "https://lottie.host/0fe72a0d-19b4-4cf1-b805-81c1436960ef/pObPi3K16F.json"
)
lottie2 = load_lottie(
    "https://lottie.host/bc11374a-eb53-4a24-9204-78a3e7ff54c0/50dcPFMMSl.json"
)

# ------ Date sitting -----------
setDate = datetime.date(datetime.now() + timedelta(days=-2))
min_limit = datetime.now() + timedelta(days=-3)
min_limit = datetime.date(min_limit)
max_limit = datetime.now() + timedelta(days=+3)
max_limit = datetime.date(max_limit)

# ------ Form -----------
contact_form = """
<form action="https://formsubmit.co/naseif2002@gmail.com" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder="Your Name" required>
    <input type="email" name="email" placeholder="Your Email" required>
    <textarea name="message" placeholder="Details of your problem"></textarea>
    <button type="submit">Send</button>
</form>
"""
def read_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ------ BODY -----------


with st.container():
    st.image("SuitAi.png")
    #st.title("Suit Ai 	:cactus:")
    st.title("Your Business is more Intilligent with AI :white_check_mark:")
    st.subheader("[Our Website](https://suitsai.wuiltweb.com/)")
    st.write(
        "Hi Please note that this is a beta version for testing the product we know its (slow-sucks)"
    )

colorList = ["#F4F7ED", "#86EE60", "#2E6E65","2B3752"]
def meangraph(df):
    df = df
    df['ds'] = pd.to_datetime(df['ds'])
    df["weekday"] = df.ds.dt.day_name()
    df = pd.DataFrame({'count' : df.groupby("weekday")["y"].mean()}).reset_index()
    df = df.sort_values(by=['count'])
    df = df.round(0)
    fig = px.bar(df, x='weekday', y='count',
                hover_data=['count'], color='count',color_continuous_scale= 'Aggrnyl',
                labels={'pop':'population of Canada'}, height=400)
    fig.update_layout(
            yaxis_title="Amount",
            xaxis_title="Week Days",
            title="Mean of weekdays for the last 4 weeks",
        )
    return fig

def graph(df,val):
    df["y"] = val["y"]
    fig = go.Figure([
        go.Scatter(
            name="Upper Forecasted",
            x=df['ds'].iloc[-7:],
            y=df['yhat_upper'].iloc[-7:],
            mode='lines+markers',
            marker=dict(color='#86EE60'),
            line=dict(width=3),

        ),
        go.Scatter(
            name="Forecasted",
            x=df['ds'].iloc[-7:],
            y=df['yhat'].iloc[-7:],
            #round(df['yhat'] + ((df['yhat_upper'] - df['yhat']) / 2 )),
            mode='lines+markers',
            line=dict(color="#86EE60",width = 3),
            fillcolor='rgba(134, 238, 96, 0.3)',
            fill='tonexty',),
        go.Scatter(
            name="Actual",
            x=df['ds'].iloc[-7:],
            y=df['y'].iloc[-7:],
            mode='lines+markers',
            line=dict(color="#05BFDB",width = 3),
            fillcolor='rgba(134, 238, 96, 0.3)',
            fill='tonexty',

        ),
        go.Scatter(
            name="Lower Forecasted",
            x=df['ds'].iloc[-7:],
            y=df['yhat_lower'].iloc[-7:],
            mode='lines+markers',
            line=dict(color='#2E6E65',width = 3),
            fillcolor='rgba(134, 238, 96, 0.3)',
            fill='tonexty',

        ),

    ])
    fig.update_layout(
        yaxis_title="Amount",
        xaxis_title="Date",
        title="Performance Over last week",
        hovermode="x"
    )
    
    return fig

def inner_graph(file_name):
        val = pd.read_csv(file_name, encoding="utf-8")
        chart_data = final_model.predict(val)
        chart_data = chart_data[["ds","yhat", "yhat_lower", "yhat_upper"]]
        chart_data = chart_data.round({"yhat": 0, "yhat_lower": 0, "yhat_upper": 0})
        chart_data["ds"] = chart_data["ds"].dt.date
        fig = graph(chart_data,val)
        st.write("##")
        st.plotly_chart(fig, use_container_width=True)
        meanfig = meangraph(val)
        st.write("##")
        st.plotly_chart(meanfig, use_container_width=True)



def reccomendation(d):
        if d.weekday() == 3 or d.weekday() == 4 :
            st.warning('Recommendation: The date you choosed is a weekend please consider choosing the upper limit', icon="✨")
        else:
            st.warning('Recommendation: We noticed That the date you choosed there will be a drop in the sales we recommends you to choose the lower limit', icon="✨")

def result(file_name):
    d = st.date_input(
        "Please choose a date to forecast",
        setDate,
        min_limit,
        max_limit,
        format="YYYY-MM-DD",
    )
    if d != setDate:
        with st.empty():
            for seconds in range(3):
                if seconds == 0:
                    st_lottie(lottie1, height=200, key="loading")
                time.sleep(1)
            for seconds in range(3):
                if seconds == 0:
                    st_lottie(lottie2, height=200, key="done")
                time.sleep(1)

            
            st.write("##")
  
        st.subheader("Any Events? :male-teacher:")
        item = {
            "ds": d,
            "day_of_week": d.weekday(),
            "month": d.month,
            "day_month": d.day,
        }
        df = pd.DataFrame([item.values()], columns=item.keys())
        result = final_model.predict(df)
        result = result[["yhat", "yhat_lower", "yhat_upper"]]
        only_y = result["yhat"].iloc[0]
        only_y = round(only_y)

        only_u = result["yhat_upper"].iloc[0]
        only_u = round(only_u)

        prev = d + timedelta(days=-1)
        prev_item = {
            "ds": prev,
            "day_of_week": prev.weekday(),
            "month": prev.month,
            "day_month": prev.day,
        }
        df1 = pd.DataFrame([prev_item.values()], columns=prev_item.keys())
        result = final_model.predict(df1)
        result = result[["yhat", "yhat_lower", "yhat_upper"]]
        prev_only_u = result["yhat_upper"].iloc[0]
        prev_only_u = round(prev_only_u)

        pers = only_u - prev_only_u

        with st.container():
            choosenEvent = st.selectbox(
                "please choose the The event Type",
                ["Choose Event", "No Event", "Ads", "Offer", "Special Event"],)
            
            if choosenEvent == "Choose Event":
                st.warning('Choosing Type of event will impact the forecasting', icon="⚠️")
            if choosenEvent == "No Event":
                st.write("##")
                st.write("---")
                st.subheader("Your Results!	:medal:")
                st.metric(
                    label="Forecasted Demand",
                    value=f"{only_y} - {only_u} Cups",
                    delta=f"{pers} cups from Yesterday",
                )
                reccomendation(d)
                inner_graph(file_name)

            if choosenEvent == "Ads":
                st.write("##")
                st.write("---")
                st.subheader("Your Results!	:medal:")
                st.metric(
                    label="Forecasted Demand",
                    value=f"{round(only_y+((only_u*1.75)-only_u))} - {round(only_u*1.75)} Cups",
                    delta=f"{pers} cups from Yesterday",
                )
                reccomendation(d)
                inner_graph(file_name)
            if choosenEvent == "Offer":
                st.write("##")
                st.write("---")
                st.subheader("Your Results!	:medal:")
                st.metric(
                    label="Forecasted Demand",
                    value=f"{round(only_y+((only_u*2)-only_u))} - {round(only_u*2)} Cups",
                    delta=f"{pers} cups from Yesterday",
                )
                reccomendation(d)
                inner_graph(file_name)
            if choosenEvent == "Special Event":
                st.write("##")
                st.write("---")
                st.subheader("Your Results!	:medal:")
                st.metric(
                    label="Forecasted Demand",
                    value=f"{round(only_y+((only_u*1.5)-only_u))} - {round(only_u*1.5)} Cups",
                    delta=f"{pers} cups from Yesterday",
                )
                reccomendation(d)
                inner_graph(file_name)
        



yesterday = datetime.now() + timedelta(days=-1)
yesterday = datetime.date(yesterday)
def mongoModel(id):
    model = []
    if collection.count_documents({ "date": str(datetime.date(datetime.now())) }, limit = 1) != 0:
        result = collection.find({"date":str(datetime.date(datetime.now())), "itemId":id})
        pass
    else:
        result = collection.find({"date":str(yesterday), "itemId":id})
    for doc in result:
        model.append(doc)
        model = model[0]
        model = model["model"]
        model = json.dumps(model)
        model = model_from_json(model)
        return model
        


with st.container():
    st.write("---")
    st.title("Welcome Assin Cafe :maple_leaf:!")
    choosenItem = st.selectbox(
        "please chose the item to forecast",
        ["Choose Item", "Iced Tea", "Yousfi", "Cascara", "Cold Brew", "Brew Tea"],
    )
    if choosenItem == "Cascara":
        final_model = mongoModel(6)
        result("كاسكارا-.csv")

    if choosenItem == "Brew Tea":
        final_model = mongoModel(7)
        result("بروتي-.csv")

    if choosenItem == "Iced Tea":
        final_model = mongoModel(8)
        result("شاي مثلج - توت ورمان-.csv")

    if choosenItem == "Yousfi":
        final_model = mongoModel(9)
        result("شاي مثلج - يوسفي-.csv")

    if choosenItem == "Cold Brew":
        final_model = mongoModel(10)
        result("كولد برو-.csv")





# ----------------- Contact Form ------------

st.write("---")
st.title("Contact Us :male-technologist:")
st.markdown(contact_form, unsafe_allow_html=True)
read_css("style/style.css")
