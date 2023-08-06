import re
import urllib.parse
from datetime import datetime
from typing import Dict, Generator, List

import requests
from bs4 import BeautifulSoup
from ythesis import Thesis

from journal_crawler import JournalCrawler
from journal_crawler.const import BROWSER_HEADER
from journal_crawler.utils import parse_authors

BASE_URL = 'https://www.journalofsing.org/'

ROOT_RESPONSE = requests.get('https://www.journalofsing.org/', headers=BROWSER_HEADER)
ROOT_SOUP = BeautifulSoup(ROOT_RESPONSE.text, 'html.parser')

JOURNAL_LIST_SOUP = ROOT_SOUP.find('div', {
    'class': 'box',
    'id': 'col'
}).find('div').find('div').find('ul').find('ul')


class JournalOfSingularitiesCrawler(JournalCrawler):

    def crawl_journal_links(self) -> Dict[str, str]:
        """ get dict from title to url """
        journal_links: Dict[str, str] = {}
        for journal_soup in JOURNAL_LIST_SOUP:
            a_elem = journal_soup.find('a')
            if a_elem == -1 or a_elem is None:
                continue
            href = a_elem.get('href')
            if 'volume' not in href:
                continue

            journal_title = a_elem.get_text()
            journal_links[journal_title] = urllib.parse.urljoin(BASE_URL, href)

        return journal_links

    def crawl_thesises(self) -> Generator[Thesis, None, None]:
        journal_links = self.crawl_journal_links()

        for journal_title, url in journal_links.items():
            published_year = int(re.search(r'\d{4}', journal_title).group())  # type: ignore
            published = datetime(published_year, 1, 1)
            thesises_response = requests.get(url, headers=BROWSER_HEADER)
            thesises_soup = BeautifulSoup(thesises_response.text, 'html.parser')
            thesises_elem = thesises_soup.find('div', {
                'class': 'box',
                'id': 'col'
            }).find('div', {
                'id': 'col-text-content2'
            }).find_all('table')
            for thesis_elem in thesises_elem:
                trs = thesis_elem.find_all('tr')
                if trs[0].find('td').find('img'):
                    continue
                thesis_title = trs[0].find('td').find('a').find('em').get_text().strip()
                thesis_href = trs[0].find('td').find('a').get('href')

                if thesis_title == 'Preface':
                    continue
                authors = parse_authors(trs[1].find('td').get_text())
                yield (
                    Thesis(
                        title=thesis_title,
                        authors=authors,
                        published=published,
                        journal_name='Journal of Singularities',
                        url=urllib.parse.urljoin(url, thesis_href)))


def main() -> None:
    crawler = JournalOfSingularitiesCrawler()
    thesises: List[Thesis] = list(crawler.crawl_thesises())

    from pprint import pprint
    pprint(thesises)
    print('length', len(thesises))


if __name__ == '__main__':
    main()
