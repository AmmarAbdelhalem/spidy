import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class WebCrawler:
    def __init__(self, start_url) -> None:
        self.start_url = start_url
        self.base_url = self.extract_base_url(start_url)
        self.visited_urls = set()

    def extract_base_url(self, url) -> str:
        parsed_url = urlparse(url)
        if parsed_url.scheme:
            return f"{parsed_url.scheme}://{parsed_url.netloc}"
        else:
            return f"https://{parsed_url.netloc}"

    def is_same_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.base_url

    def extract_links(self, url):
        response = requests.get(url, allow_redirects=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                if self.is_same_domain(href):
                    links.append(href)
            elif href and not href.startswith('http'):
                absolute_url = urljoin(self.base_url, href)
                links.append(absolute_url)
        return links

    def crawl(self, url):
        if url in self.visited_urls:
            return
        print('Crawling:', url)
        self.visited_urls.add(url)
        links = self.extract_links(url)
        for link in links:
            self.crawl(link)

    def start(self):
        self.crawl(self.start_url)

site = input("TARGET > ")

crawler = WebCrawler(site)
crawler.start()
