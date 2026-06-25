import streamlit as st
import requests
import yfinance as yf

API_URL = "https://stockmarketprediction-r270.onrender.com/predict"

st.set_page_config(
    page_title="AI Stock Predictor",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0;
}

.sub-title {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.signal-buy {
    background: #1e5631;
    color: white;
    border: 2px solid #28a745;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-top: 20px;
}

.signal-sell {
    background: #7a1f1f;
    color: white;
    border: 2px solid #dc3545;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-top: 20px;
}

.signal-hold {
    background: #7a6618;
    color: white;
    border: 2px solid #ffc107;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
    "<h1 class='main-title'>AI Stock Prediction Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>Built by Aryan Rawat</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------- STOCK SELECTION ----------
popular_stocks = [
    "AAPL",
    "TSLA",
    "GOOGL",
    "MSFT",
    "TCS.NS",
    "RELIANCE.NS",
    "INFY.NS",
    "HDFCBANK.NS"
]

col1, col2 = st.columns(2)

with col1:
    ticker = st.selectbox(
        "Popular Stocks",
        popular_stocks
    )

with col2:
    custom_ticker = st.text_input(
        "Custom Ticker",
        placeholder="AMZN, TATAMOTORS.NS"
    )

if custom_ticker.strip():
    ticker = custom_ticker.strip().upper()

st.write("")

predict_clicked = st.button(
    "Predict",
    use_container_width=True,
    type="primary"
)

# ---------- PREDICTION ----------
if predict_clicked:

    try:
        hist = yf.Ticker(ticker).history(period="1mo")

        st.subheader("Price Chart")

        if hist.empty:
            st.warning("No chart data found.")

        else:
            st.line_chart(
                hist["Close"],
                use_container_width=True
            )

            if len(hist) >= 2:

                last_close = float(hist["Close"].iloc[-1])
                prev_close = float(hist["Close"].iloc[-2])

                change = last_close - prev_close
                change_pct = (change / prev_close) * 100

                m1, m2, m3 = st.columns(3)

                m1.metric(
                    "Last Close",
                    f"₹{last_close:.2f}"
                )

                m2.metric(
                    "Daily Change",
                    f"₹{change:.2f}",
                    f"{change_pct:.2f}%"
                )

                m3.metric(
                    "30-Day High",
                    f"₹{hist['Close'].max():.2f}"
                )

        st.divider()

        with st.spinner("Analyzing market..."):

            response = requests.get(
                API_URL,
                params={"ticker": ticker},
                timeout=60
            )

            data = response.json()

            if "error" in data:
                st.error(data["error"])

            else:

                st.subheader("Prediction")

                p1, p2, p3 = st.columns(3)

                p1.metric(
                    "Current Price",
                    f"₹{data['current_price']}"
                )

                p2.metric(
                    "Predicted Price",
                    f"₹{data['predicted_price']}",
                    f"{data['predicted_change_pct']}%"
                )

                trend = "UP" if data["trend"] == 1 else "DOWN"

                p3.metric(
                    "Trend",
                    trend
                )

                if "trend_probability_up" in data:

                    probability = float(
                        data["trend_probability_up"]
                    )

                    probability = max(0, min(1, probability))

                    st.progress(probability)

                    st.caption(
                        f"Probability of UP: {probability:.2%}"
                    )

                decision = data["decision"]

                if decision == "BUY":
                    st.markdown(
                        "<div class='signal-buy'>BUY SIGNAL</div>",
                        unsafe_allow_html=True
                    )

                elif decision == "SELL":
                    st.markdown(
                        "<div class='signal-sell'>SELL SIGNAL</div>",
                        unsafe_allow_html=True
                    )

                else:
                    st.markdown(
                        "<div class='signal-hold'>HOLD SIGNAL</div>",
                        unsafe_allow_html=True
                    )

                st.divider()

                st.subheader("Model Performance")

                accuracy = data.get("model_accuracy")

                if accuracy:

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "Trend Accuracy",
                        f"{accuracy['trend_accuracy_pct']}%"
                    )

                    c2.metric(
                        "Price MAE",
                        f"₹{accuracy['price_mae']}"
                    )

                    c3.metric(
                        "R² Score",
                        accuracy["price_r2_score"]
                    )

                    r2 = float(accuracy["price_r2_score"])

                    if r2 >= 0.9:
                        st.success("Excellent model fit")

                    elif r2 >= 0.7:
                        st.info("Good model fit")

                    else:
                        st.warning("Weak model fit")

                else:
                    st.warning(
                        "Model accuracy data unavailable."
                    )

    except requests.exceptions.Timeout:
        st.error("Request timed out.")

    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

st.markdown(
    """
    <p style='text-align:center; color:gray;'>
    © 2026 Aryan Rawat | AI Stock Predictor
    </p>
    """,
    unsafe_allow_html=True
)
