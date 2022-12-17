from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import csv
import time

# fixed constants
url_base = 'https://finviz.com/'
url_ext = '&r='
url = 'https://finviz.com/screener.ashx?v=151&f=cap_midover,fa_curratio_o1,fa_debteq_u1,fa_div_pos,fa_pe_u35,fa_quickratio_o1,fa_roe_pos&ft=2'

def ConnectNGetSoup(in_url):
    # connect to Chrome browser
    options = ChromeOptions()
    options.headless = False
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

    # input finviz url and connect to page
    driver.get(in_url)

    content = driver.page_source
    # convert page to soup
    soup = BeautifulSoup(content, 'html.parser')
    return soup

def NumCompanyInScope(in_soup):
    for total in in_soup.findAll(attrs={'width': '140', 'align': 'left', 'valign': 'bottom', 'class': 'count-text'}):
        # print('total',total.getText().split(' '))
        num_in_scope = int(total.getText().split(' ')[1])

    return num_in_scope

def PageUrls(num_in_scope):
    # Create list of pages that will need to be queried

    url_add_on = [i for i in range(21,num_in_scope,20)]
    url_pages = [url+url_ext+str(i) for i in url_add_on]
    url_pages.insert(0,url)

    return url_pages


def CreateCsv():
    headers = ['Company Name', 'Ticker', 'Sector', 'Industry', 'Country', 'Index', 'P/E', 'EPS (ttm)', 'Insider Own'
        , 'Shs Outstand', 'Perf Week', 'Market Cap', 'Forward P/E', 'EPS next Y', 'Insider Trans', 'Shs Float',
               'Perf Month'
        , 'Income', 'PEG', 'EPS next Q', 'Inst Own', 'Short Float / Ratio', 'Perf Quarter', 'Sales', 'P/S', 'EPS this Y'
        , 'Inst Trans', 'Short Interest', 'Perf Half Y', 'Book/sh', 'P/B', 'ROA', 'Target Price', 'Perf Year', 'Cash/sh'
        , 'P/C', 'EPS next 5Y', 'ROE', '52W Range', 'Perf YTD', 'Dividend', 'P/FCF', 'EPS past 5Y', 'ROI', '52W High'
        , 'Beta', 'Dividend %', 'Quick Ratio', 'Sales past 5Y', 'Gross Margin', '52W Low', 'ATR', 'Employees'
        , 'Current Ratio', 'Sales Q/Q', 'Oper. Margin', 'RSI (14)', 'Volatility', 'Optionable', 'Debt/Eq', 'EPS Q/Q'
        , 'Profit Margin', 'Rel Volume', 'Prev Close', 'Shortable', 'LT Debt/Eq', 'Earnings', 'Payout', 'Avg Volume'
        , 'Price', 'Recom', 'SMA20', 'SMA50', 'SMA200', 'Volume', 'Change']

    f = open('FinvizExtract.csv', 'w', newline='')

    writer = csv.writer(f)

    writer.writerow(headers)

    f.close()

def WriteCsv(row):

    f = open('FinvizExtract.csv', 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()

def SourcePages(url_pages):
    # Create empty list for temp values
    temp_list = []
    # For loop to cycle through the pages
    for page in url_pages:
        #C reate temp soup of page selected
        temp_soup = ConnectNGetSoup(page)

        # Extract rows where reference url is located
        for screenbody in temp_soup.findAll(attrs={'class': 'screener-body-table-nw', 'align': 'right'}):
            # isolate tag with ref url
            for dtag in screenbody.findAll('a', attrs={'class': 'screener-link'}):
                # form full url and add to list
                temp_list.append(url_base + dtag['href'])

    # do a list-set-list to remove duplicates
    source_page = list(set(temp_list))
    # clear temp list
    temp_list.clear()

    return source_page


def CompanyData(in_url):
    # Connect to individual company page
    sub_soup = ConnectNGetSoup(in_url)

    # extract ticker and company name
    ticker = sub_soup.findAll(attrs={'class': 'fullview-ticker', 'id': 'ticker'})[0].getText()
    company_name = sub_soup.findAll(attrs={'target': '_blank', 'class': 'tab-link'})[0].getText()

    # extract Sector, Industry and Country
    for descriptor in sub_soup.findAll(attrs={'align': 'center', 'class': 'fullview-links'}):
        comp_desc_l = [dtag.getText() for dtag in descriptor.findAll('a', attrs={'class': 'tab-link'})]

    # combine in company descriptor data
    comp_desc_dict = {'Company Name': company_name, 'Ticker': ticker, 'Sector': comp_desc_l[0],
                      'Industry': comp_desc_l[1], 'Country': comp_desc_l[2]}

    # Create list to hold raw tables data
    raw_desc_info = []

    # Get table rows then extract from the columns, insert into raw data table
    for row in sub_soup.findAll(attrs={'class': 'table-dark-row'}):
        for column in row.findAll('td'):
            raw_desc_info.append(column.getText())

    # Create list of data descriptors
    data_desc = [i for i in raw_desc_info[0:144:2]]
    # Create list of data values
    data_value = [i for i in raw_desc_info[1:144:2]]

    # create dictionary for data
    data_pairs = dict(zip(data_desc, data_value))

    data_pairs = dict(zip(data_desc, data_value))

    merged_dict = comp_desc_dict | data_pairs

    load_values = list(merged_dict.values())

    WriteCsv(load_values)

    #return comp_desc_dict, data_pairs




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Start of Once off functions
    soup_intial = ConnectNGetSoup(url)

    # get number of companies in scope
    num_in_scope = NumCompanyInScope(soup_intial)
    print(num_in_scope, ": companies in scope.")

    # Create list of pages that will need to be queried
    url_pages = PageUrls(num_in_scope)

    # print(url_pages)

    # End of once off functions

    # Create list of source_pages to be queried

    source_pages = SourcePages(url_pages)

    # Create Csv File for data
    CreateCsv()
    i = 1
    for s in source_pages:
        print("Starting ",i," of ",num_in_scope)
        CompanyData(s)
        print("Finished ", i, " of ", num_in_scope)
        i = i + 1
    #sub_url = 'https://finviz.com/quote.ashx?t=AMKR&ty=c&p=d&b=1'

    #x,y = CompanyData(sub_url)

    #print(x)
    #print(y)



# Connect to individual company page


# https://finviz.com/quote.ashx?t=ABM&ty=c&p=d&b=1
