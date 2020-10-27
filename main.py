import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options_chrom
import subprocess
import os

#checks if firefox browser is installed - TODO
#does it really need firefox to runn?
#   -first part no. -CzMeanwell
#   -second part is resulting in error for PC without firefox. -GME.cz

#try:
#    subprocess.run("start chrom", shell=True)
#except OSError as e:
#    if e.errno == os.errno.ENOENT:
#        print('end')


# http://www.networkinghowtos.com/howto/common-user-agent-list/
HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Accept-Language': 'en-US, en;q=0.5'})

# list of competitors webshop sites
competitors = ('trackers/MEAN_WELL.csv', 'trackers/TME.csv', 'trackers/GME.csv')


#######################################################################################################################
###################################################    Meanwell     ###################################################
#######################################################################################################################

# imports a csv file with the url's to scrape
prod_tracker = pd.read_csv(competitors[0], sep=';')
prod_tracker_URLS = prod_tracker.url
print(prod_tracker_URLS)

# creating dataframe
tracker_log = pd.DataFrame()
now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')

# repeat for each url
for x, url in enumerate(prod_tracker_URLS):
    # fetch the url
    page = requests.get(url, headers=HEADERS)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(page.content, features="lxml")
    print(page)

    # Name reading
    Meanwell_title = soup.find_all('h1')[0].text
    print(Meanwell_title)

    # Price reading
    meanwell_price = soup.find_all('span', class_='price-novat fleft old-variants-price-replace')[0].text
    meanwell_price = float(meanwell_price.replace('\xa0', '').replace('Kč', ''))
    print(meanwell_price)

    # creating a log filed with price and name
    log = pd.DataFrame({'date': now.replace('h', ':').replace('m', ''),
                        'url': url,
                        'title': Meanwell_title,
                        'price': meanwell_price,}, index=[x])

    # append result
    tracker_log = tracker_log.append(log)

# save results to excel
tracker_log.to_excel('results/MEAN_WELL_results_{}.xlsx'.format(now), index=False)
print('end of search for MEAN_WELL CZECH')

#######################################################################################################################
#####################################################    GME     ######################################################
#######################################################################################################################
# imports a csv file with the url's to scrape
prod_tracker = pd.read_csv(competitors[2], sep=';')
prod_tracker_URLS = prod_tracker.url
print(prod_tracker_URLS)

# magic
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(options=options)


# creating dataframe
tracker_log = pd.DataFrame()
now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')

# repeat for each url
for x, url in enumerate(prod_tracker_URLS):
    # fetch the url
    driver.get(url)
    page = driver.page_source


    # create the object that will contain all the info in the url
    soup = BeautifulSoup(page, 'lxml')

    # Name reading
    GME_title = soup.find_all('h1')[0].text
    print(GME_title)

    # Price reading
    GME_price = soup.find_all('span', class_='price col col-6')[-1].text
    GME_price = float(GME_price.replace('\xa0', '').replace('Kč', ''))

    #DPH coversion
    GME_price=round(GME_price*0.79,2)
    print(GME_price)

    # creating a log filed with price and name
    log = pd.DataFrame({'date': now.replace('h', ':').replace('m', ''),
                        'url': url,
                        'title': GME_title,
                        'price': GME_price,}, index=[x])

    # append result
    tracker_log = tracker_log.append(log)

#kill driver
driver.quit()

# save results to excel
tracker_log.to_excel('results/GME_results_{}.xlsx'.format(now), index=False)
print('end of search for GME')

#######################################################################################################################
#####################################################    TME     ######################################################
#######################################################################################################################
