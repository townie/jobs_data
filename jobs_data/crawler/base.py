import scrapy
from scrapy.linkextractors import LinkExtractor
import justext
from tld import get_tld
import logging
from datetime import datetime
from jobs_data.db.schema import engine, CompanySite, Company
from sqlalchemy.orm import sessionmaker
import json

class JusTextCompanySpider(scrapy.Spider):
    name = 'all'
    urls = []
    for r in engine.execute("select company_url from company").fetchall():
        urls.append(r['company_url'])
    start_urls = urls

    def parse(self, response):
        # logging.warn(self.start_urls)

        base_domains = self.start_urls_base_urls()
        blacklist_tld = self.blacklist_tld()

        json_page = self.jsonify_page(response)
        text = self.collect_text(json_page)

        self.create_and_save_site(json_page=json_page, text=text, response=response)

        # Next Page
        for link in LinkExtractor().extract_links(response):
            if self.valid_url(link, base_domains=base_domains, blacklist_tld=blacklist_tld):
                # logging.warn('Nextpage:{}'.format(link.url))
                yield scrapy.Request(link.url, callback=self.parse)
            else:
                pass
                # logging.warn("passing on domain:{} link:{}".format(get_tld(link.url, as_object=True).domain,link.url))

    def valid_url(self, link, base_domains=[], blacklist_tld=[]):
        valid_domain = get_tld(link.url, as_object=True).domain in base_domains 
        blacklisted = get_tld(link.url, as_object=True).tld in blacklist_tld

        if valid_domain and not blacklisted:
            return True
        else:
            return False

    def create_and_save_site(self, json_page=None, text=None, response=None):
        site = CompanySite(
            snapshoted_at=datetime.now(),
            url=response.url,
            raw_html=response.text,
            justext_content=text,
            justext_json=json.dumps(json_page),
            domain=get_tld(response.url, as_object=True).domain
        )
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(site)
        session.commit()
        logging.info("inserted {}".format(site.url))

    def jsonify_page(self, response):
        paragraphs = justext.justext(response.text, justext.get_stoplist("English"))
        content = []
        for p in paragraphs:
            j = {}
            j['is_boilerplate'] = p.is_boilerplate
            j['class_type'] = p.class_type
            j['heading'] = p.heading
            j['tags_count'] = p.tags_count           
            j['xpath'] = p.xpath                
            j['cf_class'] = p.cf_class             
            j['dom_path'] = p.dom_path             
            j['links_density'] = p.links_density()        
            j['text'] = p.text                                        
            j['chars_count_in_links'] = p.chars_count_in_links 
            j['text_nodes'] = p.text_nodes                                  
            j['words_count'] = p.words_count  
            content.append(j)

        return content

    def blacklist_tld(self):
        blacklist = ['blinkforhome.support',
        ]
        return blacklist

    def collect_text(self, json):
        text = []
        for row in json:
            if not row['is_boilerplate']:
                text.append(row['text'] + " ")
        return ''.join(text)


    def start_urls_base_urls(self):
        base_domains = []
        bad = self.black_list_sites()
        for url in self.start_urls:
            try:
                res = get_tld(url, as_object=True)
                if res.domain in bad:
                    continue
                base_domains.append(res.domain)
            except:
                # logging.warn("BAD URL:{}".format(url))
                pass

        self.base_domains = base_domains
        return base_domains

    def black_list_sites(self):
        blacklist = ['careacademy',
                     'facebook',
                     'twitter',
                     'google',
                     'youtube',
                     'support.google',
                     'monster',
                     'mit',
                     'act',
                     'teenlife',
                     'wordpress',
                     'linkedin', 
                     'zaius', 
                     'slideshare', 
                     'streetwise', 
                     'nature', 
                     'squarespace', 'caredash', 'cisco']
        return blacklist
