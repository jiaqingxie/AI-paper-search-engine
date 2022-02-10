from os import path
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
cur_path = path.dirname(path.abspath(__file__))
chromedriver_path = cur_path + "/chromedriver"

a = "https://dblp.org/db/conf/icra/icra2021.html"

option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)
driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)

if __name__ == "__main__":
    driver.get(a)
    pub_list = driver.find_elements_by_class_name("publ-list")
    
    abslist = []
    autlist_ = []
    pdfnamelist = []
    pdfurllist = []
    
    for num_sec, pub_sec in enumerate(pub_list):
        pubs = pub_sec.find_elements_by_xpath('li')[1:]
        for pub in pubs:
            link = pub.find_element_by_xpath('nav/ul/li[1]/div[1]/a')
            url = link.get_attribute('href')
            driver2.get(url)
            title = driver2.find_element_by_xpath('//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span').text ## title
            pdfnamelist.append(title)
            
            authors = driver2.find_elements_by_class_name("authors-info")
            abstract = driver2.find_elements_by_class_name("u-mb-1")[1]
            autlist = ""
            try:
                for aut in authors:
                    autlist = autlist + aut.find_element_by_xpath('span/a/span').text + ","
                autlist_.append(autlist)
            except:
                autlist_.append(autlist)
                
            try:
                abstract = abstract.find_element_by_xpath("div").text
                abslist.append(abstract)
            except:
                abslist.append("None")
                
            try:
                url = driver2.find_element_by_class_name("pdf-btn-link").get_attribute("href")
                pdfurllist.append(url)
            except:
                pdfurllist.append("None")
                
               
            
            
               
            
                

