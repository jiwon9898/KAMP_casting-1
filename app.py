import streamlit as st


st.set_page_config(
    page_title="LS빅데이터스쿨 2기 대시보드",
    page_icon="🏭",
)

# Streamlit 대시보드
st.title('LS빅데이터 스쿨 제조 데이터 대시보드')
st.balloons()
st.divider()
image_url = "https://firebasestorage.googleapis.com/v0/b/ls-storage-e452a.appspot.com/o/%E1%84%83%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8F%E1%85%A2%E1%84%89%E1%85%B3%E1%84%90%E1%85%B5%E1%86%BC.gif?alt=media&token=70587460-34c3-4a67-a056-f7a5e6ad8521"

# HTML을 사용하여 이미지 크기 조정
st.markdown(f'<img src="{image_url}" width="700" height="350">', unsafe_allow_html=True)


import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(df)

import streamlit as st
import pandas as pd
import numpy as np

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))


import streamlit as st
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)


import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name


import streamlit as st

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)




# ## 👨🏻‍🔧 효율적인 제조, 생산관리를 위한 대시보드

# 오늘날의 제조 환경은 점점 더 복잡해지고 있으며, 경쟁력을 유지하기 위해서는 신속하고 정확한 의사결정이 필수적입니다. 
# 이러한 요구에 부응하기 위해, 우리는 제조 공정 데이터를 기반으로 하는 최첨단 대시보드를 소개합니다. 
# 이 대시보드는 데이터를 효율적으로 시각화하고, 원하는 시간대 조회 서비스를 제공하여 제조 공정의 모든 측면을 개선할 수 있도록 설계되었습니다.

# #### 핵심 기능 및 이점
# --------------------------------

# ##### 📊 실시간 데이터 시각화 
# 제조 공정에서 발생하는 다양한 데이터를 수집하여 시각화합니다. 이를 통해 공정 상태를 한눈에 파악할 수 있으며, 빠른 의사결정을 지원합니다.

# --------------------------------

# ##### 📈 효율성 분석 
# 각 공정 단계의 성능을 분석하여 비효율적인 부분을 식별하고, 최적화 방안을 제시합니다. 이를 통해 자원 낭비를 최소화하고, 생산성을 극대화할 수 있습니다.

# --------------------------------

# ##### 🤖 불량요인 분석 
# 과거 데이터를 기반으로 미래의 공정 상태를 예측합니다. 예측 분석 기능을 통해 사전에 문제를 예방하고, 공정 안정성을 향상시킬 수 있습니다.

# --------------------------------

# ##### 🗺 맞춤형 대시보드 
# 사용자의 필요에 맞게 대시보드를 맞춤화할 수 있습니다. 각 사용자에게 가장 유용한 정보를 손쉽게 확인할 수 있도록 합니다.

# --------------------------------

# ##### 🛎 생산 관리 
# 일자별 및 시간별 데이터 조회 서비스를 제공하여 생산 관리를 보다 효율적으로 수행할 수 있도록 합니다.


            
# - [ ] [시간별 데이터 조회](/pages/01_Hour_data.py)
# - [ ] [일자별 데이터 조회](/pages/02_Daily_data.py)
# - [ ] [제품 품질 예측](/pages/03_Predict_data.py)

# """
# )


import time
import pandas as pd
import joblib
import streamlit as st

# CSV 파일 읽기
FILE_PATH = 'data/component1.csv'
data = pd.read_csv(FILE_PATH, encoding='cp949', index_col=0)
data = data.drop(columns=['ID','COMPONENT_ARBITRARY','U100', 'U75', 'U50','U25', 'U20','U14','U6', 'U4','FH2O','FNOX','FOPTIMETHGLY','FOXID','FSO4','FTBN','SOOTPERCENTAGE'])
data = data.dropna()

X = data.drop(columns=['Y_LABEL'], axis=1) 
y = data['Y_LABEL'] 

# feature_names 설정
feature_names = X.columns.tolist()

# 모델 학습 버튼
if st.button("모델 학습"):
    # 모델이 학습될 때까지 스핀
    with st.spinner("모델 학습 중..."):
        time.sleep(3)
        model = XGBClassifier(objective='binary:logistic', n_jobs=-1)
        model.fit(X, y)
        # 모델 로컬에 저장
        joblib.dump(model, './component1_model.pkl')
        st.write("✅ 모델이 학습되었습니다.")

# 데이터셋을 사용한 예측
st.header("🏗️ component1 데이터셋을 사용한 예측")

