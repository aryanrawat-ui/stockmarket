import os
import threading
import time
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from fastapi import FastAPI
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

app = FastAPI(title="AI Stock Predictor API")

TREND_THRESHOLD_PCT = 0.3 
MIN_ROWS = 120
FEATURE_COLS = [
    "Close",
    "Volume",
    "MA_5",
    "MA_10",
    "MA_20",
    "EMA_10",
    "EMA_20",
    "MACD",
    "MACD_SIGNAL",
    "RSI",
    "BB_WIDTH",
    "BB_POSITION",
    "RETURN_1D",
    "RETURN_5D",
    "VOLATILITY_10",
    "VOLUME_CHANGE_PCT",
    "HL_SPREAD",
    "OC_SPREAD",
    "CANDLE_BODY_PCT",
    "CLOSE_LAG_1",
    "CLOSE_LAG_2",
    "CLOSE_LAG_3",
    "RETURN_LAG_1",
    "RETURN_LAG_2",
    "RETURN_LAG_3",
    "VOLUME_LAG_1",
    "MA_DIFF",
    "EMA_DIFF",
    "Trend_Strength",
]


def get_stock_data(ticker: str) -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period="2y", interval="1d", auto_adjust=False)

    if df.empty:
        return df

    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    close = df["Close"]

    df["MA_5"] = close.rolling(5).mean()
    df["MA_10"] = close.rolling(10).mean()
    df["MA_20"] = close.rolling(20).mean()
  
    df["EMA_10"] = close.ewm(span=10, adjust=False).mean()
    df["EMA_20"] = close.ewm(span=20, adjust=False).mean()
    df["EMA_12"] = close.ewm(span=12, adjust=False).mean()
    df["EMA_26"] = close.ewm(span=26, adjust=False).mean()

    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["Trend_Strength"] = df["MA_5"] - df["MA_20"]
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    df["RSI"] = 100 - (100 / (1 + rs))

    bb_mid = close.rolling(20).mean()
    bb_std = close.rolling(20).std()
    df["BB_UPPER"] = bb_mid + 2 * bb_std
    df["BB_LOWER"] = bb_mid - 2 * bb_std
    df["BB_WIDTH"] = df["BB_UPPER"] - df["BB_LOWER"]
    df["BB_POSITION"] = (close - df["BB_LOWER"]) / (df["BB_WIDTH"] + 1e-9)

    df["RETURN_1D"] = close.pct_change() * 100
    df["RETURN_5D"] = close.pct_change(5) * 100
    df["VOLATILITY_10"] = df["RETURN_1D"].rolling(10).std()

    df["VOLUME_CHANGE_PCT"] = df["Volume"].pct_change() * 100
    df["HL_SPREAD"] = df["High"] - df["Low"]
    df["OC_SPREAD"] = df["Close"] - df["Open"]
    df["CANDLE_BODY_PCT"] = (df["Close"] - df["Open"]) / (df["Open"] + 1e-9) * 100

    df["CLOSE_LAG_1"] = close.shift(1)
    df["CLOSE_LAG_2"] = close.shift(2)
    df["CLOSE_LAG_3"] = close.shift(3)

    df["RETURN_LAG_1"] = df["RETURN_1D"].shift(1)
    df["RETURN_LAG_2"] = df["RETURN_1D"].shift(2)
    df["RETURN_LAG_3"] = df["RETURN_1D"].shift(3)

    df["VOLUME_LAG_1"] = df["Volume"].shift(1)
    df["MA_DIFF"] = df["MA_5"] - df["MA_10"]
    df["EMA_DIFF"] = df["EMA_10"] - df["EMA_20"]

    df = df.replace([np.inf, -np.inf], np.nan)
    return df


def create_targets(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    next_close = df["Close"].shift(-1)
    df["TARGET_PRICE"] = next_close
    df["NEXT_RETURN_PCT"] = ((next_close - df["Close"]) / df["Close"]) * 100

    df["TARGET_TREND"] = (df["NEXT_RETURN_PCT"] > TREND_THRESHOLD_PCT).astype(int)

    df = df.dropna().copy()
    return df


def train_and_evaluate(df: pd.DataFrame):
    X = df[FEATURE_COLS].copy()
    y_price = df["TARGET_PRICE"].copy()
    y_trend = df["TARGET_TREND"].copy()

    split = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    yp_train, yp_test = y_price.iloc[:split], y_price.iloc[split:]
    yt_train, yt_test = y_trend.iloc[:split], y_trend.iloc[split:]

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    price_model = LinearRegression()
    price_model.fit(X_train_sc, yp_train)
    price_preds = price_model.predict(X_test_sc)

    mae = mean_absolute_error(yp_test, price_preds)
    r2 = r2_score(yp_test, price_preds)

    trend_model = LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        C=0.5,
        solver="lbfgs"
    )
    trend_model.fit(X_train_sc, yt_train)
    trend_preds = trend_model.predict(X_test_sc)
    trend_acc = accuracy_score(yt_test, trend_preds)

    return price_model, trend_model, scaler, mae, r2, trend_acc


def make_decision(trend: int, predicted_price: float, current_price: float) -> str:
    up_buffer = current_price * 1.001
    down_buffer = current_price * 0.999

    if trend == 1 and predicted_price > up_buffer:
        return "BUY"
    elif trend == 0 and predicted_price < down_buffer:
        return "SELL"
    return "HOLD"


def self_ping():
    url = os.getenv("SELF_PING_URL")
    if not url:
        return

    while True:
        try:
            requests.get(url, timeout=10)
            print("Self ping sent")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(300)


if os.getenv("ENABLE_SELF_PING") == "1":
    threading.Thread(target=self_ping, daemon=True).start()


@app.get("/")
def home():
    return {"message": "Stock Prediction API is running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/predict")
def predict(ticker: str):
    try:
        raw_df = get_stock_data(ticker)

        if raw_df.empty:
            return {"error": f"No data found for '{ticker}'"}

        if len(raw_df) < MIN_ROWS:
            return {"error": f"Not enough historical data for '{ticker}'. Try a larger ticker or a more liquid stock."}

        feature_df = add_features(raw_df)
        model_df = create_targets(feature_df)

        model_df = model_df.dropna(subset=FEATURE_COLS + ["TARGET_PRICE", "TARGET_TREND"]).copy()

        if len(model_df) < MIN_ROWS // 2:
            return {"error": "Not enough usable rows after feature engineering. Try a ticker with more data."}

        price_model, trend_model, scaler, mae, r2, trend_acc = train_and_evaluate(model_df)

        latest_features = feature_df[FEATURE_COLS].dropna().iloc[[-1]]
        if latest_features.empty:
            return {"error": "Could not prepare the latest feature row."}

        latest_sc = scaler.transform(latest_features)

        predicted_price = float(price_model.predict(latest_sc)[0])
        trend = int(trend_model.predict(latest_sc)[0])
        trend_prob_up = float(trend_model.predict_proba(latest_sc)[0][1])

        current_price = float(feature_df["Close"].dropna().iloc[-1])
        decision = make_decision(trend, predicted_price, current_price)

        return {
            "stock": ticker,
            "current_price": round(current_price, 2),
            "predicted_price": round(predicted_price, 2),
            "predicted_change_pct": round(((predicted_price - current_price) / current_price) * 100, 2),
            "trend": trend,
            "trend_probability_up": round(trend_prob_up, 4),
            "decision": decision,
            "model_accuracy": {
                "trend_accuracy_pct": round(trend_acc * 100, 2),
                "price_mae": round(mae, 2),
                "price_r2_score": round(r2, 4),
            },
        }

    except Exception as e:
        return {"error": str(e)}
