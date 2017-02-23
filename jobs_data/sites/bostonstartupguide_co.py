# Docs
# https://bostonstartupsguide.com/boston-startup-jobs/#s=1

import requests
from datetime import datetime
from jobs_data.db.schema import Job, Base, engine, Company
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from datetime import datetime

if __name__ == "__main__":
    page = 0
    while True:
        co_url = "https://bostonstartupsguide.com/boston-area-startups/page/{}/".format(page)
        print("getting page {}".format(page))
        res = requests.get(co_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        if soup.find_all("div", {'class':'no-results'}):
            print("end of the line current page {}".format(page))
            break
        page += 1

        for company_html in soup.find_all("div", {"class": "post-single"}):
            # company_html = soup.find_all("div", {"class": "post-single"})[0]
            name = company_html.select('a')[0]['title']
            location = company_html.find_all("span", {'class': 'post-neighborhood'})[0].get_text().encode('ascii', 'ignore')
            short_description = company_html.find_all("p")[0].get_text()

            long_description = short_description + company_html.find_all("span", {"class": "post-industry"})[0].get_text()
            company_url = company_html.select('a')[0]['href']
            snapshoted_at = datetime.now()
            co = Company(name=name,
                    location=location,
                    short_description=short_description,
                    long_description=long_description,
                    company_url=company_url,
                    snapshoted_at=snapshoted_at)
            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            print("Storing comapny {}".format(co.name))
            session.add(co)
            session.commit()
