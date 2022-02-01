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
emnlp_url_list = dict()
for i in range(10, 22):
    emnlp_url_list[i] = "https://aclanthology.org/events/emnlp-20" + str(i)
#%%
os.makedirs('Papers/EMNLP', exist_ok=True)  
#%%
for year in emnlp_url_list.keys():
    page_url = emnlp_url_list[year]
    conf_name = 'emnlp_20' + str(year)
    if year < 20:
        conf_id = "d" + str(year) + "-1"
    else:
        conf_id = "20" + str(year) + "-emnlp-main"
        
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
            abstract = soup2.find("div",class_="card-body acl-abstract").find_all("span")[0].get_text() 
 
        paper_span = paper_p.contents[-1]
        assert paper_span.name == 'span'
        paper_a = paper_span.strong.a
        title = paper_a.get_text()
        url = "https://aclanthology.org" + paper_a['href']
        people = [paper_p.contents[1].contents[i].get_text() for i in range(len(paper_p.contents[1])) if i%2==0 and i!=0]
        
        thispaper = {"conference": "emnlp", "url": pdf_url, "title": title, "authors": ",".join(people), "abstract": abstract}
        paper_list.append(thispaper)

    df = pd.DataFrame(data=paper_list)
    df.to_csv("Papers/EMNLP/emnlp_20" + str(year) + ".csv", index=False)