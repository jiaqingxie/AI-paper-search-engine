from os import path
from selenium import webdriver

cur_path = path.dirname(path.abspath(__file__))
chromedriver_path = cur_path + "/chromedriver"

option = webdriver.ChromeOptions()
option.add_argument("headless")

# def retrieve_from_siggraph(driver):
#     pdfurllist =  []
#     pdfnamelist = []
#     import time
#     elementllist =  driver.find_elements_by_class_name('toc__section')[1:-2]
#     for i, section in enumerate(elementllist):
#         section.find_element_by_partial_link_text('SESSION').click()
#         time.sleep(3)
#         # print(session_name)
#         for j, paper_element in enumerate(section.find_elements_by_class_name('issue-item__content')):
#             paper_name = paper_element.find_element_by_xpath('div/h5').text
#             pdf_url = paper_element.find_element_by_class_name('red').get_attribute('href')

#             pdfnamelist.append(paper_name)
#             pdfurllist.append(pdf_url)

#     return pdfurllist, pdfnamelist


def retrieve_from_siggraph(driver):
    pdfurllist = []
    pdfnamelist = []
    import time
    elementllist = driver.find_elements_by_class_name('accordion-tabbed')[1].find_elements_by_class_name('toc__section')
    for i, section in enumerate(elementllist):
        section.click()
        time.sleep(3)
        print('\n', section.text)
        for j, paper_element in enumerate(section.find_elements_by_class_name('issue-item__content')):
            paper_name = paper_element.find_element_by_xpath('div/h5').text
            pdf_url = paper_element.find_element_by_class_name('red').get_attribute('href')
            print('\t', paper_name)
            pdfnamelist.append(paper_name)
            pdfurllist.append(pdf_url)

    return pdfurllist, pdfnamelist


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


def retrieve_from_iccv(driver):
    pdfurllist = []
    pdfnamelist = []

    title_element_list = driver.find_elements_by_class_name('ptitle')
    url_element_list = driver.find_elements_by_partial_link_text('pdf')
    for i, element in enumerate(url_element_list):
        pdfnamelist.append(title_element_list[i].text)
        pdfurllist.append(url_element_list[i].get_attribute('href'))
    return pdfurllist, pdfnamelist


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
def retrieve_from_neurips(driver):
    pdfurllist = []
    pdfnamelist = []
    elementllist = driver.find_elements_by_tag_name('li')[2:]
    for i, element in enumerate(elementllist):
        pdfnamelist.append(elementllist[i].find_elements_by_xpath('a')[0].text)
        pdfurllist.append(
            elementllist[i].find_elements_by_xpath('a')[0].get_attribute('href').replace('hash', 'file', 1). \
                replace('Abstract.html', 'Paper.pdf', 1))
    return pdfurllist, pdfnamelist

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

def retrieve_from_kdd(driver, year):
    pdfurllist = []
    pdfnamelist = []
    abslist = []
    autlist = []
    if year > 2020:
        element_list = driver.find_elements_by_xpath("//div[@class='media-body']")
    else:
        element_list = driver.find_elements_by_xpath("//span[@class='d-block u-link-v5 g-font-weight-600 g-mb-3']/a")
    print(element_list)
    # return pdfurllist, pdfnamelist, abslist, autlist
    

#def retrieve_from_www():
    