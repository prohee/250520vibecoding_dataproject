import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Streamlit + Folium 인터랙티브 지도 앱")

# 기본 지도 위치(서울)
default_lat = 37.5665
default_lon = 126.9780

st.write("지도에서 원하는 위치를 클릭하면 마커가 표시됩니다.")

# 지도 생성
m = folium.Map(location=[default_lat, default_lon], zoom_start=12)

# Streamlit에서 지도 클릭 이벤트 감지 및 마커 추가
map_data = st_folium(m, width=700, height=500)

if map_data and map_data["last_clicked"]:
    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lon = map_data["last_clicked"]["lng"]
    st.success(f"클릭한 위치: 위도 {clicked_lat:.5f}, 경도 {clicked_lon:.5f}")

    # 마커 추가
    m = folium.Map(location=[clicked_lat, clicked_lon], zoom_start=15)
    folium.Marker([clicked_lat, clicked_lon], popup="여기!").add_to(m)
    st_folium(m, width=700, height=500)

else:
    st.info("지도를 클릭해보세요!")

st.write("---")
st.write("이 앱은 folium+streamlit-folium을 사용하여 동작합니다.")
