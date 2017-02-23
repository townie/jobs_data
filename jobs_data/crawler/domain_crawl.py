from jobs_data.crawler.base import JusTextCompanySpider
from jobs_data.db.schema import engine, CompanySite, Company

if __name__ == "__main__":
	for r in engine.execute("select company_url from company").fetchall():
         urls.append(r['company_url'])
     