"""
this class is used for getting the stuff of subdomains, notably:
    links
    the webserver it runs on
    perhaps google dorks?
"""
from db_connection import create_connection, create_subdomain
from scrapy_shell import QuotesSpider


class Subdomain:

    def __init__(self, asset_id, subdomain, out_of_scope):
        self.url = subdomain
        self.out_of_scope = out_of_scope
        self.google_dorks = []
        self.webserver = None
        self.links = []
        self.asset_id = asset_id
        self.subdomain_id = None

    def parse_links(self):
        spider_class = QuotesSpider()
        links = spider_class.main(self.url, self.out_of_scope)
        self.links = links
        return self.links

    def save_subdomain(self):
        conn = create_connection()
        with conn:
            subdomain = (self.url, self.google_dorks, self.webserver, self.links, self.asset_id)
            self.subdomain_id = create_subdomain(conn, subdomain)
        return self.subdomain_id
