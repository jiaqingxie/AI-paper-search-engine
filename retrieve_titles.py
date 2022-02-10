from os import path
from selenium import webdriver
import time

cur_path = path.dirname(path.abspath(__file__))
chromedriver_path = cur_path + "/chromedriver"

option = webdriver.ChromeOptions()
option.add_argument("headless")


def retrieve_from_aaai(driver, year):
    pass

def retrieve_from_iclr(driver, year):
    pass


def retrieve_from_icra(driver, year):
    driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)
    pub_list = driver.find_elements_by_class_name("publ-list")
    
    abslist = []
    autlist_ = []
    pdfnamelist = []
    pdfurllist = []
    
    for num_sec, pub_sec in enumerate(pub_list):
        pubs = pub_sec.find_elements_by_xpath('li')[1:]
        for pub in pubs:
            try:
                link = pub.find_element_by_xpath('nav/ul/li[1]/div[1]/a')
            except:
                continue
            url = link.get_attribute('href')
            driver2.get(url)
            title = driver2.find_element_by_xpath('//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span').text ## title
            pdfnamelist.append(title)
            print(title)
            
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
    return pdfurllist, pdfnamelist, abslist, autlist_
        
                
               


def retrieve_from_www(driver, year):
    driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)
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
            authors_ = ''
            for author in authors:
                tmp = ''
                try:
                    tmp = author.find_element_by_xpath('a/span/div/span/span').text
                    driver2.implicitly_wait(5)
                except:
                    tmp = ''
       
                authors_ = authors_ + tmp + ', '

            # abstract
            try:
                abstract = driver2.find_element_by_class_name('abstractSection')
                driver2.implicitly_wait(2)
                
                abstract_ = abstract.find_element_by_xpath('p').text
                driver2.implicitly_wait(2)
                pdfurl = driver2.find_element_by_class_name('pdf-file').find_element_by_xpath('a').get_attribute('href')
                driver2.implicitly_wait(2)
                title = driver2.find_element_by_class_name('citation__title')
                driver2.implicitly_wait(2)
                pdfnamelist.append(title.text)
                autlist.append(authors_)
                abslist.append(abstract_)
                pdfurllist.append(pdfurl)
            except:
                continue
             
    return pdfurllist, pdfnamelist, abslist, autlist
    
    
def retrieve_from_kdd(driver, year):
    driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)
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
            authors_ = ''
            for author in authors:
                tmp = ''
                try:
                    tmp = author.find_element_by_xpath('a/span/div/span/span').text
                    driver2.implicitly_wait(5)
                except:
                    tmp = ''
       
                authors_ = authors_ + tmp + ', '

            
            try:
                title = driver2.find_element_by_class_name('citation__title')
                pdfnamelist.append(title.text)
            except:
                continue
                
            try:
                abstract = driver2.find_element_by_class_name('abstractSection')
                abstract_ = abstract.find_element_by_xpath('p').text
                abslist.append(abstract_)
            except:
                abslist.append("None")
            
            try: 
                pdfurl = driver2.find_element_by_class_name('pdf-file').find_element_by_xpath('a').get_attribute('href')
                driver2.implicitly_wait(5)
                pdfurllist.append(pdfurl)
            except:
                pdfurllist.append("None")
                
            autlist.append(authors_)
                
             
    return pdfurllist, pdfnamelist, abslist, autlist

def retrieve_from_sigir(driver, year):
    driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)
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
            authors_ = ''
            for author in authors:
                tmp = ''
                try:
                    tmp = author.find_element_by_xpath('a/span/div/span/span').text
                    driver2.implicitly_wait(5)
                except:
                    tmp = ''
       
                authors_ = authors_ + tmp + ', '

            
            try:
                title = driver2.find_element_by_class_name('citation__title')
                pdfnamelist.append(title.text)
            except:
                continue
                
            try:
                abstract = driver2.find_element_by_class_name('abstractSection')
                abstract_ = abstract.find_element_by_xpath('p').text
                abslist.append(abstract_)
            except:
                abslist.append("None")
            
            try: 
                pdfurl = driver2.find_element_by_class_name('pdf-file').find_element_by_xpath('a').get_attribute('href')
                driver2.implicitly_wait(5)
                pdfurllist.append(pdfurl)
            except:
                pdfurllist.append("None")
                
            autlist.append(authors_)
                
             
    return pdfurllist, pdfnamelist, abslist, autlist

#debug
def retrieve_from_iclr(driver):
    pdfurllist = []
    pdfnamelist = []

    # three sections: oral, spotlight, poster
    for num_section, section in enumerate(['Oral', 'Spotlight', 'Poster']):
        driver.find_element_by_partial_link_text(section).click()
        elementllist = driver.find_elements_by_tag_name('h4')[1:]
        for i, element in enumerate(elementllist):
            pdfnamelist.append(elementllist[i].text)
            pdfurllist.append(elementllist[i].find_elements_by_xpath('a')[1].get_attribute('href'))

    return pdfurllist, pdfnamelist


