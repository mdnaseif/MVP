import streamlit as st
import requests
from prophet.serialize import model_from_json
import pandas as pd
from streamlit_lottie import st_lottie
from pathlib import Path
import streamlit_authenticator as stauth
from datetime import datetime, timedelta
import time


# ------ MODEL PROCESSING -----------
st.set_page_config(page_title="SuitAi - Assin!", page_icon=":tada:", layout="wide")


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


setDate = datetime.date(datetime.now() + timedelta(days=-2))
min_limit = datetime.now() + timedelta(days=-3)
min_limit = datetime.date(min_limit)
max_limit = datetime.now() + timedelta(days=+3)
max_limit = datetime.date(max_limit)

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


# ------ HEADER -----------


with st.container():
    st.title("Suit Ai 	:cactus:")
    st.subheader("Your Business is more Intilligent with AI :white_check_mark:")
    st.write("[Our Website](https://suitai.wuiltweb.com/)")
    st.write(
        "Hi Please note that this is a beta version for  testing the product we know its (slow-sucks)"
    )


def result():
    d = st.date_input(
        "Please choose a date to forecast",
        setDate,
        min_limit,
        max_limit,
        format="YYYY-MM-DD",
    )
    if d != setDate:
        with st.empty():
            for seconds in range(7):
                if seconds == 0:
                    st_lottie(lottie1, height=200, key="loading")
                time.sleep(1)
            for seconds in range(3):
                if seconds == 0:
                    st_lottie(lottie2, height=200, key="done")
                time.sleep(1)

            # st.warning(' This is a warning', icon="⚠️")
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

            st.metric(
                label="Inshallah",
                value=f"{only_y} - {only_u} Pieces",
                delta=f"{pers} pc",
            )


with st.container():
    st.write("---")
    st.title("Welcome Assin Cafe :maple_leaf:!")
    choosenItem = st.selectbox(
        "please chose the item to forecast",
        ["Choose Item", "Iced Tea", "Yousfi", "Cascara", "Cold Brew", "Brew Tea"],
    )

    if choosenItem == "Brew Tea":
        with open("بروتي-.json", "r") as fin:
            final_model = model_from_json(fin.read())
        result()

    if choosenItem == "Cold Brew":
        with open("كولد برو-.json", "r") as fin:
            final_model = model_from_json(fin.read())
        result()

    if choosenItem == "Iced Tea":
        with open("شاي مثلج - توت ورمان-.json", "r") as fin:
            final_model = model_from_json(fin.read())
        result()

    if choosenItem == "Yousfi":
        with open("شاي مثلج - يوسفي-.json", "r") as fin:
            final_model = model_from_json(fin.read())
        result()

    if choosenItem == "Cascara":
        with open("كاسكارا-.json", "r") as fin:
            final_model = model_from_json(fin.read())
        result()


# ----------------- Contact Form ------------

st.write("---")
st.title("Contact Us :male-technologist:")
st.markdown(contact_form, unsafe_allow_html=True)
read_css("style/style.css")
