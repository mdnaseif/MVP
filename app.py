import streamlit as st
import datetime
import requests
from prophet.serialize import model_from_json
import pandas as pd
from streamlit_lottie import st_lottie
from pathlib import Path
import streamlit_authenticator as stauth

# ------ MODEL PROCESSING -----------


def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie = load_lottie(
    "https://lottie.host/3851bc3d-8d2f-4e77-9a25-ba4ee6ae33a4/rpjbRrXp7d.json"
)


today = datetime.datetime.now()
next_day = today.day + 2
month = today.month
min_limit = datetime.date(2023, 7, 20)
max_limit = datetime.date(2023, month, next_day)

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
st.set_page_config(page_title="SuitAi - Assin!", page_icon=":tada:", layout="wide")


with st.container():
    st.title("Suit Ai 	:cactus:")
    st.subheader("Your Business is more Intilligent with AI :white_check_mark:")
    st.write("[Our Website](https://suitai.wuiltweb.com/)")
    st.write(
        "Hi Please note that this is a beta version for  testing the product we know its (slow-sucks)"
    )


with st.container():
    st.write("---")
    l_col, r_col = st.columns(2)
    with l_col:
        st.title("Welcome Assin Cafe :maple_leaf:!")
        choosenItem = st.selectbox(
            "please chose the item to forecast",
            ["Iced Tea", "Yousfi", "Cascara", "Cold Brew", "Brew Tea"],
        )
        if choosenItem == "Brew Tea":
            with open("بروتي-.json", "r") as fin:
                final_model = model_from_json(fin.read())
            d = st.date_input(
                "Please choose a date to forecast",
                today,
                min_limit,
                max_limit,
                format="YYYY-MM-DD",
            )
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
            st.metric(
                label="Inshallah", value=f"{only_y} - {only_u} Pieces", delta=" 1.1% "
            )

        if choosenItem == "Cold Brew":
            with open("كولد برو-.json", "r") as fin:
                final_model = model_from_json(fin.read())
            d = st.date_input(
                "Please choose a date to forecast",
                today,
                min_limit,
                max_limit,
                format="YYYY-MM-DD",
            )
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
            st.metric(
                label="Inshallah", value=f"{only_y} - {only_u} Pieces", delta=" 1.1% "
            )

        if choosenItem == "Iced Tea":
            with open("شاي مثلج - توت ورمان-.json", "r") as fin:
                final_model = model_from_json(fin.read())
            d = st.date_input(
                "Please choose a date to forecast",
                today,
                min_limit,
                max_limit,
                format="YYYY-MM-DD",
            )
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
            st.metric(
                label="Inshallah", value=f"{only_y} - {only_u} Pieces", delta=" 1.1% "
            )

        if choosenItem == "Yousfi":
            with open("شاي مثلج - يوسفي-.json", "r") as fin:
                final_model = model_from_json(fin.read())
            d = st.date_input(
                "Please choose a date to forecast",
                today,
                min_limit,
                max_limit,
                format="YYYY-MM-DD",
            )
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
            st.metric(
                label="Inshallah", value=f"{only_y} - {only_u} Pieces", delta=" 1.1% "
            )

        if choosenItem == "Cascara":
            with open("كاسكارا-.json", "r") as fin:
                final_model = model_from_json(fin.read())
            d = st.date_input(
                "Please choose a date to forecast",
                today,
                min_limit,
                max_limit,
                format="YYYY-MM-DD",
            )
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
            st.metric(
                label="Inshallah", value=f"{only_y} - {only_u} Pieces", delta=" 1.1% "
            )

    with r_col:
        st_lottie(lottie, height=400, key="robot")

# ----------------- Contact Form ------------

st.write("---")
st.title("Contact Us :male-technologist:")
st.markdown(contact_form, unsafe_allow_html=True)
read_css("style/style.css")
