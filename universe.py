from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser = webdriver.Edge("msedgedriver.exe")
browser.get(START_URL)

time.sleep(10)

scraped_data = []

def scrape():
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source,"html.parser")

    bright_star_table = soup.find("table", attrs={"class","wikitable sortable jquery-tablesorter"})
    table_body = bright_star_table.find('tbody')
    table_rows = table_body.find_all('tr')

    for row in table_rows:
        table_cols = row.find_all('td')
        # print(table_cols)
        temp_list = []

        for col_data in table_cols:
            # print(col_data.text)
            data = col_data.text.strip()
            # print(data)
            temp_list.append(data)
        scraped_data.append(temp_list)
    stars_data = []

    for i in range(0,len(scraped_data)):
        Star_names = scraped_data[i][1]
        Distance = scraped_data[i][3]
        Mass = scraped_data[i][5]
        Radius = scraped_data[i][6]
        Lum = scraped_data[i][7]

        required_data = [Star_names,Distance,Mass,Radius,Lum]
        stars_data.append(required_data)

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temps_list = []
        for tr_tag in soup.find_all("class", attrs={"class":"wikitable sortable jquery-tablesorter"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temps_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temps_list.append("")
        scraped_data.append(temps_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

scrape()

headers = ['Star_name','Distance','Mass','Radius','Luminosity']
star_df_1 = pd.DataFrame(stars_data, columns=headers)
star_df_1.to_csv('scraped_data.csv',index=True,index_label='id')

