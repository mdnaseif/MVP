import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid
from adtk.detector import QuantileAD
import matplotlib.pyplot as plt
import warnings
import random
from prophet.serialize import model_to_json, model_from_json

warnings.filterwarnings("ignore")
plt.style.use("ggplot")
plt.style.use("fivethirtyeight")

from prophet import Prophet
from datetime import timedelta


def mean_absolute_percentage_error(y_true, y_pred):
    """Calculates MAPE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


df_original = pd.read_csv("assin2023-07-30.csv", encoding="utf-8")


def data_processing(df, item_name: str):
    # only these 4 columns
    df = df[["Date", "Item", "Variant", "Quantity"]]
    # fill Variant null with empty string
    df = df.fillna("")
    # Using + operator to combine two columns
    df["item"] = df["Item"].astype(str) + "-" + df["Variant"]
    df = df.drop(["Item", "Variant"], axis=1)
    # sort data
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y %H:%M")
    df = df.sort_values(by="Date")
    df = df.reset_index(drop=True)

    # consider the day start from 18:00
    df["Date"] = pd.to_datetime(df["Date"])
    df["Date"] = df["Date"].apply(
        lambda x: x + timedelta(days=-1) if x.hour < 18 else x
    )

    # make df from each item
    teams = df["item"].unique()
    df_dict = {}
    j = 0
    for i in teams:
        df_f = df[df["item"] == i]
        df_dict[j] = df_f
        j += 1

    for i in range(len(teams)):
        df_dict[teams[i]] = df_dict.pop(i)

    teams = pd.DataFrame(teams)
    item_name = item_name
    df_item = df_dict[item_name]
    df = (
        df_item.groupby([pd.Grouper(key="Date", freq="D")])["Quantity"]
        .sum()
        .reset_index()
    )
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")
    df.rename(columns={"Quantity": "amount"}, inplace=True)
    # df = df[:-1]
    # oulier removing
    df = df.rename(columns={"Date": "ds", "amount": "y"})
    data = df.set_index("ds")
    data["y"] = data["y"]
    # Quantile
    trech_d = QuantileAD(low=0.1, high=0.999)
    anom = trech_d.fit_detect(data)
    what = list(anom["y"])  # type: ignore
    df["anomly"] = what
    df1 = df.loc[df["anomly"] == False]
    df1.drop(["anomly"], axis=1, inplace=True)

    return df1


items = [
    "كاسكارا-",
    "بروتي-",
    "شاي مثلج - توت ورمان-",
    "شاي مثلج - يوسفي-",
    "كولد برو-",
]

for item in items:
    df = data_processing(df_original, item)

    def add_date(dff):
        dff["day_of_week"] = dff.ds.dt.weekday
        dff["month"] = dff.ds.dt.month
        dff["day_month"] = dff.ds.dt.day
        li = []
        for i in dff["day_of_week"]:
            if i < 5 and i > 2:
                li.append(1)
            else:
                li.append(0)

        # dff["IsWeekend"] = li
        return dff

    df = add_date(df)

    def split_data(df):
        end_train = "2023-07-23"
        global end_val
        end_val = "2023-07-30"
        mask1 = df["ds"] <= end_train  # train
        mask2 = df[(df["ds"] > end_train) & (df["ds"] <= end_val)]
        mask3 = df["ds"] > end_val  # test
        X_tr = df.loc[mask1]
        X_val = mask2
        X_tst = df.loc[mask3]

        return X_tr, X_val, X_tst

    X_tr, X_val, X_tst = split_data(df)

    params_grid = {
        "seasonality_mode": ("multiplicative", "additive"),
        "seasonality_prior_scale": [0.01, 0.1, 1, 5],
        "changepoint_prior_scale": [0.01, 0.1, 0.5, 0.8, 10],
    }
    grid = ParameterGrid(params_grid)

    model_parameters = pd.DataFrame(columns=["MAPE", "Parameters"])
    for p in grid:
        test = pd.DataFrame()
        print(p)
        random.seed(0)
        train_model = Prophet(
            changepoint_prior_scale=p["changepoint_prior_scale"],
            seasonality_prior_scale=p["seasonality_prior_scale"],
            seasonality_mode=p["seasonality_mode"],
            daily_seasonality=True,  # type: ignore
            interval_width=0.70,
        )
        train_model.add_regressor("day_of_week", mode="additive")
        train_model.add_regressor("month", mode="multiplicative")
        train_model.add_regressor("day_month", mode="additive")
        train_model.fit(X_tr)
        # train_forecast = train_model.make_future_dataframe(periods=8, freq='D',include_history = False)
        train_forecast = train_model.predict(X_val)
        test = train_forecast[["ds", "yhat", "day_month", "day_of_week", "month"]]
        Actual = X_val
        MAPE = mean_absolute_percentage_error(Actual["y"], abs(test["yhat"]))
        print(
            "Mean Absolute Percentage Error(MAPE)------------------------------------",
            MAPE,
        )
        model_parameters = model_parameters._append({"MAPE": MAPE, "Parameters": p}, ignore_index=True)  # type: ignore

    parameters = model_parameters.sort_values(by=["MAPE"])
    parameters = parameters.reset_index(drop=True)
    x = parameters["Parameters"][0].values()
    x = list(x)

    X_tr_val = df[(df["ds"] <= end_val) & (df["ds"] <= end_val)]
    # Setup and train model with holidays
    final_model = Prophet(
        changepoint_prior_scale=x[0],
        seasonality_prior_scale=x[2],
        seasonality_mode=x[1],
        daily_seasonality=True,  # type: ignore
        interval_width=0.70,
    )
    final_model.add_regressor("day_of_week", mode="additive")
    final_model.add_regressor("month", mode="multiplicative")
    final_model.add_regressor("day_month", mode="additive")

    final_model.fit(X_tr_val)

    # Python
    from prophet.serialize import model_to_json, model_from_json

    file_name = item

    with open(f"{file_name}.json", "w") as fout:
        fout.write(model_to_json(final_model))  # Save model
        print("model has been saved")
    # with open('model.json', 'r') as fin:
    #    final_model = model_from_json(fin.read())  # Load model
