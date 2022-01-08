import argparse
import os
import pandas as pd
from retrieve_titles import *


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', type=str, help='conference name', required=True)
    arg = parser.parse_args()
    return arg


cur_path = path.dirname(path.abspath(__file__))

neurips_url_list = [
    # collect papers from 2010 - 2021
    "https://proceedings.neurips.cc/paper/" + str(2021-i) for i in range(0, 12)
]

cvpr_url_list = [
	# collect papers from 2013 - 2021
    "https://openaccess.thecvf.com/CVPR" + str(2021-i) for i in range(0, 9)
]

iccv_url_list = [
    "https://openaccess.thecvf.com/ICCV" + str(2021-i) for i in range(0, 9, 2)
]

icml_url_list = [
	# collect papers from 2013 - 2021
    "http://proceedings.mlr.press/v139/",  # ICML-21
    "https://proceedings.mlr.press/v119/",  # ICML-20
    "http://proceedings.mlr.press/v97/",  # ICML-19
    "https://proceedings.mlr.press/v80/",  # ICML-18
    "https://proceedings.mlr.press/v70/",  # ICML-17
    "https://proceedings.mlr.press/v48/",  # ICML-16
    "https://proceedings.mlr.press/v37/",  # ICML-15
    "https://proceedings.mlr.press/v32/",  # ICML-14
    "https://proceedings.mlr.press/v28/"  # ICML-13
]

aaai_url_list = [
    "https://aaai.org/Library/AAAI/aaai10contents.php"  # AAAI-10

]
chromedriver_path = cur_path + "//chromedriver"



if __name__ == "__main__":
    args = parse()
    # open PMLR page
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)
    retreive = globals()['retrieve_from_' + args.conf]
    years = []
    
    root = None
    if args.conf == 'cvpr':
        url_list = cvpr_url_list
        root = cur_path  + "//Papers//CVPR"
    elif args.conf == 'icml':
        url_list = icml_url_list
        root = cur_path  + "//Papers//ICML"
    elif args.conf == 'iccv':
        url_list = iccv_url_list
        root = cur_path  + "//Papers//ICCV"
    elif args.conf == 'neurips':
        url_list = neurips_url_list
        root = cur_path  + "//Papers//NeurIPS"       
    os.makedirs(root, exist_ok=True)
    
    year = 2021
    for conference_url in url_list:
        driver.get(conference_url)
        pdfurllist, pdfnamelist, abslist, autlist = retreive(driver, year)
        conf = [args.conf for i in range(len(pdfurllist))]
        assert len(pdfurllist) == len(pdfnamelist)
        # write to excel
        df = pd.DataFrame({'conference': conf,
                           'url': pdfurllist,
                           'title': pdfnamelist,
                           'authors': autlist,
                           'abstract': abslist
                           })
        df.to_csv('%s//%s_%s.csv' % (root, args.conf, year), index=False)
        if args.conf != "iccv":
            year -= 1
        else:
            year -= 2
