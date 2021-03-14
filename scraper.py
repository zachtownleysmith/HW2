import pandas as pd
import requests
from bs4 import BeautifulSoup


def scraper(url):
    site_text = requests.get(url).text
    company_info = BeautifulSoup(site_text, 'lxml').find_all('li')
    company_name = ''
    company_purpose = ''

    for info in company_info:
        if 'Name:' in info.text:
            company_name = info.text.replace('Name: ', '')
        if 'Purpose:' in info.text:
            company_purpose = info.text.replace('Purpose: ', '')
    company_df = pd.DataFrame([[company_name, company_purpose]], columns=["Name", "Purpose"])
    return company_df


def loop_scraper(call_num, url):
    scraped_df = pd.DataFrame(data=None, columns=["Name", "Purpose"])
    for i in range(call_num):
        scraped_df = scraped_df.append(scraper(url=url), ignore_index=True)
    scraped_df.to_csv('output.csv', index=False)


if __name__ == '__main__':
    loop_scraper(50, url='http://18.206.38.144:8000/random_company')

