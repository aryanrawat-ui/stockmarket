import streamlit as st
import requests
import yfinance as yf
API_URL = "https://stockmarketprediction-r270.onrender.com/predict"
st.set_page_config(page_title="Stock Predictor", layout="wide")
st.title("📈 AI Stock Prediction Dashboard")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TCS.NS, RELIANCE.NS)")
if st.button("Predict"):
    if ticker:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("📊 Stock Chart")
            try:
                data = yf.Ticker(ticker).history(period="1mo")
                st.line_chart(data["Close"])
            except:
                st.warning("Chart not available")
        with col2:
            st.subheader("🤖 Prediction")
            with st.spinner("Analyzing..."):
                try:
                    res = requests.get(API_URL, params={"ticker": ticker})
                    data = res.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.metric("Current Price", f"₹{data['current_price']}")
                        st.metric("Predicted Price", f"₹{data['predicted_price']}")
                        trend = "UP 📈" if data["trend"] == 1 else "DOWN 📉"
                        st.write(f"**Trend:** {trend}")
                        if data["decision"] == "BUY":
                            st.success("💰 BUY")
                        elif data["decision"] == "SELL":
                            st.error("📉 SELL")
                        else:
                            st.warning("⏳ HOLD")
                except Exception as e:
                    st.error(str(e))
    else:
        st.warning("Enter a stock ticker first!")
