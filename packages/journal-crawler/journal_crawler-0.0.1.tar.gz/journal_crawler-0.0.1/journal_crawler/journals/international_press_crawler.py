import re
import urllib.parse
from datetime import datetime
from typing import Dict, Final, Generator

import requests
from bs4 import BeautifulSoup
from ythesis import Thesis

from journal_crawler import JournalCrawler
from journal_crawler.const import BROWSER_HEADER
from journal_crawler.utils import parse_authors

BASE_URL: Final[str] = 'https://www.intlpress.com/'
JOURNAL_CONTENTS: Final[Dict[str, str]] = {
    'acta': 'Acta Mathematica',
    'atmp': 'Advances in Theoretical and Mathematical Physics',
    'amsa': 'Annals of Mathematical Sciences and Applications',
    'arkiv': 'Arkiv för Matematik',
    'ajm': 'Asian Journal of Mathematics',
    'cjm': 'Cambridge Journal of Mathematics',
    'cag': 'Communications in Analysis and Geometry',
    'cis': 'Communications in Information and Systems',
    'cms': 'Communications in Mathematical Sciences',
    'cntp': 'Communications in Number Theory and Physics',
    # 'cdm': 'Current Developments in Mathematics',
    # 'dpde': 'Dynamics of Partial Differential Equations',
    # 'gic': 'Geometry, Imaging and Computing',
    # 'hha': 'Homology, Homotopy and Applications',
    # 'joc': 'Journal of Combinatorics',
    # 'jdg': 'Journal of Differential Geometry',
    # 'jsg': 'Journal of Symplectic Geometry',
    # 'mrl': 'Mathematical Research Letters',
    # 'mcgd': 'Mathematics, Computation and Geometry of Data',
    # 'maa': 'Methods and Applications of Analysis',
    # 'iccm': 'Notices of the International Congress of Chinese Mathematicians',
    # 'pamq': 'Pure and Applied Mathematics Quarterly',
    # 'sii': 'Statistics and Its Interface',
    # 'sdg': 'Surveys in Differential Geometry',
}


class InternationalPressCrawler(JournalCrawler):

    def crawl_volumes(self, journal_name: str) -> Dict[str, str]:
        """ from volume title to volume url """
        journal_url = 'https://www.intlpress.com/site/pub/pages/journals/items/' + \
            f'{journal_name}/content/vols/index.php'
        journal_response = requests.get(journal_url, headers=BROWSER_HEADER)
        journal_soup = BeautifulSoup(journal_response.text, 'html.parser')

        volumes: Dict[str, str] = {}
        volumes_elem = journal_soup.find('div', {
            'id': 'mainbody'
        }).find('div', {
            'id': 'list'
        }).find_all('div', {'class': 'list_item'})
        for volume_elem in volumes_elem:
            href = urllib.parse.urljoin(BASE_URL, volume_elem.find('a').get('href'))
            volume_title = volume_elem.find('a').find('p').get_text().strip()
            volumes[volume_title] = href

        return volumes

    def crawl_thesises_one_journal(self, journal_name: str) -> Generator[Thesis, None, None]:
        volumes = self.crawl_volumes(journal_name)
        for volume_title, volume_url in volumes.items():
            print(volume_title)
            published_year = int(re.search(r'\d{4}', volume_title).group())  # type: ignore
            volume_response = requests.get(volume_url, headers=BROWSER_HEADER)
            if volume_response.status_code > 300:
                continue

            volume_soup = BeautifulSoup(volume_response.text, 'html.parser')
            issue_elems = volume_soup.find('div', {
                'id': 'list'
            }).find_all('div', {'class': 'list_item'})

            issues = {}
            for issue_elem in issue_elems:
                issue_title = issue_elem.find('a').find('p').get_text()
                issue_url = issue_elem.find('a').get('href')
                issue_url = urllib.parse.urljoin(BASE_URL, issue_url)
                issues[issue_title] = issue_url

            for issue_title, issue_url in issues.items():
                content_response = requests.get(issue_url, headers=BROWSER_HEADER)
                if content_response.status_code > 300:
                    continue
                content_soup = BeautifulSoup(content_response.text, 'html.parser')
                print(90, issue_title, issue_url)
                no_contents_notice = bool(
                    content_soup.find('div', {
                        'id': 'mainbody'
                    }).find('div', {
                        'id': 'list'
                    }).find('p', {'class': 'nocontentsnotice'}))

                if no_contents_notice:
                    continue

                content_elems = content_soup.find('div', {
                    'id': 'list'
                }).find_all('div', {'class': 'list_item'})

                for content_elem in content_elems:
                    thesis_title = content_elem.find('a').find('p').get_text()

                    if not content_elem.find('p', {'class': 'authors'}):
                        continue

                    thesis_authors = parse_authors(
                        content_elem.find('p', {
                            'class': 'authors'
                        }).get_text())
                    thesis_url = content_elem.find('a').get('href')
                    thesis_url = urllib.parse.urljoin(BASE_URL, thesis_url)
                    yield (
                        Thesis(
                            title=thesis_title,
                            authors=thesis_authors,
                            published=datetime(published_year, 1, 1),
                            journal_name=JOURNAL_CONTENTS[journal_name],
                            url=thesis_url,
                        ))

    def crawl_thesises(self) -> Generator[Thesis, None, None]:
        for journal_name in JOURNAL_CONTENTS:
            print(journal_name)
            yield from self.crawl_thesises_one_journal(journal_name)


def main() -> None:
    crawler = InternationalPressCrawler()
    thesises = list(crawler.crawl_thesises())

    from pprint import pprint
    pprint(thesises)
    print('length', len(thesises))


if __name__ == '__main__':
    main()
