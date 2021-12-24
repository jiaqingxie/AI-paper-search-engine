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
conference_url = "http://proceedings.mlr.press/v139/"
chromedriver_path = cur_path + "\chromedriver.exe"
root = cur_path + "\Papers\ICML"
os.makedirs(root, exist_ok=True)

if __name__ == "__main__":
    # open PMLR page
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)
    driver.get(conference_url)
    retreive = globals()['retrieve_from_'+conference]
    print("Retrieving pdf urls ......")
    pdfurllist, pdfnamelist, abslist = retreive(driver)
    assert len(pdfurllist) == len(pdfnamelist)

    # write to excel
    df = pd.DataFrame({'url': pdfurllist,
                       'title': pdfnamelist,
                       'abstract': abslist
                       })
    df.to_csv('icml2021.csv', index=False)






