import pymysql
import pandas as pd
from os import path
import os
import glob

par_path = path.abspath(path.dirname(os.getcwd()))


class Mysql_csv(object):
    def __init__(self):
        self.connect = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="password",database="ai_paper")
        self.cursor = self.connect.cursor()
        self.conf = ["aaai", "iccv", "icml", "cvpr", "iclr", "kdd", "sigir", "www", "acl", "emnlp", "icra", "neurips"]
        self.data = pd.DataFrame([])

    def __del__(self):
        self.connect.close()
        self.cursor.close()
        
    def read_csv_colnmus(self):
        
        for conf in self.conf:
            print(conf)
            if conf != "neurips":
                extended_list = glob.glob(par_path + '/Papers/{}/{}_[0-9]*_extended.csv'.format(conf.upper(), conf))
                count = 0
                df1 = None
                for sig_csv in extended_list:
                    if count == 0:
                        df1 = pd.read_csv(sig_csv,encoding="utf-8")
                    else:
                        df2 = pd.read_csv(sig_csv,encoding="utf-8")
                        df1 = df1.append(df2, ignore_index=True)
                        df1  = df1 .where((pd.notnull(df1)), "NULL")
                    count+=1
            else:
                extended_list = glob.glob(par_path + '/Papers/NeurIPS/{}_[0-9]*_extended.csv'.format(conf))       
                count = 0
                df1 = None
                for sig_csv in extended_list:
                    if count == 0:
                        df1 = pd.read_csv(sig_csv,encoding="utf-8")
                    else:
                        df2 = pd.read_csv(sig_csv,encoding="utf-8")
                        df1 = df1.append(df2, ignore_index=True)
                        df1  = df1 .where((pd.notnull(df1)), "NULL")
                    count+=1
                
                     
            if self.data.empty:
                self.data = df1
            else:
                self.data = self.data.append(df1, ignore_index = True)
                       
        return self.data
        
    def read_csv_values(self):
        data_3 = list(self.data.values)
        return data_3
        
    def write_mysql(self):
        for i in self.read_csv_values(): 
            data_6 = tuple(i)
            sql = """insert into ai_paper_db values{}""".format(data_6)
            self.cursor.execute(sql)
            self.commit()
        print("\nComplete")
        
    def commit(self):
        self.connect.commit()
        
    def create(self):
        query="drop table if exists ai_paper_db;"
        self.cursor.execute(query)
        data_2 = self.read_csv_colnmus()
        sql = "CREATE TABLE ai_paper_db(conference varchar(63) not null, url varchar(512) not null, title varchar(2047) not null, authors varchar(4096) not null, abstract varchar(8192) not null, citations varchar(63) not null);"
        self.cursor.execute(sql)
        self.commit()

    def run(self):
        self.create()
        self.write_mysql()


def main():
    sql = Mysql_csv()
    sql.run()
if __name__ == '__main__':
    main()

