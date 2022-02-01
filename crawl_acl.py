#%%
from bs4 import BeautifulSoup
import json
import numpy as np
import requests
import os, io
from tqdm import tqdm
from PyPDF2 import PdfFileReader
import pandas as pd

#%%
acl_url_list = dict()
for i in range(10, 22):
    acl_url_list[i] = "https://aclanthology.org/events/acl-20" + str(i)
    
#%%
os.makedirs('Papers/ACL', exist_ok=True)  
#%%
for year in acl_url_list.keys():
    page_url = acl_url_list[year]
    conf_name = 'acl_20' + str(year)
    if year == 20:
        conf_id = "2020-acl-main"
    elif year == 21:
        conf_id = "2021-acl-long"
    else:
        conf_id = "p" + str(year) + "-1"
        
    html_doc = requests.get(page_url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    main_papers = soup.find('div', id = conf_id).find_all('p', class_ = "d-sm-flex")
    
    paper_list = []
    for paper_p in tqdm(main_papers[1:]):
        pdf_url = paper_p.contents[0].contents[0]['href']
        paper_url = pdf_url.replace(".pdf","/")
        paper_doc = requests.get(paper_url).text
        soup2 = BeautifulSoup(paper_doc, 'html.parser')
        if year < 17:
            abstract = "None"
        else:
            abstract = soup2.find("div",class_="row acl-paper-details").find_all("span")[0].get_text()  
        paper_span = paper_p.contents[-1]
        assert paper_span.name == 'span'
        paper_a = paper_span.strong.a
        title = paper_a.get_text()
        url = "https://aclanthology.org" + paper_a['href']
        people = [paper_p.contents[1].contents[i].get_text() for i in range(len(paper_p.contents[1])) if i%2==0 and i!=0]
        
        thispaper = {"conference": "acl", "url": pdf_url, "title": title, "authors": ",".join(people), "abstract": abstract}
        paper_list.append(thispaper)

    df = pd.DataFrame(data=paper_list)
    df.to_csv("Papers/ACL/acl_20" + str(year) + ".csv", index=False)

    # --------------------------------------------------------------------------------
    # Write the json file for better fetching
    # with open("Papers/ACL/" + conf_name + '.json', 'w', encoding='utf8') as f:
    #     json.dump(paper_list, f, indent = 2, ensure_ascii= False)

    # Below is the code to crawl each .pdf file into a folder called acl_2020_main. 
    # At this stage, we only expect the title, url, pdf_url, author and abstract 
    # from each paper, so below code is commented but it could be useful in later 
    # implementation. 
    # # %%
    # print('There are total {} papers'.format(len(paper_list)))

    # if not os.path.exists(conf_name):
    #     os.mkdir(conf_name)

    # illegal_chr = r'\/:*?<>|'
    # table = ''.maketrans('', '', illegal_chr)
    # for i, paper in tqdm(list(enumerate(paper_list))):
    #     r = requests.get(paper[2])
    #     n = '{}.{}.pdf'.format(i+1, paper[0].translate(table))
    #     with open('./{}/{}'.format(conf_name, n), 'wb') as f:
    #         f.write(r.content)