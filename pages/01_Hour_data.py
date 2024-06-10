import warnings

import numpy as np
import pandas as pd
from matplotlib import rc
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

from src.config import Config
from src.data import DataManager
from src.preprocess import Preprocess
from src.feature_engineering import FeatureEngineer
from src.charts import MakeChart



def initialize_objects():
    conf = Config()
    dtm = DataManager(conf)
    preprocess = Preprocess(conf)
    feature_engineer = FeatureEngineer()
    return dtm, preprocess, feature_engineer


def load_data(dtm, preprocess):
    data_raw = dtm.create_data_mart()
    data_mart = preprocess.preprocess_data(data_raw)
    return data_mart


def create_features(data_mart, feature_engineer):
    features = feature_engineer.hour_data_cleansing(data_mart)
    return features


def main():
    warnings.filterwarnings(action='ignore')
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    pd.set_option("display.max_rows", 50)
    pd.set_option("display.max_columns", 50)

    # Streamlit 대시보드
    st.title('시간별 제조 데이터 대시보드')
    st.balloons()
    st.divider()
    image_url = "https://firebasestorage.googleapis.com/v0/b/ls-storage-e452a.appspot.com/o/%E1%84%83%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8F%E1%85%A2%E1%84%89%E1%85%B3%E1%84%90%E1%85%B5%E1%86%BC.gif?alt=media&token=70587460-34c3-4a67-a056-f7a5e6ad8521"

    # HTML을 사용하여 이미지 크기 조정
    st.markdown(f'<img src="{image_url}" width="700" height="350">', unsafe_allow_html=True)

    dtm, preprocess, feature_engineer = initialize_objects()
    data_mart = load_data(dtm, preprocess)
    result = create_features(data_mart, feature_engineer)

    # st.markdown("### 1. 원천 데이터 마트")
    # st.write(data_mart)

    # st.markdown("### 2. 가공 피쳐")
    # st.write(result)

    make_chart = MakeChart()

    # Streamlit에서 날짜 범위 선택 위젯을 가로로 배치
    # 도넛 차트
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input('시작 날짜', value=result['date_time'].min())
    with col2:
        end_date = st.date_input('종료 날짜', value=result['date_time'].max())
        

    # 선택한 날짜 범위에 맞게 데이터 필터링
    filtered_data = result[(result['date_time'] >= pd.to_datetime(start_date)) &
                                    (result['date_time'] <= pd.to_datetime(end_date))]

    ## 정상품 비율
    pass_ratio = filtered_data['pass_count'].sum() / filtered_data['count'].sum()
    ## 불량품 비율
    fail_ratio = filtered_data['error_count'].sum() / filtered_data['count'].sum()

    # 필터링된 데이터로 도넛 차트 생성
    donut_chart_pass = make_chart.make_donut(pass_ratio.round(2) * 100, '정상품', 'green')
    donut_chart_fail = make_chart.make_donut(fail_ratio.round(2) * 100, '불량품', 'red')

    with col1:
        st.write('정상품 비율')
        st.altair_chart(donut_chart_pass, use_container_width=True)

    with col2:
        st.write('불량품 비율') 
        st.altair_chart(donut_chart_fail, use_container_width=True)



    # Streamlit을 사용해 대시보드에 차트 표시
    tab1, tab2, tab3 = st.tabs(['생산량', '불량률', '평균 생산 시간'])

    st.write(filtered_data)

    with tab1:
        # 날짜별, 요일별, 시간별 생산량 시각화
        fig1 = px.bar(filtered_data, x='date_time', y='count',
            color='weekday',
            title='날짜별, 요일별, 시간별 생산량',
            labels={'count': '생산량', 'hour': '시간', 'weekday': '요일'})

        # x축 범위 설정
        fig1.update_xaxes(range=[str(start_date), str(end_date)])
        st.plotly_chart(fig1)

    with tab2:
            # 날짜별, 요일별, 시간별 불량률 시각화
            fig2 = px.bar(filtered_data, x='date_time', y='error_ratio',
                    color='weekday', title='날짜별, 요일별, 시간별 불량률',
                    labels={'error_ratio': '불량률', 'hour': '시간', 'weekday': '요일'})
            
            ## 0.8 부분에 빨간색 점선 추가
            fig2.add_hline(y=0.8, line_dash='dot', line_color='red', annotation_text='불량률 80%', annotation_position='top right')


            # x축 범위 설정
            fig2.update_xaxes(range=[str(start_date), str(end_date)])
            st.plotly_chart(fig2)

    with tab3:

            # 날짜별, 요일별, 시간별 평균 생산 시간 시각화
            fig3 = px.bar(filtered_data, x='date_time', y='mean',
                    color='weekday',
                    title='날짜별, 요일별, 시간별 평균 생산 시간',
                    labels={'mean': '평균 생산 시간', 'hour': '시간', 'weekday': '요일'},
                    color_continuous_scale='Plasma'
                    )

            # x축 범위 설정
            fig3.update_xaxes(range=[str(start_date), str(end_date)])
            st.plotly_chart(fig3)


if __name__ == "__main__":
    main()
