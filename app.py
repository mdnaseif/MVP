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


def meangraph(df):
    df = df
    df['ds'] = pd.to_datetime(df['ds'])
    df["weekday"] = df.ds.dt.day_name()
    df = pd.DataFrame({'count' : df.groupby("weekday")["y"].mean()}).reset_index()
    df = df.sort_values(by=['count'])
    df = df.round(0)
    fig = px.bar(df, x='weekday', y='count',
                hover_data=['count'], color='count',color_continuous_scale= 'Aggrnyl',
                labels={'pop':'population of Canada'})
    fig.update_layout(
            yaxis_title="Amount",
            xaxis_title="Week Days",
            title="Mean of weekdays for the last 4 weeks",
        )
    return fig

def graph(df,val):
    df['ds'] = pd.to_datetime(df['ds'])
    df["weekday"] = df.ds.dt.day_name()
    fig = go.Figure([
        go.Scatter(
            name="Upper Forecasted",
            x=df["weekday"].iloc[-7:],
            y=df['yhat_upper'].iloc[-7:],
            mode='lines+markers',
            marker=dict(color='#2E6E65'),
            line=dict(width=3),

        ),
        go.Scatter(
            name="Forecasted",
            x=df["weekday"].iloc[-7:],
            y=df['yhat'].iloc[-7:],
            #round(df['yhat'] + ((df['yhat_upper'] - df['yhat']) / 2 )),
            mode='lines+markers',
            line=dict(color="#86EE60",width = 3),
            fillcolor='rgba(134, 238, 96, 0.3)',
            fill='tonexty',),
        go.Scatter(
            name="Actual",
            x=df["weekday"].iloc[-7:],
            y=val['y'].iloc[-7:],
            mode='lines+markers',
            line=dict(color="#05BFDB",width = 3),
            fillcolor='rgba(134, 238, 96, 0.3)',
            fill='tonexty',

        ),
        go.Scatter(
            name="Lower Forecasted",
            x=df["weekday"].iloc[-7:],
            y=df['yhat_lower'].iloc[-7:],
            mode='lines+markers',
            line=dict(color='#2E6E65',width = 3),
            fillcolor='rgba(134, 238, 96, 0.3)',
            fill='tonexty',

        ),

    ])
    startweek= str(datetime.date(df["ds"].iloc[-1]))
    endweek= str(datetime.date(df["ds"].iloc[-7]))
    fig.update_layout(
        yaxis_title="Amount",
        xaxis_title="Date",
        title=f"Performance Over last week, From ({endweek}) until ({startweek}) ",
        hovermode="x"
    )
    
    return fig

def inner_graph(data):
        val = data
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


def predict(df):
        result = final_model.predict(df)
        result = result[["yhat", "yhat_lower", "yhat_upper"]]
        yhat = result["yhat"].iloc[0]
        yhat = round(yhat)

        y_upper = result["yhat_upper"].iloc[0]
        y_upper = round(y_upper)

        return yhat, y_upper
        """prev = d + timedelta(days=-1)
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

        pers = only_u - prev_only_u"""

# ------ Date sitting -----------
setDate = datetime.date(datetime.now() + timedelta(days=-2))
min_limit = datetime.now() + timedelta(days=-3)
min_limit = datetime.date(min_limit)
max_limit = datetime.now() + timedelta(days=+3)
max_limit = datetime.date(max_limit)

