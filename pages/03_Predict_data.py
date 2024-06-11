import joblib

import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.base import system_setting
from src.base import base_dataframe


def predict_page(model, base_df):
    st.title("주조 모델 예측 대시보드")

    # 첫 번째 구역: 개별 데이터 입력 및 결과 출력
    st.header("개별 예측")

    with st.form("individual_prediction_form"):
        edited_df = st.data_editor(base_df, num_rows="dynamic")
        submit_button = st.form_submit_button(label="예측")

    if submit_button:
        result_proba = model.predict_proba(edited_df)
        result = model.predict(edited_df)
        result_text = "✅ 정상품" if result[0] == 0 else "❌ 불량품"
        st.write(f"예측 결과: {result_text}")
        st.write(f"불량 확률: {result_proba[0][1] * 100:.2f}%")

    st.header("특정 변수의 범위 예측")
    with st.form("range_prediction_form"):
        selected_col = st.selectbox("⭐️ 범위로 지정할 변수 선택", list(base_df.columns))
        cols = st.columns(3)
        min_value = cols[0].number_input(f"변경될 최소 값", value=0)
        max_value = cols[1].number_input(f"변경될 최대 값", value=1000)
        step_value = cols[2].number_input("스텝 값", value=10)
        st.divider()
        
        # 나머지 변수들 입력 (2열로 나누어 표시)
        cols = st.columns(2)
        for i, col in enumerate(base_df.columns):
            if col != selected_col:
                base_df[col] = cols[i % 2].number_input(f"{col} 값", value=base_df[col].item())
        
        range_submit_button = st.form_submit_button(label="시각화")

    if range_submit_button:
        selected_values = np.arange(min_value, max_value + step_value, step_value)
        range_df = pd.concat([base_df] * len(selected_values), ignore_index=True)
        range_df[selected_col] = selected_values
        
        range_result_proba = model.predict_proba(range_df)
        range_df['failure_probability'] = range_result_proba[:, 1] * 100

        fig = px.line(range_df, x=selected_col, y='failure_probability',
                    title=f'{selected_col} 값의 범위에 따른 불량 확률',
                    labels={selected_col: f'{selected_col}', 'failure_probability': '불량 확률 (%)'})
        
        ## 50 부분에 빨간색 점선 추가
        fig.add_hline(y=20, line_dash='dot', line_color='red', annotation_text='불량률 20%', annotation_position='top right')
        
        st.plotly_chart(fig)


def main():
    system_setting()

    # 초기 데이터 생성
    base_df = base_dataframe()
    
    # 모델 불러오기
    model = joblib.load('models/random_forest_classifier.joblib')

    predict_page(model, base_df)


if __name__ == "__main__":
    main()