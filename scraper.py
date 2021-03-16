import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define scraper function to return one scraped get request from a generic URL


def scraper(url):
    site_text = requests.get(url).text
    # From inspecting random_company endpoint, company name, purposes, and other info are <li> elements
    # find_all('li') will return a list of all li elements which can be looped over
    company_info = BeautifulSoup(site_text, 'lxml').find_all('li')
    company_name = ''
    company_purpose = ''

    # loop over all li elements, store text containing Name: and Purpose to a pandas dataframe
    for info in company_info:
        if 'Name:' in info.text:
            company_name = info.text.replace('Name: ', '')
        if 'Purpose:' in info.text:
            company_purpose = info.text.replace('Purpose: ', '')
    company_df = pd.DataFrame([[company_name, company_purpose]], columns=["Name", "Purpose"])
    return company_df


# Define loop_scraper to call scraper() multiple times and append the result to a pandas df
# Output result to csv file
def loop_scraper(call_num, url):
    scraped_df = pd.DataFrame(data=None, columns=["Name", "Purpose"])
    for i in range(call_num):
        scraped_df = scraped_df.append(scraper(url=url), ignore_index=True)
    scraped_df.to_csv('output.csv', index=False)


# Testing Block, run 50 get requests and save company Name/Purpose to CSV file
if __name__ == '__main__':
    loop_scraper(50, url='http://18.206.38.144:8000/random_company')

