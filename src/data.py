import os
import pandas as pd


def read_data(data_dir="./data", data_filename="casting.csv"):
    data_path = os.path.abspath(os.path.join(data_dir, data_filename))
    print("data_path:", data_path)
    data = pd.read_csv(data_path, encoding='euckr')
    return data