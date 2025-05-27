import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="세계지리 데이터 분석")

# 사이드바 메뉴
page = st.sidebar.radio(
    "원하는 정보를 선택하세요",
    ["세계 지도(인구·면적·밀도)", "대륙별 통계·상관관계 분석"]
)

# 예시 세계지리 데이터 (국가명, 국가코드, 대륙, 인구, 면적)
DATA = [
    # 국가, ISO3, 대륙, 인구(백만), 면적(천㎢)
    ["China", "CHN", "Asia", 1440, 9597],
    ["India", "IND", "Asia", 1393, 3287],
    ["United States", "USA", "North America", 332, 9834],
    ["Indonesia", "IDN", "Asia", 277, 1911],
    ["Brazil", "BRA", "South America", 215, 8516],
    ["Nigeria", "NGA", "Africa", 223, 924],
    ["Russia", "RUS", "Europe", 144, 17098],
    ["Japan", "JPN", "Asia", 124, 378],
    ["Germany", "DEU", "Europe", 84, 357],
    ["United Kingdom", "GBR", "Europe", 68, 243],
    ["France", "FRA", "Europe", 65, 551],
    ["Egypt", "EGY", "Africa", 110, 1010],
    ["Canada", "CAN", "North America", 40, 9985],
    ["Australia", "AUS", "Oceania", 26, 7692],
    ["Argentina", "ARG", "South America", 46, 2780],
    ["South Africa", "ZAF", "Africa", 60, 1221],
    ["South Korea", "KOR", "Asia", 52, 100],
    ["Turkey", "TUR", "Asia", 85, 783],
    ["Saudi Arabia", "SAU", "Asia", 37, 2149],
    ["Mexico", "MEX", "North America", 128, 1964]
]
df = pd.DataFrame(DATA, columns=["국가", "국가코드", "대륙", "인구(백만)", "면적(천㎢)"])
df["인구밀도(명/㎢)"] = (df["인구(백만)"] * 1_000_000 / (df["면적(천㎢)"] * 1_000)).round(1)

if page == "세계 지도(인구·면적·밀도)":
    st.title("🌏 세계 지도 - 인구, 면적, 인구밀도 시각화")
    metric = st.selectbox("지도에 표시할 지표", ["인구(백만)", "면적(천㎢)", "인구밀도(명/㎢)"])
    fig = px.choropleth(
        df,
        locations="국가코드",
        color=metric,
        hover_name="국가",
        color_continuous_scale=px.colors.sequential.Plasma,
        labels={metric: metric},
        title=f"국가별 {metric} 지도"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("▼ 데이터 미리보기")
    st.dataframe(df)

elif page == "대륙별 통계·상관관계 분석":
    st.title("🗺️ 대륙별 통계 및 인구-면적 상관관계")
    # 대륙별 통계
    st.subheader("대륙별 평균 및 합계")
    summary = df.groupby("대륙").agg({
        "국가":"count",
        "인구(백만)":["sum","mean"],
        "면적(천㎢)":["sum","mean"],
        "인구밀도(명/㎢)":["mean"]
    })
    st.dataframe(summary)

    # 인구(백만) vs 면적(천㎢) 산점도
    st.subheader("국가별 인구(백만) vs 면적(천㎢) 산점도")
    fig2 = px.scatter(
        df,
        x="면적(천㎢)", y="인구(백만)",
        color="대륙", hover_name="국가",
        size="인구밀도(명/㎢)",
        labels={"면적(천㎢)":"면적(천㎢)", "인구(백만)":"인구(백만)"},
        title="국가별 인구-면적-밀도 관계"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 인구밀도 top5/bottom5
    st.subheader("인구밀도 상위/하위 5개국")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top 5**")
        st.dataframe(df.sort_values("인구밀도(명/㎢)", ascending=False).head(5)[["국가", "인구밀도(명/㎢)", "대륙"]])
    with col2:
        st.markdown("**Bottom 5**")
        st.dataframe(df.sort_values("인구밀도(명/㎢)", ascending=True).head(5)[["국가", "인구밀도(명/㎢)", "대륙"]])

    st.markdown("▼ 전체 데이터")
    st.dataframe(df)
