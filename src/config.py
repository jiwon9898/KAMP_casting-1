import yaml


class Config:
    def __init__(self):
        with open("config/db.yml", 'r') as file:
            conf = yaml.safe_load(file)
            self.db_config = conf['db_config']
        with open("config/values.yml", 'r') as file:
            conf = yaml.safe_load(file)
            self.normal_range_dict = conf['normal_range_dict']
        pass
        