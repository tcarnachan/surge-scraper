import os
from urllib import request, parse
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, base_url, res_path):
        self.base_url = base_url
        self.res_path = res_path

    # Fetches a page, either from local cache or from the web
    def get_page(self, url_path):
        filename = url_path.strip('/').replace('/', '_') + '.html'
        filepath = os.path.join(self.res_path, filename)

        # Check if file already exists
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            print(f"Loaded from cache: {filepath}")
        # Otherwise, fetch and save it
        else:
            content = self.__fetch_page(url_path)
            print(f"Fetched and saved: {filepath}")
            if not os.path.exists(self.res_path):
                os.makedirs(self.res_path)
            with open(filepath, 'w') as f:
                f.write(content)
        return content

    # Internal method to fetch a page
    def __fetch_page(self, url_path):
        full_url = parse.urljoin(self.base_url, url_path)
        response = request.urlopen(full_url)
        return response.read().decode('utf-8')

# Returns a list of relative urls from the conditions page
def get_condition_links(scraper):
    content = scraper.get_page('conditions')
    soup = BeautifulSoup(content, 'html.parser')
    # Set because e.g. Anaemia and Iron defeciency both link to the same page
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Exclude links with anchors or to other parts of the site
        if '#' not in href and href.startswith('/conditions/'):
            links.add(href)
    return list(links)

scraper = Scraper(base_url="https://www.nhs.uk/", res_path="res/nhs")
print(len(get_condition_links(scraper)))