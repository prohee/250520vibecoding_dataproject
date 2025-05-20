import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.title("글로벌 시가총액 Top 10 기업의 최근 1년간 주식 변화")

# 글로벌 시가총액 Top 10 (2024.6 기준, 티커/회사명)
STOCKS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet(Google)",
    "AMZN": "Amazon",
    "NVDA": "NVIDIA",
    "BRK-B": "Berkshire Hathaway",
    "META": "Meta Platforms(Facebook)",
    "TSLA": "Tesla",
    "LLY": "Eli Lilly",
    "V": "Visa",
}
TICKERS = list(STOCKS.keys())

# 기간 설정 (최근 1년)
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

@st.cache_data(show_spinner=True)
def get_data(tickers, start, end):
    df = yf.download(tickers, start=start, end=end)["Adj Close"]
    if isinstance(df, pd.Series):
        df = df.to_frame()
    return df

st.info(f"아래 기업들의 최근 1년간 주가(종가, USD)를 비교합니다:\n\n" +
        ", ".join([f"{v} ({k})" for k, v in STOCKS.items()]))

# 데이터 가져오기
df = get_data(TICKERS, start_date, end_date)

# Plotly 그래프
fig = go.Figure()
for ticker in TICKERS:
    if ticker in df:
        fig.add_trace(go.Scatter(
            x=df.index, y=df[ticker],
            mode='lines',
            name=STOCKS[ticker]
        ))

fig.update_layout(
    title="글로벌 시가총액 Top 10 기업의 최근 1년 주가(USD)",
    xaxis_title="날짜",
    yaxis_title="종가(USD)",
    legend_title="기업명",
    hovermode="x unified",
    template="plotly_white",
    height=600,
)
st.plotly_chart(fig, use_container_width=True)

st.caption("데이터: Yahoo Finance (yfinance)")

# 선택적으로, 특정 기업만 보고 싶을 때 체크박스
with st.expander("특정 기업만 선택해서 보기"):
    selected = st.multiselect("기업 선택", options=TICKERS, default=TICKERS,
                              format_func=lambda x: f"{STOCKS[x]} ({x})")
    if selected:
        fig2 = go.Figure()
        for ticker in selected:
            fig2.add_trace(go.Scatter(
                x=df.index, y=df[ticker],
                mode='lines',
                name=STOCKS[ticker]
            ))
        fig2.update_layout(
            title="선택 기업 최근 1년 주가(USD)",
            xaxis_title="날짜",
            yaxis_title="종가(USD)",
            legend_title="기업명",
            hovermode="x unified",
            template="plotly_white",
            height=600,
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("기업을 하나 이상 선택하세요.")
