from os import path
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
cur_path = path.dirname(path.abspath(__file__))
chromedriver_path = cur_path + "/chromedriver"

a = "https://dblp.org/db/conf/kdd/kdd2021.html"

option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)
driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)

if __name__ == "__main__":
    driver.get(a) # get kdd pub from dblp
   
    pub_list = driver.find_elements_by_class_name("publ-list")[1:]
    abslist = []
    autlist = []
    pdfnamelist = []
    pdfurllist = []
    for num_sec, pub_sec in enumerate(pub_list):
        pubs = pub_sec.find_elements_by_class_name("entry")
        for pub in pubs:
            link = pub.find_element_by_xpath('nav/ul/li[1]/div[1]/a')
            url = link.get_attribute('href')
            driver2.get(url)
            # authors
            authors = driver2.find_elements_by_class_name('loa__item')
            authors_ = ', '.join([author.find_element_by_xpath('a/span/div/span/span').text for author in authors])
            # abstract
            abstract = driver2.find_element_by_class_name('abstractSection')
            abstract_ = abstract.find_element_by_xpath('p').text
            # title
            title = driver2.find_element_by_class_name('citation__title')
            pdfnamelist.append(title)
            autlist.append(authors_)
            abslist.append(abstract_)
            pdfurllist.append("None")
            print("Yes")
            
    #return pdfurllist, pdfnamelist, abslist, autlist
            
