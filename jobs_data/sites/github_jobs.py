# Docs
# https://jobs.github.com/api

import requests
from datetime import datetime
from jobs_data.db.schema import Job, Base, engine
from sqlalchemy.orm import sessionmaker

def page_url(page=0):
	return "https://jobs.github.com/positions.json?full_time=true&page={}".format(page)


def parse_job(raw_data, company_id=None, source_id="GITHUB"):
    job = Job(
        remote_id=raw_data['id'],
        snapshoted_at=datetime.now(),
        title=raw_data['title'],
        description=raw_data['description'],
        raw_text=str(raw_data),
        location=raw_data['location'],
        type=raw_data['type'],
        post_url=raw_data['how_to_apply'],
        company_name=raw_data['company'],
        company_url = raw_data['company_url'],
        company_id=company_id,
        source_id=source_id,
        )
    return job


def parse_and_find_company(raw_data):
	company = Company(
	    name = raw_data['company'],
	    company_url = raw_data['company_url'])

	session.query(Company).filter(Company.name == company.name).one()
	return company

if __name__ == "__main__":
    page=0
    all_jobs = []
    while True:
        print("page_number:{}".format(page))
        res=requests.get(page_url(page=page))
        for raw_data in res.json():
        	job = parse_job(raw_data)
        	all_jobs.append(job)
        print("total_jobs:{}".format(len(all_jobs)))

        if not res.json():
            break
        page += 1


    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for job in all_jobs:
        session.add(job)
    session.commit()