def proccess(data):
    d = st.date_input(
        "Please choose a date to forecast",
        setDate,
        min_limit,
        max_limit,
        format="YYYY-MM-DD",
    )
    if d != setDate:
        isschool = 0
        st.subheader("Any Events In the date you choosed? :male-teacher:")
        item = {
            "ds": d,
            "day_of_week": d.weekday(),
            "month": d.month,
            "day_month": d.day,
            "isIncrease": 0,
            "isschool": isschool,
            "isDrop": 0,
            "Ads": 0 
        }
        df = pd.DataFrame([item.values()], columns=item.keys())
        startschool = datetime.date(datetime.strptime("2023-08-20",'%Y-%m-%d'))
        endchool = datetime.date(datetime.strptime("2023-06-22",'%Y-%m-%d'))
        df['isschool'] = df['ds'].apply(lambda x: 1 if x >= startschool or x < endchool else 0)

        with st.container():
            choosenEvent = st.selectbox(
                "please choose the The event Type",
                ["Choose Event", "Normal day without events", "We made a promotion for the item",  "Will be a Special Event","A partial close (Drop in sales)"],)
            
            if choosenEvent == "Choose Event":
                st.warning('Choosing Type of event will impact the forecasting', icon="⚠️")
            if choosenEvent != "Choose Event":
                with st.empty():
                    for seconds in range(3):
                        if seconds == 0:
                            st_lottie(lottie1, height=200, key="loading")
                        time.sleep(1)
                    for seconds in range(3):
                        if seconds == 0:
                            st_lottie(lottie2, height=200, key="done")
                        time.sleep(1)
                    st.write("")
                if choosenEvent == "Normal day without events":
                    df["isIncrease"].iloc[0] = 0
                    yhat, y_upper = predict(df)
                    st.write("##")
                    st.write("---")
                    st.subheader("Your Results!	:medal:")
                    st.metric(
                        label="Forecasted Demand",
                        value=f"{yhat} - {y_upper} Cups",
                        delta=f"{0} cups from Yesterday",
                    )
                    reccomendation(d)
                    inner_graph(data)
                

                if choosenEvent == "We made a promotion for the item":
                    df["Ads"].iloc[0] = 1
                    yhat, y_upper = predict(df)
                    st.write("##")
                    st.write("---")
                    st.subheader("Your Results!	:medal:")
                    st.metric(
                        label="Forecasted Demand",
                        value=f"{yhat} - {y_upper} Cups",
                        delta=f"{0} cups from Yesterday",
                    )
                    reccomendation(d)
                    inner_graph(data)
                if choosenEvent == "Will be a Special Event":
                    df["isIncrease"].iloc[0] = 1
                    yhat, y_upper = predict(df)
                    st.write("##")
                    st.write("---")
                    st.subheader("Your Results!	:medal:")
                    st.metric(
                        label="Forecasted Demand",
                        value=f"{yhat} - {y_upper} Cups",
                        delta=f"{0} cups from Yesterday",
                    )
                    reccomendation(d)
                    inner_graph(data)

                if choosenEvent == "A partial close (Drop in sales)":
                    df["isDrop"].iloc[0] = 1
                    yhat, y_upper = predict(df)
                    st.write("##")
                    st.write("---")
                    st.subheader("Your Results!	:medal:")
                    st.metric(
                        label="Forecasted Demand",
                        value=f"{yhat} - {y_upper} Cups",
                        delta=f"{0} cups from Yesterday",
                    )
                    reccomendation(d)
                    inner_graph(data)

        
        
        




#---------------- DataBase -------------------------
yesterday = datetime.now() + timedelta(days=-1)
yesterday = datetime.date(yesterday)
def mongoModel(id):
    model = []
    result= ""
    if collection.count_documents({ "date": str(datetime.date(datetime.now())), "type":"model" }, limit = 1) != 0:
        result = collection.find({"date":str(datetime.date(datetime.now())), "itemId":id , "type":"model"})
        pass
    else:
        result = collection.find({"date":str(yesterday), "itemId":id, "type":"model"})
    for doc in result:
        model.append(doc)
        model = model[0]
        model = model["model"]
        model = json.loads(model)
        model = json.dumps(model)
        model = model_from_json(model)
        return model
    
def mongodata(id):
    data = []
    docs = ""
    if collection.count_documents({ "date": str(datetime.date(datetime.now())), "itemId":id ,"type":"data" }, limit = 1) != 0:
        docs = collection.find({"date":str(datetime.date(datetime.now())), "itemId":id , "type":"data"})
        pass
    else:
        docs = collection.find({"date":str(yesterday), "itemId":id , "type":"data"})
    for doc in docs:
        data.append(doc)
        data = data[0]
        data = data["data"]
        df = pd.read_json(data)
        df['ds']= pd.to_datetime(df['ds'])
        return df    


with st.container():
    st.write("---")
    st.title("Welcome Assin Cafe :maple_leaf:!")
    choosenItem = st.selectbox(
        "please choose the item to forecast",
        ["Choose Item", "Iced Tea", "Yousfi", "Cascara", "Cold Brew", "Brew Tea"],
    )
    if choosenItem == "Cascara":
        final_model = mongoModel(1)
        data = mongodata(1)
        proccess(data)

    if choosenItem == "Brew Tea":
        final_model = mongoModel(2)
        data = mongodata(2)
        proccess(data) 

    if choosenItem == "Iced Tea":
        final_model = mongoModel(3)
        data = mongodata(3)
        proccess(data)

    if choosenItem == "Yousfi":
        final_model = mongoModel(4)
        data = mongodata(4)
        proccess(data)

    if choosenItem == "Cold Brew":
        final_model = mongoModel(5)
        data = mongodata(5)
        proccess(data)




# ----------------- Contact Form ------------

st.write("---")
st.title("Contact Us :male-technologist:")
st.markdown(contact_form, unsafe_allow_html=True)
read_css("style/style.css")
