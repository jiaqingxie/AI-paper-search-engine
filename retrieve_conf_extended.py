import pandas as pd
from os import path

cur_path = path.dirname(path.abspath(__file__))

class Extended:
    def __init__(self):
        self.cur_data = None

    def read_file(self, file_name):
        """ read csv file """
        file = pd.read_csv(cur_path + file_name)
        


if __name__ == "__main__":
    extend = Extended()
    extend.read_file("/Papers/AAAI/aaai_2010.csv")


