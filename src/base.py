import warnings

from matplotlib import rc
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px

from src.config import Config
from src.data import DataManager
from src.preprocess import Preprocess
from src.feature_engineering import FeatureEngineer


def system_setting():
    warnings.filterwarnings(action='ignore')
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False


def initialize_objects():
    conf = Config()
    dtm = DataManager(conf)
    preprocess = Preprocess(conf)
    feature_engineer = FeatureEngineer()
    return dtm, preprocess, feature_engineer


def load_data(dtm, preprocess):
    # data_raw = dtm.create_data_mart()
    # data_mart = preprocess.preprocess_data(data_raw)
    data_mart = pd.read_parquet("data/data_mart.parquet")
    return data_mart


def base_dashboard(make_chart, features, resolution: str):
    # Streamlit 대시보드
    if resolution=="daily":
         title = "일별 제조 데이터 대시보드"
         chart_prefix = "날짜별, 요일별"
         x_col = "date"
    elif resolution=="hourly":
         title = "시간별 제조 데이터 대시보드"
         chart_prefix = "날짜별, 요일별, 시간별"
         x_col = "date_time"
    
    st.title(title)
    st.divider()

    # Streamlit에서 날짜 범위 선택 위젯을 가로로 배치
    # 도넛 차트
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input('시작 날짜', value=features[x_col].min())
        start_date = pd.to_datetime(start_date)

    with col2:
        end_date = st.date_input('종료 날짜', value=features[x_col].max())
        end_date = pd.to_datetime(end_date)
        
    with col3:
        unique_mold_codes = features['mold_code'].unique()
        selected_mold_code = st.multiselect('Mold Code 선택', unique_mold_codes)
        

    # 선택한 날짜 범위에 맞게 데이터 필터링
    filtered_data = features[(features[x_col].between(start_date, end_date)) & 
                             (features['mold_code'].isin(selected_mold_code))]
    ## 선택 기간 정상품 비율
    pass_ratio = filtered_data['pass_count'].sum() / filtered_data['count'].sum()
    ## 선택 기간 불량품 비율
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
        fig1 = px.bar(filtered_data, x=x_col, y='count',
            color='weekday',
            title=f'{chart_prefix} 생산량',
            labels={'count': '생산량', 'hour': '시간', 'weekday': '요일'})

        # x축 범위 설정
        fig1.update_xaxes(range=[str(start_date), str(end_date)])
        st.plotly_chart(fig1)

    with tab2:
            # 날짜별, 요일별, 시간별 불량률 시각화
            fig2 = px.bar(filtered_data, x=x_col, y='error_ratio',
                    color='weekday', title=f'{chart_prefix} 불량률',
                    labels={'error_ratio': '불량률', 'hour': '시간', 'weekday': '요일'})
            
            ## 0.8 부분에 빨간색 점선 추가
            fig2.add_hline(y=0.8, line_dash='dot', line_color='red', annotation_text='불량률 80%', annotation_position='top right')


            # x축 범위 설정
            fig2.update_xaxes(range=[str(start_date), str(end_date)])
            st.plotly_chart(fig2)

    with tab3:

            # 날짜별, 요일별, 시간별 평균 생산 시간 시각화
            fig3 = px.bar(filtered_data, x=x_col, y='mean',
                    color='weekday',
                    title=f'{chart_prefix} 평균 생산 시간',
                    labels={'mean': '평균 생산 시간', 'hour': '시간', 'weekday': '요일'},
                    color_continuous_scale='Plasma'
                    )

            # x축 범위 설정
            fig3.update_xaxes(range=[str(start_date), str(end_date)])
            st.plotly_chart(fig3)


def base_dataframe():
    # 기본 데이터 프레임 생성
    default_values = {
        'molten_temp': 731,
        'production_cycletime': 120,
        'low_section_speed': 110,
        'high_section_speed': 110,
        'cast_pressure': 310,
        'biscuit_thickness': 40,
        'upper_mold_temp1': 200,
        'upper_mold_temp2': 200,
        'lower_mold_temp1': 200,
        'lower_mold_temp2': 200,
        'lower_mold_temp3': 1449,
        'sleeve_temperature': 480,
        'physical_strength': 0,
        'coolant_temperature': 30,
        'ems_operation_time': 2
    }
    df = pd.DataFrame(default_values, index=[0])
    return df