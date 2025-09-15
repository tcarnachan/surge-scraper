import json
from bs4 import BeautifulSoup

from scraper import Scraper

# Returns a list of relative urls from the conditions page
def get_condition_links(scraper):
    content = scraper.get_page('conditions').content
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
condition_links = get_condition_links(scraper)
page_types = { 'directory': [], 'single': [], 'multi': [] }
for link in condition_links:
    page = scraper.get_page(link)
    page_types[page.get_page_type()].append(link)

with open('res/nhs/page_types.json', 'w') as f:
    json.dump(page_types, f, indent=2)