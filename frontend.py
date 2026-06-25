import streamlit as st
import requests
import yfinance as yf

API_URL = "https://stockmarketprediction-r270.onrender.com/predict"

st.set_page_config(
    page_title="AI Stock Predictor",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .sub-title {
        text-align: center;
        color: #888;
        margin-top: 0;
        margin-bottom: 20px;
    }

    .signal-buy {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 14px;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
    }

    .signal-sell {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 14px;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
    }

    .signal-hold {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 14px;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 class='main-title'>AI Stock Prediction Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>Built by Aryan Rawat</p>",
    unsafe_allow_html=True
)

st.divider()

st.sidebar.title("Settings")

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

ticker = st.sidebar.selectbox(
    "Popular Stocks",
    popular_stocks
)

custom_ticker = st.sidebar.text_input(
    "Custom Ticker",
    placeholder="AMZN, TATAMOTORS.NS"
)

if custom_ticker.strip():
    ticker = custom_ticker.strip().upper()

predict_clicked = st.sidebar.button(
    "Predict",
    use_container_width=True
)

if predict_clicked:

    if not ticker:
        st.warning("Please enter a stock ticker.")

    else:
        st.subheader(f"{ticker}")

        col1, col2 = st.columns([2, 1])

        with col1:

            st.subheader("Price Chart (1 Month)")

            try:
                hist = yf.Ticker(ticker).history(period="1mo")

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

            except Exception as e:
                st.error(f"Chart Error: {e}")

        with col2:

            st.subheader("Prediction")

            with st.spinner("Analyzing..."):

                try:
                    res = requests.get(
                        API_URL,
                        params={"ticker": ticker},
                        timeout=60
                    )

                    data = res.json()

                    if "error" in data:
                        st.error(data["error"])

                    else:

                        st.metric(
                            "Current Price",
                            f"₹{data['current_price']}"
                        )

                        st.metric(
                            "Predicted Price",
                            f"₹{data['predicted_price']}",
                            delta=f"{data['predicted_change_pct']}%"
                        )

                        trend = (
                            "UP"
                            if data["trend"] == 1
                            else "DOWN"
                        )

                        st.write(f"**Trend:** {trend}")

                        if "trend_probability_up" in data:

                            probability = float(
                                data["trend_probability_up"]
                            )

                            probability = min(
                                max(probability, 0),
                                1
                            )

                            st.progress(probability)

                            st.caption(
                                f"Probability of UP: {probability:.2%}"
                            )

                        st.divider()

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
                                "<div class='signal-hold'>HOLD</div>",
                                unsafe_allow_html=True
                            )

                        st.divider()

                        st.subheader("Model Performance")

                        acc = data.get("model_accuracy")

                        if acc:

                            c1, c2, c3 = st.columns(3)

                            c1.metric(
                                "Trend Accuracy",
                                f"{acc['trend_accuracy_pct']}%"
                            )

                            c2.metric(
                                "Price MAE",
                                f"₹{acc['price_mae']}"
                            )

                            c3.metric(
                                "R² Score",
                                acc["price_r2_score"]
                            )

                            r2 = float(
                                acc["price_r2_score"]
                            )

                            if r2 >= 0.9:
                                st.success(
                                    "Excellent model fit"
                                )

                            elif r2 >= 0.7:
                                st.info(
                                    "Good model fit"
                                )

                            else:
                                st.warning(
                                    "Weak model fit"
                                )

                        else:
                            st.warning(
                                "Model accuracy data unavailable."
                            )

                except requests.exceptions.Timeout:
                    st.error(
                        "Request timed out. Please try again."
                    )

                except Exception as e:
                    st.error(
                        f"Connection Error: {e}"
                    )

st.divider()
st.markdown(
    """
    <p style='text-align:center; color:gray;'>
        © 2026 Aryan Rawat | AI Stock Predictor
    </p>
    """,
    unsafe_allow_html=True
)
