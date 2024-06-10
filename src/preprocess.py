class Preprocess:
    def __init__(self):
        self.key_cols = ["registration_time","count"]
        pass

    def normalize_column_name(self, data):
        data_cols = list(map(lambda s: s.lower(), data.columns))
        data.columns = data_cols
        data['date'], data['time'] = data['time'], data['date']
        return data

    def remove_trivial_columns(self, data):
        rm_cols = [
            'line',
            'name',
            'mold_name',
            'time',
            'date',
            'tryshot_signal',
            'working',
            'emergency_stop',
        ]
        data = data.drop(columns=rm_cols)
        return data

    def drop_duplicated_rows(self, data):
        data = data.drop_duplicates(subset=self.key_cols, keep='first')
        return data

    @property
    def data_type_dict(self):
        type_dict = {
            'registration_time': pd.to_datetime,
            'mold_code': np.vectorize(lambda x: "CODE_" + str(x))
        }
        return type_dict
    
    def data_type_casting(self, data):
        type_dict = self.data_type_dict
        for c in type_dict.keys():
            func = type_dict.get(c, lambda x: x)
            data[c] = func(data[c])
        return data

    def sort_data(self, data):
        data = data.sort_values(self.key_cols)
        return data

    def mask_abnormal_values(self, data):
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
        for c in data:
            normal_range = normal_range_dict.get(data[c].name, None)
            if normal_range is None:
                continue
            cond = data[c].between(*sorted(normal_range), inclusive='both')
            data[c] = data[c].mask(~cond)
        return data

    def drop_trivial_rows(self, data):
        cond = data['passorfail'].notnull()
        data = data.loc[cond]
        return data

    def create_feature(self, data):
        data['hour'] = data['registration_time'].apply(lambda t: t.hour)
        data['']
        return data

    def preprocess_data(self, data_before):
        data_after = data_before.copy()
        data_after = self.normalize_column_name(data_after)
        data_after = self.remove_trivial_columns(data_after)
        data_after = self.drop_duplicated_rows(data_after)
        data_after = self.data_type_casting(data_after)
        data_after = self.sort_data(data_after)
        data_after = self.mask_abnormal_values(data_after)
        data_after = self.drop_trivial_rows(data_after)
        return data_after
