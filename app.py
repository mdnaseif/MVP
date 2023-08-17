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



def graph(df,val):
    df["y"] = val["y"]
    fig = go.Figure([
        go.Scatter(
            name="Upper Forecasted",
            x=df['ds'],
            y=df['yhat_upper'],
            mode='lines+markers',
            marker=dict(color='#2E6E65'),
            line=dict(width=3),

        ),
        go.Scatter(
            name="Lower Forecasted",
            x=df['ds'],
            y=df['yhat'],
            #round(df['yhat'] + ((df['yhat_upper'] - df['yhat']) / 2 )),
            mode='lines+markers',
            line=dict(color="#86EE60",width = 3),
            fillcolor='rgba(134, 238, 96, 0.3)',
            fill='tonexty',
        ),
        go.Scatter(
            name="Actual",
            x=df['ds'],
            y=df['y'],
            mode='lines+markers',
            line=dict(color="#05BFDB",width = 3),
            fillcolor='rgba(5, 191, 219, 0.3)',
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
        st.subheader("Here is the result	:medal:")
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
            agree = st.checkbox('There is AD')
            if agree:
                st.metric(
                    label="Forecasted Demand",
                    value=f"{round(only_y+((only_u*1.5)-only_u))} - {round(only_u*1.5)} Cups",
                    delta=f"{pers} cups from Yesterday",
                )
            else:
                st.metric(
                    label="Forecasted Demand",
                    value=f"{only_y} - {only_u} Cups",
                    delta=f"{pers} cups from Yesterday",
                )

        if d.weekday() == 3 or d.weekday() == 4 :
            st.warning('Example: The date you choosed is a weekend please consider choosing the upper limit', icon="⚠️")
        else:
            st.warning('Example: We noticed That the date you choosed there will be a drop in the sales we reccomend you to choose the lower limit', icon="⚠️")


        val = pd.read_csv(file_name, encoding="utf-8")
        chart_data = final_model.predict(val)
        chart_data = chart_data[["ds","yhat", "yhat_lower", "yhat_upper"]]
        chart_data = chart_data.round({"yhat": 0, "yhat_lower": 0, "yhat_upper": 0})
        chart_data["ds"] = chart_data["ds"].dt.date
        fig = graph(chart_data,val)
        st.write("##")
        st.plotly_chart(fig, use_container_width=True)




def mongoModel(id):
    model = []
    result = collection.find({"date":str(datetime.date(datetime.now())), "itemId":id})
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
        final_model = mongoModel(1)
        result("كاسكارا-.csv")

    if choosenItem == "Brew Tea":
        final_model = mongoModel(2)
        result("بروتي-.csv")

    if choosenItem == "Iced Tea":
        final_model = mongoModel(3)
        result("شاي مثلج - توت ورمان-.csv")

    if choosenItem == "Yousfi":
        final_model = mongoModel(4)
        result("شاي مثلج - يوسفي-.csv")

    if choosenItem == "Cold Brew":
        final_model = mongoModel(5)
        result("كولد برو-.csv")





# ----------------- Contact Form ------------

st.write("---")
st.title("Contact Us :male-technologist:")
st.markdown(contact_form, unsafe_allow_html=True)
read_css("style/style.css")
