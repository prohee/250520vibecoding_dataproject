import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

st.set_page_config(layout='wide')
st.title("서울시 인구 피라미드 (Plotly, Streamlit)")

uploaded_file = st.file_uploader("읍면동별 성별/연령별 인구 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 인코딩 자동 판별
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    
    # '행정구역' 컬럼명 판단 (첫 컬럼)
    region_col = df.columns[0]
    
    # '서울특별시' 전체 행 찾기
    seoul_row = df[df[region_col].str.contains("서울특별시")].iloc[0]
    
    # 연령별 남여 컬럼 찾기 (패턴: '2025년04월_0세_남자', ...)
    age_male_cols = []
    age_female_cols = []
    age_labels = []
    for col in df.columns:
        match = re.match(r"20\d{2}년\d{2}월_([0-9]{1,3})세_남자", col)
        if match:
            age = match.group(1)
            age_male_cols.append(col)
            age_labels.append(age)
        match = re.match(r"20\d{2}년\d{2}월_([0-9]{1,3})세_여자", col)
        if match:
            age_female_cols.append(col)
    
    # 정렬
    age_labels = sorted(list(set(age_labels)), key=lambda x: int(x))
    age_male_cols = sorted(age_male_cols, key=lambda x: int(re.search(r'(\d+)세_남자', x).group(1)))
    age_female_cols = sorted(age_female_cols, key=lambda x: int(re.search(r'(\d+)세_여자', x).group(1)))
    
    # 각 연령별 남자/여자 인구수 추출
    male_counts = [-int(seoul_row[col].replace(",","")) for col in age_male_cols]  # 음수로 변환
    female_counts = [int(seoul_row[col].replace(",","")) for col in age_female_cols]

    # Plotly 피라미드
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=age_labels,
        x=male_counts,
        name='남자',
        orientation='h',
        marker_color='royalblue',
        hovertemplate='남자: %{x:,.0f}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        y=age_labels,
        x=female_counts,
        name='여자',
        orientation='h',
        marker_color='lightpink',
        hovertemplate='여자: %{x:,.0f}<extra></extra>'
    ))
    fig.update_layout(
        barmode='relative',
        title='서울시 인구 피라미드 (남녀구분)',
        xaxis=dict(title='인구수', tickvals=[-10000, -5000, 0, 5000, 10000]),
        yaxis=dict(title='연령', categoryorder='category ascending'),
        bargap=0.1,
        plot_bgcolor='white',
        legend=dict(x=0.8, y=1.1, orientation="h"),
        height=800
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("※ 왼쪽(음수)은 남자, 오른쪽(양수)은 여자입니다.")
else:
    st.info("CSV 파일을 업로드하세요. (예: 행정구역, ..., '2025년04월_0세_남자', ...)")
