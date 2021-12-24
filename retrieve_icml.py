import time
import urllib
import random
import os
import requests
import pandas as pd
from selenium import webdriver
from slugify import slugify
from os import path
from retrieve_titles import *

cur_path = path.dirname(path.abspath(__file__))
conference = "icml"
icml_url_list = [
    "http://proceedings.mlr.press/v139/",  # ICML-21
    "https://proceedings.mlr.press/v119/",  # ICML-20
    "http://proceedings.mlr.press/v97/",  # ICML-19
    "https://proceedings.mlr.press/v80/",  # ICML-18
    "https://proceedings.mlr.press/v70/",  # ICML-17
    "https://proceedings.mlr.press/v48/",  # ICML-16
    "https://proceedings.mlr.press/v37/",  # ICML-15
    "https://proceedings.mlr.press/v32/",  # ICML-14
    "https://proceedings.mlr.press/v28/"  # ICML-13
]
chromedriver_path = cur_path + "\chromedriver.exe"
root = cur_path + "\Papers\ICML"
os.makedirs(root, exist_ok=True)

if __name__ == "__main__":
    # open PMLR page
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)
    retreive = globals()['retrieve_from_' + conference]
    year = 2021
    for conference_url in icml_url_list:
        driver.get(conference_url)
        pdfurllist, pdfnamelist, abslist = retreive(driver)
        assert len(pdfurllist) == len(pdfnamelist)
        # write to excel
        df = pd.DataFrame({'url': pdfurllist,
                           'title': pdfnamelist,
                           'abstract': abslist
                           })
        df.to_csv('%s\\icml_%s.csv' % (root, year), index=False)
        year -= 1
