import json
import os
from bs4 import BeautifulSoup
from urllib import request, parse
from webpage import Webpage

class Scraper:
    def __init__(self, base_url, res_path):
        self.base_url = base_url
        self.res_path = res_path

    # Fetches a page, either from local cache or from the web
    def get_page(self, url_path):
        filename = url_path.strip('/') + '.html'
        filepath = os.path.join(self.res_path, filename)
        dirname = os.path.dirname(filepath)

        # Check if file already exists
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            print(f"Loaded from cache: {filepath}")
        # Otherwise, fetch and save it
        else:
            content = self.__fetch_page(url_path)
            print(f"Fetched and saved: {filepath}")
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(filepath, 'w') as f:
                f.write(content)

        return Webpage(url_path, content, filepath)

    # Internal method to fetch a page
    def __fetch_page(self, url_path):
        full_url = parse.urljoin(self.base_url, url_path)
        response = request.urlopen(full_url)
        return response.read().decode('utf-8')

class Webpage:
    def __init__(self, url, content, filepath):
        self.url = url
        self.content = content
        self.filepath = filepath
    
    def get_related_links(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        # Every page has a <script type="application/ld+json">
        for script in soup.find_all('script', type='application/ld+json'):
            json_data = json.loads(script.string)
            # if json_data.get('@type') == 'MedicalWebPage':
            if 'WebPage' in json_data.get('@type'):
                return json_data.get('relatedLink', [])
        # Sanity check
        print(f"Error: No JSON-LD script found on page {self.url}")
    
    def get_page_type(self):
        rel = self.get_related_links()
        # Directory page with subpages
        if len(rel) == 0:
            return 'directory'
        # Single page with no subpages
        elif len(rel) == 1:
            return 'single'
        # Multi-page with subpages
        else:
            return 'multi'