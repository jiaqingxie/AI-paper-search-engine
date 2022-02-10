from os import path
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
cur_path = path.dirname(path.abspath(__file__))
chromedriver_path = cur_path + "/chromedriver"

a = "https://dblp.org/db/conf/iclr/iclr2016.html"

option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)
driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)

if __name__ == "__main__":
    driver.get(a)
    pub_list = driver.find_elements_by_class_name("publ-list")[1:]
    
    abslist = []
    autlist = []
    pdfnamelist = []
    pdfurllist = []
    
    for num_sec, pub_sec in enumerate(pub_list):
        pubs = pub_sec.find_elements_by_xpath('li')
        for pub in pubs[:len(pubs)-1]:
            authors = ""  
            link = pub.find_element_by_xpath('nav/ul/li[1]/div[1]/a')
            url = link.get_attribute('href')
            driver2.get(url)
            
            content = driver2.find_element_by_id('content-inner')
            title = content.find_element_by_xpath('div/h1').text
            pdfnamelist.append(title)

            author = content.find_element_by_class_name('authors').find_elements_by_xpath('a')
            for aut in author:
                authors = authors + aut.text + ','
            autlist.append(authors)
            
            abstract = content.find_element_by_class_name('abstract').text
            abslist.append(abstract)
            
            urllink = driver2.find_element_by_xpath('//*[@id="abs-outer"]/div[2]/div[1]/ul/li[1]/a').get_attribute('href')

            
            
            
            
            
            
            