def retrieve_from_iccv(driver, year):
    pdfurllist = []
    pdfnamelist = []
    autlist = []
    abslist = []
    y_to_d = {2019: 4, 2021: 2}
    loo = 1 if year <= 2018 else y_to_d[year]
    driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)
    for day in range(loo):
        if year >= 2018:
            driver.find_elements_by_xpath('//body/div[3]/dl/dd/a')[day].click()
        title_element_list = driver.find_elements_by_class_name('ptitle')
        url_element_list = driver.find_elements_by_partial_link_text('pdf')
        for i, element in enumerate(url_element_list):
            driver2.get(driver.find_element_by_link_text(title_element_list[i].text).get_attribute('href'))
            rel_path = '//body/div[3]/dl/div[2]/b/i' if year == 2021 else '//body/div[3]/dl/dd/div[2]/b/i'
            aut_element = driver2.find_element_by_xpath(rel_path)
            autlist.append(aut_element.text)
            abslist.append(driver2.find_element_by_id('abstract').text)
            pdfnamelist.append(title_element_list[i].text)
            pdfurllist.append(url_element_list[i].get_attribute('href'))
        if year >= 2018:
            driver.back()

    return pdfurllist, pdfnamelist, abslist, autlist


def retrieve_from_icml(driver, year):
    abslist = []
    autlist = []
    pdfurllist = []
    pdfnamelist = []
    elementllist = driver.find_elements_by_class_name('title')
    authorlist = driver.find_elements_by_class_name('authors')
    url_element_list = driver.find_elements_by_link_text('Download PDF')
    abs_element_list = driver.find_elements_by_link_text('abs')
    driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)
    for i, element in enumerate(url_element_list):
        driver2.get(abs_element_list[i].get_attribute('href'))
        abs_element = driver2.find_element_by_class_name('abstract')
        abslist.append(abs_element.text)
        autlist.append(authorlist[i].text)
        pdfnamelist.append(elementllist[i].text)
        pdfurllist.append(url_element_list[i].get_attribute('href'))
    return pdfurllist, pdfnamelist, abslist, autlist


# debug
def retrieve_from_neurips(driver, year):
    pdfurllist = []
    pdfnamelist = []
    autlist = []
    abslist = []
    elementllist = driver.find_elements_by_tag_name('li')[2:]
    driver2 = webdriver.Chrome(options = option, executable_path=chromedriver_path)
    for i, element in enumerate(elementllist):
        driver2.get(driver.find_element_by_link_text(elementllist[i].find_elements_by_xpath('a')[0].text).get_attribute('href'))
        driver2.implicitly_wait(0.5)
        if year != 2021:
            autlist.append(driver2.find_element_by_xpath('//body/div[2]/div/p[2]').text)
            try:
                abslist.append(driver2.find_element_by_xpath('//body/div[2]/div/p[4]').text)
            except:
                abslist.append(driver2.find_element_by_xpath('//body/div[2]/div/p[3]').text)
        else:
            autlist.append(driver2.find_element_by_xpath('//body/div[2]/div/p[3]').text)
            try:
                abslist.append(driver2.find_element_by_xpath('//body/div[2]/div/p[5]').text)
            except:
                abslist.append(driver2.find_element_by_xpath('//body/div[2]/div/p[4]').text)
        pdfnamelist.append(elementllist[i].find_elements_by_xpath('a')[0].text)
        print(elementllist[i].find_elements_by_xpath('a')[0].text)
        pdfurllist.append(
            elementllist[i].find_elements_by_xpath('a')[0].get_attribute('href').replace('hash', 'file', 1). \
                replace('Abstract.html', 'Paper.pdf', 1))
        driver2.back()
        
    return pdfurllist, pdfnamelist, abslist, autlist


def retrieve_from_cvpr(driver, year):
    pdfurllist = []
    pdfnamelist = []
    autlist = []
    abslist = []
    y_to_d = {2018: 3, 2019: 3, 2020: 3, 2021: 5}
    loo = 1 if year <= 2018 else y_to_d[year]
    driver2 = webdriver.Chrome(options=option, executable_path=chromedriver_path)
    for day in range(loo):
        if year >= 2018:
            driver.find_elements_by_xpath('//body/div[3]/dl/dd/a')[day].click()
        title_element_list = driver.find_elements_by_class_name('ptitle')
        url_element_list = driver.find_elements_by_partial_link_text('pdf')
        for i, element in enumerate(url_element_list):
            driver2.get(driver.find_element_by_link_text(title_element_list[i].text).get_attribute('href'))
            rel_path = '//body/div[3]/dl/div[2]/b/i' if year == 2021 else '//body/div[3]/dl/dd/div[2]/b/i'
            aut_element = driver2.find_element_by_xpath(rel_path)
            autlist.append(aut_element.text)
            abslist.append(driver2.find_element_by_id('abstract').text)
            pdfnamelist.append(title_element_list[i].text)
            pdfurllist.append(url_element_list[i].get_attribute('href'))
        if year >= 2018:
            driver.back()

    return pdfurllist, pdfnamelist, abslist, autlist
