import streamlit as st
import requests
import yfinance as yf
import plotly.graph_objects as go

API_URL = "https://stockmarketprediction-r270.onrender.com/predict"

st.set_page_config(
    page_title="AI Stock Predictor",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:48px;
    font-weight:700;
    margin-bottom:0;
}

.subtitle{
    text-align:center;
    color:#9ca3af;
    margin-bottom:30px;
}

div[data-testid="metric-container"]{
    background-color:#111827;
    border:1px solid #374151;
    border-radius:15px;
    padding:15px;
}

.signal-buy{
    background:linear-gradient(90deg,#059669,#10b981);
    color:white;
    padding:22px;
    border-radius:15px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
}

.signal-sell{
    background:linear-gradient(90deg,#b91c1c,#ef4444);
    color:white;
    padding:22px;
    border-radius:15px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
}

.signal-hold{
    background:linear-gradient(90deg,#ca8a04,#facc15);
    color:white;
    padding:22px;
    border-radius:15px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
}

.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 class='main-title'>AI Stock Predictor</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Machine Learning Market Forecasting</p>",
    unsafe_allow_html=True
)

st.divider()

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

left, center, right = st.columns([1,2,1])

with center:

    ticker = st.selectbox(
        "Select Stock",
        popular_stocks
    )

    custom_ticker = st.text_input(
        "Custom Ticker",
        placeholder="AMZN, TATAMOTORS.NS"
    )

    if custom_ticker.strip():
        ticker = custom_ticker.strip().upper()

    predict_clicked = st.button(
        "Analyze Stock",
        use_container_width=True,
        type="primary"
    )

if predict_clicked:

    try:

        stock = yf.Ticker(ticker)

        try:
            info = stock.info

            company = info.get(
                "longName",
                ticker
            )

            sector = info.get(
                "sector",
                ""
            )

            st.subheader(company)

            if sector:
                st.caption(sector)

        except:
            pass

        hist = stock.history(period="1mo")

        st.subheader("Price Chart")

        if hist.empty:

            st.warning("No market data available.")

        else:

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=hist.index,
                    y=hist["Close"],
                    mode="lines",
                    line=dict(width=3)
                )
            )

            fig.update_layout(
                template="plotly_dark",
                height=450,
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20
                ),
                xaxis_title="Date",
                yaxis_title="Price"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            last_close = float(
                hist["Close"].iloc[-1]
            )

            prev_close = float(
                hist["Close"].iloc[-2]
            )

            change = last_close - prev_close

            change_pct = (
                change / prev_close
            ) * 100

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

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Current Price",
                    f"₹{data['current_price']}"
                )

                c2.metric(
                    "Predicted Price",
                    f"₹{data['predicted_price']}",
                    f"{data['predicted_change_pct']}%"
                )

                trend = (
                    "UP"
                    if data["trend"] == 1
                    else "DOWN"
                )

                c3.metric(
                    "Trend",
                    trend
                )

                if "trend_probability_up" in data:

                    probability = float(
                        data["trend_probability_up"]
                    )

                    probability = max(
                        0,
                        min(1, probability)
                    )

                    gauge = go.Figure(
                        go.Indicator(
                            mode="gauge+number",
                            value=probability * 100,
                            title={
                                "text":
                                "UP Probability"
                            },
                            gauge={
                                "axis": {
                                    "range":
                                    [0,100]
                                }
                            }
                        )
                    )

                    gauge.update_layout(
                        template="plotly_dark",
                        height=300
                    )

                    st.plotly_chart(
                        gauge,
                        use_container_width=True
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

                st.subheader(
                    "Model Performance"
                )

                acc = data.get(
                    "model_accuracy"
                )

                if acc:

                    p1, p2, p3 = st.columns(3)

                    p1.metric(
                        "Trend Accuracy",
                        f"{acc['trend_accuracy_pct']}%"
                    )

                    p2.metric(
                        "Price MAE",
                        f"₹{acc['price_mae']}"
                    )

                    p3.metric(
                        "R² Score",
                        acc["price_r2_score"]
                    )

        st.divider()

    except requests.exceptions.Timeout:

        st.error(
            "Request timed out."
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

st.markdown(
    """
    <p style='text-align:center;color:gray;margin-top:30px;'>
    © 2026 Aryan Rawat | AI Stock Predictor
    </p>
    """,
    unsafe_allow_html=True
)
