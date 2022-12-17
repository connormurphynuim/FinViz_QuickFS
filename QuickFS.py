import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
#import pandas as pd
from bs4 import BeautifulSoup
#import csv

in_url = 'https://quickfs.net/company/CNXC:US/'
options = ChromeOptions()
options.headless = True
# connect to Chrome browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

# input finviz url and connect to page
driver.get(in_url)
time.sleep(10)
content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

for element in soup.findAll('div', attrs={'class':'dropdownLabel'}):
    print(element)


driver.quit()
#elements = driver.find_elements(By.CLASS_NAME, "labelCell")


#for element in elements:
    #print(element)



# <td class="labelCell">Revenue</td>

