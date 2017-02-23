# http://www.builtinboston.com/companies?page=3

import requests
from datetime import datetime
from jobs_data.db.schema import Job, Base, engine, Company
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from googleapiclient.discovery import build

from random import randint
from time import sleep

def companies_from_google(dev=False, google="", cx="cx"):
    # google = "NEED TO GET"
    # cx = 'NEED TO GET:ziylcvy5nkuxxx'
    q = 'site:builtinboston.com/company/'
    service = build("customsearch", "v1", developerKey=google)
    position = 1
    builtinboston_co = []
    num = 10
    while True:
        sleep_time= randint(1,10)
        print("sleeping for {}".format(sleep_time))
        res = service.cse().list(q=q, cx=cx, num=num, start=position).execute()
        total = res['searchInformation']['totalResults']
        position += num
        print("pos: {} num: {}".format(position, num))
        for url in res['items']:
            builtinboston_co.append(url['formattedUrl'])

        if position >= int(total) or dev:
            break

    return builtinboston_co

if __name__ == "__main__":
    page = 0
    co_urls = []
    co_urls = companies_from_google(dev=False)
    for url in co_urls:
        # url = co_urls[0]
        r = requests.get("http://" + url)  
        soup = BeautifulSoup(r.text, 'html.parser')
        meta_info = soup.find_all('div', {'class':'nc-glance-block'})[0].get_text()
        short_description = soup.find_all('div', {'class':'nc-span-right'})[0].get_text().rstrip().lstrip()
        try:
            extra = soup.find_all('div', {'class':'nc-culture-block'})[0].get_text().rstrip().lstrip()
        except:
            extra = ""
        long_description = meta_info + short_description + extra
        name = soup.find_all('div', {'class':'nc-glance-block'})[0].select('h5')[0].select('a')[0].get('title')

        if soup.find_all('div', {'class':'nc-glance-block'})[0].select('h5')[3].strong.get_text() == 'Location: ':
            localtion = soup.find_all('div', {'class':'nc-glance-block'})[0].select('h5')[3].strong.get_text()

        company_url = soup.find_all('div', {'class':'nc-glance-block'})[0].select('h5')[0].select('a')[0].get('href')
        snapshoted_at = datetime.now()
        co = Company(name=name,
                short_description=short_description,
                company_url=company_url,
                snapshoted_at=snapshoted_at)

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        print("Storing comapny {}".format(co.name))
        session.add(co)
        session.commit()

