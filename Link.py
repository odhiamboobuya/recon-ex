from db_connection import create_connection, create_link
from hardcodes.hardcodes import search


class Link:

    def __init__(self, subdomain_id, link):
        self.page_url = link
        self.tech_stack = None
        self.header = ""
        self.forms = None
        self.http_parameters = None
        self.hardcoded_strings = ""
        self.screenshots = None
        self.backup_files = None
        self.outdated_js = None
        self.subdomain_id = subdomain_id
        self.link_id = None
        self.page_content = None
        self.response_code = None

    def get_page_content(self):
        from requests import get
        response = get(self.page_url)
        html = response.text
        response_code = response.status_code
        self.response_code = response_code
        self.page_content = html

    def get_tech_stack(self):
        from python_wappalyzer.Wappalyzer import Wappalyzer, WebPage
        webpage = WebPage.new_from_url(self.page_url)
        wappalyzer = Wappalyzer.latest(update=True)
        wappalyzer.analyze(webpage)
        self.tech_stack = wappalyzer.analyze_with_versions_and_categories(webpage)

    def get_header_hash(self):
        pass

    def get_form(self):
        from zetanize.zetanize import zetanize
        forms = zetanize.zetanize(self.page_content)
        self.forms = forms

    def get_http_params(self):
        url = self.page_url
        params = url.split('?')[1].split('&')
        for param in params:
            self.http_parameters.append({param.split('=')[0]: param.split('=')[1]})

    def get_hardcoded_strings(self):
        self.hardcoded_strings = search(self.page_content)

    def get_screenshots(self):
        from selenium import webdriver
        from time import sleep
        browser = webdriver.Firefox(executable_path="/home/user45/Documents/geckodriver")
        browser.get(self.page_url)
        sleep(1)
        file_name = self.page_url.split('//')[1].replace('.', '_').replace('/', '__') + '.png'
        try:
            browser.save_screenshot('screenshots' + file_name)
            self.screenshots = file_name
        except Exception as e:
            self.screenshots = "Error occured saving screenshot"
        browser.quit()

    def get_backup_files(self):
        pass

    def get_outdated_js(self):
        pass

    def process_link(self):
        self.get_page_content()
        self.get_tech_stack()
        self.get_header_hash()
        self.get_form()
        self.get_http_params()
        self.get_hardcoded_strings()
        self.get_screenshots()
        self.get_backup_files()
        self.get_outdated_js()

    def save_link(self):
        conn = create_connection()
        with conn:
            link = (self.response_code, self.page_url, self.tech_stack, self.header, self.forms, self.http_parameters,
                    self.hardcoded_strings, self.screenshots, self.backup_files, self.outdated_js, self.subdomain_id)
            self.link_id = create_link(conn, link)
        return self.subdomain_id
