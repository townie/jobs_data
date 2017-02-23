import requests
from datetime import datetime
from jobs_data.db.schema import Job, Base, engine, Company
from sqlalchemy.orm import sessionmaker

from bs4 import BeautifulSoup

if __name__ == "__main__":

    co_url = "http://bostonstartups.net/"
    print("getting page {}".format(co_url))
    res = requests.get(co_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    for company_html in soup.find_all('div', {'class':'card'}):
        # company_html = soup.find_all('div', {'class':'startup'})[0]
        name = company_html.select('h1')[0].get_text().encode('ascii', 'ignore').rstrip().lstrip()
        try:
            short_description = company_html.select('a')[3].p.get_text()
        except:
            print("no short description at 3 try 2 for {}".format(name))
            try:
                short_description = company_html.select('a')[2].p.get_text()
            except:
                print("no short description at 2 trying 1 for {}".format(name))
                try:
                    short_description = company_html.select('a')[1].p.get_text()
                except:
                    print("no short description at 1 trying 0 for {}".format(name))
                    try:
                        short_description = company_html.select('a')[0].p.get_text()
                    except:
                        print("no short description {}".format(name))
                        short_description = ""


        company_url = company_html.select('a')[0]['href']
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