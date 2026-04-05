from fastapi import FastAPI
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
app = FastAPI()


def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="30d", interval="1d")
    df = df[["Close"]]
    return df


def create_targets(df):
    df["target_price"] = df["Close"].shift(-1)
    df["target_trend"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    df = df.dropna()
    return df


def train_linear_model(df):
    X = df[["Close"]]
    y = df["target_price"]

    model = LinearRegression()
    model.fit(X, y)

    return model

def train_logistic_model(df):
    X = df[["Close"]]
    y = df["target_trend"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    return model

def predict_price(model, df):
    latest = df[["Close"]].iloc[-1]
    latest = np.array(latest).reshape(1, -1)

    prediction = model.predict(latest)

    return prediction[0]

def predict_trend(model, df):
    latest = df[["Close"]].iloc[-1]
    latest = np.array(latest).reshape(1, -1)

    prediction = model.predict(latest)

    return prediction[0]


def make_decision(trend, predicted_price, current_price):
    if trend == 1 and predicted_price > current_price:
        return "BUY"
    elif trend == 0 and predicted_price < current_price:
        return "SELL"
    else:
        return "HOLD"


@app.get("/")
def home():
    return {"message": "Stock Prediction API is running 🚀"}

@app.get("/predict")
def predict(ticker: str):

    try:
        # Step 1: Get data
        df = get_stock_data(ticker)

        # Step 2: Create targets
        df = create_targets(df)

        # Step 3: Train models
        linear_model = train_linear_model(df)
        logistic_model = train_logistic_model(df)

        # Step 4: Predictions
        predicted_price = predict_price(linear_model, df)
        trend = predict_trend(logistic_model, df)

        # Step 5: Current price
        current_price = df["Close"].iloc[-1]

        # Step 6: Decision
        decision = make_decision(trend, predicted_price, current_price)

        return {
            "stock": ticker,
            "current_price": float(current_price),
            "predicted_price": float(predicted_price),
            "trend": int(trend),
            "decision": decision
        }

    except Exception as e:
        return {"error": str(e)}