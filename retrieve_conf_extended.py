import pandas as pd
from os import path
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import argparse

import undetected_chromedriver as uc
import pickle
import time


cur_path = path.dirname(path.abspath(__file__))
chromedriver_path = cur_path + "/chromedriver"

chrome_options = uc.ChromeOptions()
chrome_options.headless = False

#chrome_options2 = uc.ChromeOptions()
#chrome_options2.headless = False

driver = uc.Chrome(options=chrome_options)
#driver2 = uc.Chrome(options=chrome_options2)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', type=str, help='conference name', required=True)
    arg = parser.parse_args()
    return arg



class Extended:
    def __init__(self):
        self.cur_data = None
        self.base_url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q="
        

    def read_file(self, file_name):
        """ read csv file and save to data frame"""
        self.cur_data = pd.read_csv(cur_path + file_name)
        
    def add_extra(self):
        
        citations = []
        areas = []
        for element in self.cur_data['title']:
            #print(element)
            driver.get(self.base_url + element + "&btnG=")
            driver.implicitly_wait(8)
            try:
                loc = driver.find_element(by = By.XPATH, value = '//*[@id="gs_res_ccl_mid"]/div/div[2]/div[3]/a[3]')
                

                if "Cited" in loc.text or "cited" in loc.text:
                    citations.append(loc.text.split()[2])
                else:
                    citations.append(0)
            except:
                citations.append(0)
            """ 
            cur_areas = {}
             
            try:
                authors_link = driver.find_elements(by = By.XPATH, value = '//*[@id="gs_res_ccl_mid"]/div/div[2]/div[1]/a')
                
                for author_link in authors_link:
                    print(author_link.text)
                    url = author_link.get_attribute('href')
                    driver2.get(url)
                    driver2.implicitly_wait(8)
                    interests = driver2.find_elements(by = By.XPATH, value = '//*[@id="gsc_prf_int"]/a')
                    for inte in interests:
                        
                        if inte.text in cur_areas.keys():
                            cur_areas[inte.text] +=1   
                        else:
                            cur_areas[inte.text] = 1 
                
                areas.append(cur_areas)
                print(cur_areas)
                    
            except:
                areas.append(cur_areas)
            """
        self.cur_data['citations'] = citations
        #self.cur_data['research_areas'] = areas
                
    def write2csv(self, conf, year):
        """ write the current extended data to a new csv file"""
        self.cur_data.to_csv(cur_path + '/Papers/%s/%s_%s_extended.csv' % (conf.upper(), conf, year), index=False)


if __name__ == "__main__":
    arg = parse()
    extend = Extended()
    
    if arg.conf == "aaai":
        org_csv_file_names = [arg.conf.upper() + "/" + arg.conf + "_{}".format(str(i))+ ".csv" for i in range(2010,2022)]
    elif arg.conf == "emnlp" or "acl":
        org_csv_file_names = [arg.conf.upper() + "/" + arg.conf + "_{}".format(str(i))+ ".csv" for i in range(2010,2022)]
    elif arg.conf == "iclr":
        org_csv_file_names = [arg.conf.upper() + "/" + arg.conf + "_{}".format(str(i))+ ".csv" for i in range(2013, 2017)]
    elif arg.conf == "sigir" or arg.conf == "kdd" or arg.conf == "www":
        org_csv_file_names = [arg.conf.upper() + "/" + arg.conf + "_{}".format(str(i))+ ".csv" for i in range(2010, 2022)]
    elif arg.conf == "iccv":
        org_csv_file_names = [arg.conf.upper() + "/" + arg.conf + "_{}".format(str(i))+ ".csv" for i in range(2013, 2022, 2)]
    elif arg.conf == "cvpr":
        org_csv_file_names = [arg.conf.upper() + "/" + arg.conf + "_{}".format(str(i))+ ".csv" for i in range(2013, 2022)]
    
    
    
        
     
    
    year = 2013 if arg.conf == "iccv" or arg.conf == "cvpr" or arg.conf == "iclr" else 2010
    for item in org_csv_file_names:
        if (year == 2018 or year == 2019) and arg.conf == "aaai":
            year += 1
            continue
        else:
            extend.read_file("/Papers/{}".format(item))
            extend.add_extra()
            extend.write2csv(arg.conf, year)
            year += 1
    


