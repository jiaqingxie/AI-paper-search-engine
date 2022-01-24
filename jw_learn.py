import argparse
import os
import pandas as pd
from retrieve_titles import *

cur_path = path.dirname(path.abspath(__file__))
chromedriver_path = cur_path + "//chromedriver"

option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)

driver.get("https://www.kdd.org/kdd2020/accepted-papers")

pdfurllist = []
pdfnamelist = []
abslist = []
autlist = []
element_list = driver.find_elements_by_xpath("//span[@class='d-block u-link-v5 g-font-weight-600 g-mb-3']/a")
for e in element_list:
    url = e.get_attribute("href")
    driver.get(url)
    l2 = driver.find_elements_by_xpath("//div[@class='col-lg-9']/a")
    print(l2)
    url2 = l2.get_attribute("href") # acm link
    driver.get(url2)
    l3 = driver.find_elements_by_xpath("//li[@class='pdf-file']/a")
    pdf_url = l3.get_attribute("href")
    pdfurllist.append(pdf_url)
    
    l4 = driver.find_elements_by_xpath("//h1[@class='citation__title']").text()
    print(l4)
    driver.back
    driver.back
    
    break