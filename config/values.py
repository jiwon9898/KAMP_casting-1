normal_range_dict = {
    # temperature_cols
    "molten_temp": [0, 750],                   # 용탕온도
    "sleeve_temperature": [0, 650], #[0, 500], # 슬리브온도
    "coolant_temperature": [0, 50],            # 냉각수 온도
    "upper_mold_temp1": [0, 1500],             # 상금형온도1
    "upper_mold_temp2": [0, 1500],             # 상금형온도2
    "upper_mold_temp3": [0, 1500],             # 상금형온도3
    "lower_mold_temp1": [0, 400],              # 하금형온도1
    "lower_mold_temp2": [0, 500],              # 하금형온도2
    "lower_mold_temp3": [0, 1500],             # 하금형온도3
    # speed_cols
    "high_section_speed": [0, 400],            # 고속구간속도 (단위: m/min?)
    "low_section_speed": [0, 200],             # 저속구간속도 (단위: m/min?)
    # time_cols
    "ems_operation_time": [0, 25],             # 전자교반 가동시간 (단위: 초?)
    "facility_operation_cycletime": [0, 500],  # 설비 작동 사이클시간 (단위: 초?)
    "production_cycletime": [0, 500],          # 제품생산 사이클 시간 (단위: 초?)
    # etc_cols
    "cast_pressure": [0, 400],                 # 주조압력 (단위: MPa?)
    "biscuit_thickness": [0,450],              # 비스켓 두께
    "physical_strength": [0, 800],             # 형체력
    "molten_volume": None,                     # 용탕량
    "count": None,                             # 제품 생산 번호
    "registration_time": None,                 # 등록일시
    "mold_code": None,                         # 금형코드
    "heating_furnace": None,                   # 가열로
    # passorfail_col
    "passorfail": [0, 1],                      # 양품불량판정
}