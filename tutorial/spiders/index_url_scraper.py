from scrapy import Spider
from urllib.parse import urljoin, urlparse, parse_qs

class BCorpSpider(Spider):
    name = "bcorp_spider"
    base_url = "https://www.bcorporation.net/en-us/find-a-b-corp/"
    start_urls = [base_url]

    def parse(self, response):
        # Extracting the 'href' attributes from each <a> tag within <li>
        li_elements = response.css('li.ais-Hits-item a')
        for a_tag in li_elements:
            href = a_tag.xpath('@href').get()
            if href:
                yield {'url': href}

        # Logic for pagination
        current_page_number = self.get_page_number(response.url)
        next_page_number = current_page_number + 1
        next_page_url = f"{self.base_url}?page={next_page_number}"

        # Check if next page exists by looking for a specific element
        # Adjust the selector as needed
        next_page_exists = response.css('a.pagination__next::attr(href)').get()
        if next_page_exists:
            yield response.follow(next_page_url, callback=self.parse)

    @staticmethod
    def get_page_number(url):
        """ Extracts the current page number from the URL query parameters. """
        query = urlparse(url).query
        params = parse_qs(query)
        return int(params.get('page', [1])[0])
