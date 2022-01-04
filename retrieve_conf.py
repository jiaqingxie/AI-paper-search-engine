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
icml_url_list = [
    "http://proceedings.mlr.press/v139/",   # ICML-21
    "https://proceedings.mlr.press/v119/",  # ICML-20
    "http://proceedings.mlr.press/v97/",    # ICML-19
    "https://proceedings.mlr.press/v80/",   # ICML-18
    "https://proceedings.mlr.press/v70/",   # ICML-17
    "https://proceedings.mlr.press/v48/",   # ICML-16
    "https://proceedings.mlr.press/v37/",   # ICML-15
    "https://proceedings.mlr.press/v32/",   # ICML-14
    "https://proceedings.mlr.press/v28/"    # ICML-13
]

aaai_url_list = [
    "https://aaai.org/Library/AAAI/aaai10contents.php" # AAAI-10

]

chromedriver_path = cur_path + "\chromedriver.exe"
root = cur_path + "\Papers\ICML"
os.makedirs(root, exist_ok=True)


if __name__ == "__main__":
    args = parse()
    # open PMLR page
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)
    retreive = globals()['retrieve_from_' + args.conf]
    year = 2021
    for conference_url in icml_url_list:
        driver.get(conference_url)
        pdfurllist, pdfnamelist, abslist = retreive(driver)
        assert len(pdfurllist) == len(pdfnamelist)
        # write to excel
        df = pd.DataFrame({'url': pdfurllist,
                           'title': pdfnamelist,
                           'abstract': abslist
                           })
        df.to_csv('%s\\icml_%s.csv' % (root, year), index=False)
        year -= 1
