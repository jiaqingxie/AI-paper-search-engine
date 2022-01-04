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
conference = "iclr"
iclr_url_list = [
    "https://openreview.net/group?id=ICLR.cc/2021/Conference",  # ICLR-21
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
