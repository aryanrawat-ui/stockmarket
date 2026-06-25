import streamlit as st
import requests
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

API_URL = "https://stockmarketprediction-r270.onrender.com/predict"

st.set_page_config(
    page_title="AI Market Intelligence",
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
    background:#111827;
    border:1px solid #2d3748;
    border-radius:14px;
    padding:18px;
}

.stTabs [data-baseweb="tab-list"]{
    gap:10px;
}

.stTabs [data-baseweb="tab"]{
    background:#111827;
    border-radius:10px;
    padding:10px 20px;
}

.signal-buy{
    background:linear-gradient(90deg,#00b09b,#96c93d);
    color:white;
    padding:25px;
    border-radius:15px;
    text-align:center;
    font-size:30px;
    font-weight:700;
}

.signal-sell{
    background:linear-gradient(90deg,#cb2d3e,#ef473a);
    color:white;
    padding:25px;
    border-radius:15px;
    text-align:center;
    font-size:30px;
    font-weight:700;
}

.signal-hold{
    background:linear-gradient(90deg,#d1913c,#ffd194);
    color:white;
    padding:25px;
    border-radius:15px;
    text-align:center;
    font-size:30px;
    font-weight:700;
}

.block-container{
    padding-top:1rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 class='main-title'>AI Market Intelligence</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Real-Time AI Market Analysis & Prediction</p>",
    unsafe_allow_html=True
)

left, center, right = st.columns([1,2,1])

with center:

    company = st.text_input(
        "Search Company or Ticker",
       placeholder="Apple, Tesla, Reliance, TCS, AAPL, TSLA..."
    )

    if company:
        ticker = company.strip()
    else:
        ticker = "Reliance"

    chart_period = st.radio(
        "Time Period",
        ["1M","6M","1Y","5Y"],
        horizontal=True
    )

    analyze = st.button(
        "Analyze Market",
        use_container_width=True,
        type="primary"
    )

period_map = {
    "1M":"1mo",
    "6M":"6mo",
    "1Y":"1y",
    "5Y":"5y"
}
if analyze:

    try:

        with st.spinner("Analyzing market..."):

            response = requests.get(
                API_URL,
                params={"query": ticker},
                timeout=60
            )

            data = response.json()

            if "error" in data:

                st.error(data["error"])

            else:

                real_ticker = data["stock"]

                stock = yf.Ticker(real_ticker)

                try:

                    info = stock.info

                    company_name = info.get(
                        "longName",
                        real_ticker
                    )

                    sector = info.get(
                        "sector",
                        "Unknown"
                    )

                    market_cap = info.get(
                        "marketCap",
                        "N/A"
                    )

                    pe_ratio = info.get(
                        "trailingPE",
                        "N/A"
                    )

                    high52 = info.get(
                        "fiftyTwoWeekHigh",
                        "N/A"
                    )

                    low52 = info.get(
                        "fiftyTwoWeekLow",
                        "N/A"
                    )

                except:

                    company_name = real_ticker
                    sector = "Unknown"
                    market_cap = "N/A"
                    pe_ratio = "N/A"
                    high52 = "N/A"
                    low52 = "N/A"

                st.subheader(company_name)
                st.caption(sector)

                tab1, tab2, tab3, tab4 = st.tabs(
                    [
                        "Summary",
                        "Chart",
                        "Analysis",
                        "Prediction"
                    ]
                )

                with tab1:

                    s1, s2, s3, s4 = st.columns(4)

                    s1.metric(
                        "Market Cap",
                        market_cap
                    )

                    s2.metric(
                        "PE Ratio",
                        pe_ratio
                    )

                    s3.metric(
                        "52W High",
                        high52
                    )

                    s4.metric(
                        "52W Low",
                        low52
                    )

                hist = stock.history(
                    period=period_map[chart_period]
                )

                hist["MA20"] = (
                    hist["Close"]
                    .rolling(20)
                    .mean()
                )

                hist["MA50"] = (
                    hist["Close"]
                    .rolling(50)
                    .mean()
                )

                with tab2:

                    fig = make_subplots(
                        rows=2,
                        cols=1,
                        shared_xaxes=True,
                        row_heights=[0.8,0.2],
                        vertical_spacing=0.03
                    )

                    fig.add_trace(
                        go.Candlestick(
                            x=hist.index,
                            open=hist["Open"],
                            high=hist["High"],
                            low=hist["Low"],
                            close=hist["Close"],
                            name="Price"
                        ),
                        row=1,
                        col=1
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=hist.index,
                            y=hist["MA20"],
                            name="MA20",
                            line=dict(width=2)
                        ),
                        row=1,
                        col=1
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=hist.index,
                            y=hist["MA50"],
                            name="MA50",
                            line=dict(width=2)
                        ),
                        row=1,
                        col=1
                    )

                    fig.add_trace(
                        go.Bar(
                            x=hist.index,
                            y=hist["Volume"],
                            name="Volume"
                        ),
                        row=2,
                        col=1
                    )

                    fig.update_layout(
                        template="plotly_dark",
                        height=700,
                        xaxis_rangeslider_visible=False,
                        hovermode="x unified",
                        margin=dict(
                            l=20,
                            r=20,
                            t=20,
                            b=20
                        )
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )
                with tab3:

                    acc = data.get(
                        "model_accuracy"
                    )

                    if acc:

                        a1, a2, a3 = st.columns(3)

                        a1.metric(
                            "Trend Accuracy",
                            f"{acc['trend_accuracy_pct']}%"
                        )

                        a2.metric(
                            "Price MAE",
                            f"₹{acc['price_mae']}"
                        )

                        a3.metric(
                            "R² Score",
                            acc["price_r2_score"]
                        )

                        r2 = float(
                            acc["price_r2_score"]
                        )

                        if r2 >= 0.90:

                            st.success(
                                "Excellent model fit"
                            )

                        elif r2 >= 0.70:

                            st.info(
                                "Good model fit"
                            )

                        else:

                            st.warning(
                                "Weak model fit"
                            )

                with tab4:

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
                                        "range": [0,100]
                                    },
                                    "bar": {
                                        "color": "limegreen"
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
                            """
                            <div class='signal-buy'>
                            BUY SIGNAL
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    elif decision == "SELL":

                        st.markdown(
                            """
                            <div class='signal-sell'>
                            SELL SIGNAL
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            """
                            <div class='signal-hold'>
                            HOLD SIGNAL
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.write("")

                    p1, p2 = st.columns(2)

                    p1.metric(
                        "Expected Change",
                        f"{data['predicted_change_pct']}%"
                    )

                    p2.metric(
                        "Ticker",
                        real_ticker
                    )

    except requests.exceptions.Timeout:

        st.error(
            "Request timed out."
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

st.write("")

st.divider()

st.markdown(
    """
    <p style='text-align:center;
              color:#9ca3af;
              font-size:14px;'>
    AI Market Intelligence • Built by Aryan Rawat
    </p>
    """,
    unsafe_allow_html=True
)