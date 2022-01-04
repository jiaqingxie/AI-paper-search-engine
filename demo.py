from os import path
from selenium import webdriver
cur_path = path.dirname(path.abspath(__file__))
chromedriver_path = cur_path + "\chromedriver.exe"

a = "https://aaai.org/Library/AAAI/aaai10contents.php"
#16071-18033

option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(options=option, executable_path=chromedriver_path)

if __name__ == "__main__":
    driver.get(a)
    x = driver.find_elements_by_class_name('left')
    url_element_list = driver.find_elements_by_link_text("...")
    print(x[0].get_attribute('href'))

