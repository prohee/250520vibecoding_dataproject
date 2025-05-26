import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

st.set_page_config(layout='wide', page_title='세계 지리와 교육 수준 비교')

st.sidebar.title("세계 지리와 교육 수준")
page = st.sidebar.radio("메뉴", ["세계 지도에서 교육 수준 보기", "대륙별 교육 수준 비교"])

uploaded_file = st.file_uploader("국가별 평균 교육년수 데이터(CSV, Barro-Lee/UNDP 등)", type=["csv"])

def get_continent(code):
    # 주요 대륙 코드 매핑 (alpha-3 기준)
    africa = {'DZA','AGO','BEN','BWA','BFA','BDI','CMR','CPV','CAF','TCD','COM','COG','COD','DJI','EGY','GNQ','ERI','ETH','GAB','GMB','GHA','GIN','GNB','KEN','LSO','LBR','LBY','MDG','MWI','MLI','MRT','MUS','MAR','MOZ','NAM','NER','NGA','RWA','STP','SEN','SYC','SLE','SOM','ZAF','SSD','SDN','SWZ','TZA','TGO','TUN','UGA','ESH','ZMB','ZWE'}
    asia = {'AFG','ARM','AZE','BHR','BGD','BTN','BRN','KHM','CHN','CYP','GEO','IND','IDN','IRN','IRQ','ISR','JPN','JOR','KAZ','PRK','KOR','KWT','KGZ','LAO','LBN','MAC','MYS','MDV','MNG','MMR','NPL','OMN','PAK','PHL','QAT','SAU','SGP','LKA','SYR','TWN','TJK','THA','TLS','TUR','TKM','ARE','UZB','VNM','YEM','HKG','PSX'}
    europe = {'ALB','AND','AUT','BLR','BEL','BIH','BGR','HRV','CZE','DNK','EST','FRO','FIN','FRA','DEU','GIB','GRC','GGY','HUN','ISL','IRL','IMN','ITA','JEY','LVA','LIE','LTU','LUX','MLT','MDA','MCO','MNE','NLD','MKD','NOR','POL','PRT','ROU','RUS','SMR','SRB','SVK','SVN','ESP','SJM','SWE','CHE','UKR','GBR','VAT'}
    north_america = {'AIA','ATG','ABW','BHS','BRB','BLZ','BMU','BES','VGB','CAN','CYM','CRI','CUB','CUW','DMA','DOM','SLV','GRL','GRD','GLP','GTM','HTI','HND','JAM','MTQ','MEX','MSR','ANT','NIC','PAN','PRI','KNA','LCA','SPM','VCT','SXM','TTO','TCA','USA','VIR'}
    south_america = {'ARG','BOL','BRA','CHL','COL','ECU','FLK','GUF','GUY','PRY','PER','SUR','URY','VEN'}
    oceania = {'ASM','AUS','COK','FJI','PYF','GUM','KIR','MHL','FSM','NRU','NCL','NZL','NIU','NFK','MNP','PLW','PNG','PCN','WSM','SLB','TKL','TON','TUV','UMI','VUT','WLF'}
    code = str(code).upper()
    if code in africa:
        return '아프리카'
    elif code in asia:
        return '아시아'
    elif code in europe:
        return '유럽'
    elif code in north_america:
        return '북아메리카'
    elif code in south_america:
        return '남아메리카'
    elif code in oceania:
        return '오세아니아'
    else:
        return '기타'

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # 컬럼명 표준화
    df = df.rename(columns=lambda x: x.strip())
    # 주요 컬럼명 찾기
    # Entity/국가명, Code/국가코드, Year/연도, Mean years of schooling...
    if "Entity" in df.columns:
        df = df.rename(columns={"Entity": "국가"})
    if "Country" in df.columns:
        df = df.rename(columns={"Country": "국가"})
    if "Code" in df.columns:
        df = df.rename(columns={"Code": "국가코드"})
    if "ISO3" in df.columns:
        df = df.rename(columns={"ISO3": "국가코드"})
    if "Year" in df.columns:
        df = df.rename(columns={"Year": "연도"})
    # 평균 교육년수 컬럼 찾기
    edu_col = [c for c in df.columns if "Mean years of schooling" in c or "평균교육년수" in c]
    if not edu_col:
        st.error("평균 교육년수에 해당하는 컬럼이 없습니다.")
        st.stop()
    edu_col = edu_col[0]
    df = df.rename(columns={edu_col: "평균교육년수"})
    # 최신 연도만 추출
    if "연도" in df.columns:
        latest_year = df["연도"].max()
        df = df[df["연도"] == latest_year]
    # 국가코드, 국가, 평균교육년수 컬럼만 추출
    df = df.dropna(subset=["평균교육년수", "국가코드"])
    df["평균교육년수"] = pd.to_numeric(df["평균교육년수"], errors='coerce')
    df = df.dropna(subset=["평균교육년수"])
    # 대륙 정보 추가
    df["대륙"] = df["국가코드"].apply(get_continent)

    # 1페이지: 세계 지도
    if page == "세계 지도에서 교육 수준 보기":
        st.header("세계 지도에서 국가별 평균 교육년수(교육 수준) 보기")
        st.markdown("#### 업로드한 파일에서 추출한 데이터(최신 연도 기준)")
        fig = px.choropleth(
            df,
            locations="국가코드",
            color="평균교육년수",
            hover_name="국가",
            color_continuous_scale=px.colors.sequential.Plasma,
            title="국가별 평균 교육년수 (최신 연도)",
            labels={"평균교육년수": "평균 교육년수 (년)"}
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":60,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        - 색이 진할수록 평균 교육년수가 많음(교육수준이 높음)
        - 국가명을 클릭하면 상세정보가 나옵니다.
        """)

    # 2페이지: 대륙별 비교
    elif page == "대륙별 교육 수준 비교":
        st.header("대륙(지리)별 평균 교육년수 비교")
        # 박스플롯
        fig = px.box(
            df[df["대륙"] != "기타"],
            x="대륙",
            y="평균교육년수",
            points="all",
            color="대륙",
            title="대륙별 평균 교육년수 분포"
        )
        st.plotly_chart(fig, use_container_width=True)
        # 대륙별 평균/표준편차
        st.markdown("#### 대륙별 평균/표준편차")
        summary = df[df["대륙"] != "기타"].groupby("대륙")["평균교육년수"].agg(["mean", "std", "min", "max", "count"]).round(2)
        st.dataframe(summary)
        # 국가별 top/bottom 5
        st.markdown("#### 교육년수가 가장 높은 5개국 / 가장 낮은 5개국")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Top 5**")
            st.dataframe(df.sort_values("평균교육년수", ascending=False).head(5)[["국가", "대륙", "평균교육년수"]])
        with col2:
            st.markdown("**Bottom 5**")
            st.dataframe(df.sort_values("평균교육년수", ascending=True).head(5)[["국가", "대륙", "평균교육년수"]])

else:
    st.info("CSV 파일을 업로드하면 분석 결과가 나옵니다. (파일 컬럼: 국가명, 국가코드, 연도, 평균교육년수)")
