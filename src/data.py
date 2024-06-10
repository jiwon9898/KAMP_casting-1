import os
import pandas as pd


class Data:
    def __init__(self):
        self.data_dir = "./data"
        self.data_filename = "casting.csv"
        pass

    def read_data(self, data_dir=None, data_filename=None):
        if data_dir is None:
            data_dir = self.data_dir
        if data_filename is None:
            data_filename = self.data_filename

        data_path = os.path.abspath(os.path.join(data_dir, data_filename))
        
        if data_filename.split(".")[-1] == "csv":
            data = pd.read_csv(data_path, encoding='euckr')
        else:
            raise ValueError("only csv file can be loaded now.")
        
        if data.columns[0] == "Unnamed: 0":
            data = data.set_index(data.columns[0])
            data.index.name = None
        
        return data