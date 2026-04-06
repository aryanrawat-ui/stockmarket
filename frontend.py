import streamlit as st
import requests
import yfinance as yf

API_URL = "https://stockmarketprediction-r270.onrender.com/predict"

# 🔹 Page config
st.set_page_config(page_title="AI Stock Predictor", layout="wide")

# 🔹 HEADER
st.markdown(
    """
    <h1 style='text-align: center;'>📈 AI Stock Prediction Dashboard</h1>
    <p style='text-align: center; color: grey;'>Built by Aryan Rawat!</p>
    """,
    unsafe_allow_html=True
)

st.divider()

# 🔹 SIDEBAR (branding + options)
st.sidebar.title("⚙️ Options")
st.sidebar.write("Select or enter a stock")

popular_stocks = ["AAPL", "TSLA", "TCS.NS", "RELIANCE.NS"]
ticker = st.sidebar.selectbox("Popular Stocks", popular_stocks)

custom_ticker = st.text_input("Or Enter Custom Ticker")

if custom_ticker:
    ticker = custom_ticker

# 🔹 BUTTON
if st.button("🔮 Predict"):

    if ticker:

        col1, col2 = st.columns([2, 1])

        # 📊 CHART
        with col1:
            st.subheader("📊 Stock Price (1 Month)")

            try:
                data = yf.Ticker(ticker).history(period="1mo")
                st.line_chart(data["Close"])
            except:
                st.warning("Chart not available")

        # 🤖 PREDICTION
        with col2:
            st.subheader("🤖 AI Prediction")

            with st.spinner("Analyzing market trends..."):
                try:
                    res = requests.get(API_URL, params={"ticker": ticker})
                    data = res.json()

                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.metric("💰 Current Price", f"₹{data['current_price']}")
                        st.metric("🔮 Predicted Price", f"₹{data['predicted_price']}")

                        trend = "📈 UP" if data["trend"] == 1 else "📉 DOWN"
                        st.write(f"**Trend:** {trend}")

                        decision = data["decision"]

                        if decision == "BUY":
                            st.success("💰 BUY SIGNAL")
                        elif decision == "SELL":
                            st.error("📉 SELL SIGNAL")
                        else:
                            st.warning("⏳ HOLD")

                except Exception as e:
                    st.error(str(e))

    else:
        st.warning("Please enter a stock ticker!")

st.divider()

st.markdown(
    """
    <p style='text-align: center; color: grey;'>
    © 2026 Aryan Rawat | AI Stock Predictor
    </p>
    """,
    unsafe_allow_html=True
)
