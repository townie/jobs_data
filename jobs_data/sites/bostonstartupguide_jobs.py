# Docs
# https://bostonstartupsguide.com/boston-startup-jobs/#s=1

import requests
from datetime import datetime
from jobs_data.db.schema import Job, Base, engine
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep


def extract_urls(html_doc=None):
    job_urls = []
    soup = BeautifulSoup(html_doc, 'html.parser')

    # get list of jobs
    for job_html in soup.find_all('li'):
        # get the url to the job
        try:
            job_url = job_html.select('a')[0].get('href')
            job_urls.append(job_url)
        except:
            pass
    return job_urls

job_post_url = "https://bostonstartupsguide.com/jm-ajax/get_listings/"

params = {'search_keywords': '',
          'per_page': 10,
          'orderby': 'featured',
          'order': 'DESC',
          'page': 0,  # this controls pages
          'show_pagination': 'false'
          }


def parse_job(soup, post_url=None, company_id=None, source_id="bostonstartupguide"):
    job = Job(
        remote_id=post_url,
        snapshoted_at=datetime.now(),
        title=try_title(soup),
        description=soup.find_all('div', {'class':'job_description'})[0].get_text(),
        raw_text=soup.find_all('div', {'class':'job_description'})[0].get_text(),
        location=try_loc(soup),
        type=soup.find_all('li', {'class':'job-type'})[0].get_text(),
        post_url=post_url,
        company_name=soup.find_all('strong')[0].get_text(),
        company_url=try_website(soup),
        company_id=company_id,
        source_id=source_id,
        )
    return job

def try_website(soup):
    try:
        return soup.find_all('a', {'class':'website'})[0].get('href')
    except:
        return ""

def try_title(soup):
    try:
        return soup.select('h2')[0].get_text()
    except:
        return ""

def try_loc(soup):
    try:
        return soup.find_all('a', {'class':'google_map_link'})[0].get_text()
    except:
        return ""

def get_and_store_job(job_url):
    res = requests.get(job_url)
    print("Trying job_url {}".format(job_url))
    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        job = parse_job(soup, post_url=job_url)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        print("Storing job {}".format(job.title))
        session.add(job)
        session.commit()
    except Exception as e:
        print("something went wrong on {} ERROR: {}".format(job_url, e))

def generate_job_urls():
    final_page = 2
    current_page = 0
    all_jobs = []
    debug= False

    while True:
        # handle page advancement
        params['page'] = current_page

        # get list
        res = requests.post(job_post_url, data=params)
        final_page = res.json()['max_num_pages']
        print("page{}/{}".format(current_page, final_page))
        if current_page > final_page:
            print("exiting on page: {}".format(current_page))
            break
        current_page += 1

        all_jobs.append(extract_urls(html_doc=res.json()['html']))
        if debug:
            break

    return [item for sublist in all_jobs for item in sublist]

if __name__ == "__main__":

    ## if need to scale Map Here
    full_list = generate_job_urls()

    ## then reduce here
    print("Number of jobs {}".format(full_list))
    for job_url in full_list:
        # sleep so we dont DDOS their servers
        sleep(randint(1,10))
        get_and_store_job(job_url)



