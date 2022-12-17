import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

#Account info, two lined file with email address and password
f = open("QuickFSAccountInfo", "r")
email = f.readline()
password = f.readline()
f.close()

#Input url
in_url = 'https://quickfs.net'

#Driver and browser options
options = ChromeOptions()
options.headless = True

# connect to Chrome browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

# input finviz url and connect to page
driver.get(in_url)
#time.sleep(3)

#Click sign in button
sign_in_page = driver.find_element(by=By.ID,value='top-nav-auth-links-sign-in')
sign_in_page.click()
#time.sleep(3)

#Pass in input variables
driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[3]/div/input').send_keys(email)
driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[4]/div/input').send_keys(password)

# Find and click sign in button
sign_in_button = driver.find_element(by=By.ID, value='submitLoginFormBtn')
sign_in_button.click()
time.sleep(2)

#Pass in company ticker to search and click search
driver.find_element(by=By.XPATH, value='/html/body/app-root/user-logged-in-home/app-header-main/header/div/div/div[2]/div/app-search/div/div[1]/input').send_keys('CNXC')
driver.find_element(by=By.XPATH, value='//*[@id="searchSubmitBtn"]').click()
#Wait for page to load
time.sleep(5)
#Capture overview page content
content_overview = driver.page_source

#Click on dropdown and then click on Income Statement
click_dropdown = driver.find_element(By.CLASS_NAME, value='btn-group')
click_dropdown.click()
click_income = driver.find_element(By.ID, value='is')
click_income.click()
#Wait for page to load
time.sleep(5)
#Capture income statement page content
content_income = driver.page_source

#Convert overview content to soup and confirm its and overview
over_soup = BeautifulSoup(content_overview, 'html.parser')
print('Overview Soup')
for element in over_soup.findAll('div', attrs={'class':'dropdownLabel'}):
    print(element)

#Convert income statement content to soup and confirm its and income statement
income_soup = BeautifulSoup(content_income, 'html.parser')
print('Income Soup')
for element in income_soup.findAll('div', attrs={'class':'dropdownLabel'}):
    print(element)


#Close driver
driver.quit()
