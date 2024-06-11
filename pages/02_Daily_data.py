from src.base import system_setting
from src.base import initialize_objects
from src.base import load_data
from src.base import base_dashboard
from src.charts import MakeChart


def main():
    system_setting()

    # 데이터 불러오기
    dtm, preprocess, feature_engineer = initialize_objects()
    data_mart = load_data(dtm, preprocess)
    
    # 챠트 객체 생성
    make_chart = MakeChart()

    # 대시보드 생성
    key_cols = ['date','weekday','mold_code']
    features = feature_engineer.create_features(data_mart, key_cols)
    base_dashboard(make_chart, features, resolution='daily')
    

if __name__ == "__main__":
    main()