# 저장된 모델 로드
model = joblib.load('./component1_model.pkl')

# 입력 받기
num_features = len(feature_names)
input_values = []
cols = st.columns(4)

for i, feature in enumerate(feature_names):
    col = cols[i % 4]
    min_val = float(X[feature].min())
    max_val = float(X[feature].max())
    input_val = col.slider(feature, min_val, max_val)
    input_values.append(input_val)

# 입력 데이터를 데이터프레임으로 변환
input_data = pd.DataFrame([input_values], columns=feature_names)

# 예측
prediction = model.predict(input_data)

species_mapping = {
    0: '양품',
    1: '불량품'
}

predicted_species = species_mapping[prediction[0]]
# 예측 확률 
prediction_proba = model.predict_proba(input_data)

st.write(f"✅ 예측된 결과 => {predicted_species}")
# 예측 결과가 '불량품'이면 Alert창
if predicted_species == '불량품':
    st.warning(f"🔴 경고: 불량품이라는 예측이 나오면 {prediction_proba[0][1]} 확률로 경고를 합니다.")
else:
    st.success(f"🟢 안전: 양품이라는 예측이 나오면 {prediction_proba[0][0]} 확률로 안전합니다.")

st.write("🤖 확률 TABLE")
st.write(pd.DataFrame(prediction_proba, columns=['양품', '불량품']))

st.divider()

# 예측
prediction = model.predict(input_data)

species_mapping = {
    0: '양품',
    1: '불량품'
}

predicted_species = species_mapping[prediction[0]]
# 예측 확률 
prediction_proba = model.predict_proba(input_data)
defective_proba = prediction_proba[0][1]

st.write(f"✅ 예측된 결과 => {predicted_species}")
# 예측 결과에 따른 경고 메시지 색상 변경
if defective_proba > 0.9:
    st.error(f"🔴 경고: 불량품이라는 예측이 나오면 {defective_proba:.2%} 확률로 경고를 합니다.")
elif defective_proba > 0.8:
    st.warning(f"🟡 주의: 불량품이라는 예측이 나오면 {defective_proba:.2%} 확률로 경고를 합니다.")
else:
    st.success(f"🟢 안전: 양품이라는 예측이 나오면 {1 - defective_proba:.2%} 확률로 안전합니다.")

st.write("🤖 확률 TABLE")
st.write(pd.DataFrame(prediction_proba, columns=['양품', '불량품']))

st.divider()


# 연도별 불량품 비율 계산
yearly_defects = data.groupby('YEAR')['Y_LABEL'].mean().reset_index()
yearly_defects.columns = ['YEAR', 'Defective_Ratio']

# 연도별 불량품 비율 그래프
st.header("📊 연도별 불량품 비율")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_defects['YEAR'], yearly_defects['Defective_Ratio'], marker='o')
ax.set_title('Defective Ratio per Year')
ax.set_xlabel('Year')
ax.set_ylabel('Defective Ratio')
ax.grid(True)
ax.set_xticks(yearly_defects['YEAR'].unique())

st.pyplot(fig)


# 특정 연도의 불량, 양품 비율과 갯수 시각화
st.header("📅 특정 연도의 불량, 양품 비율과 갯수")

# 연도 선택 옵션 추가 (작은순서부터 큰순서로 정렬)
years_sorted = sorted(data['YEAR'].unique())
selected_year = st.selectbox('연도 선택', years_sorted)

# 선택한 연도에 해당하는 데이터 필터링
filtered_data = data[data['YEAR'] == selected_year]

# 불량, 양품 갯수와 비율 계산
total_count = filtered_data.shape[0]
defective_count = filtered_data['Y_LABEL'].sum()
non_defective_count = total_count - defective_count
defective_ratio = defective_count / total_count
non_defective_ratio = non_defective_count / total_count

# 결과 출력
st.write(f"선택한 연도: {selected_year}")
st.write(f"총 갯수: {total_count}")
st.write(f"불량품 갯수: {defective_count} ({defective_ratio:.2%})")
st.write(f"양품 갯수: {non_defective_count} ({non_defective_ratio:.2%})")

# 비율 시각화
fig2, ax2 = plt.subplots()
ax2.bar(['양품', '불량품'], [non_defective_count, defective_count], color=['green', 'red'])
ax2.set_title(f'불량, 양품 비율 (연도: {selected_year})')
ax2.set_ylabel('갯수')

st.pyplot(fig2)
