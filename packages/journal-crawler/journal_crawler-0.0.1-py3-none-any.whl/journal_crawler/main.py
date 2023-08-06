import pickle
from pathlib import Path
from typing import Final, Set, Tuple

from ythesis import Thesis

from journal_crawler import JournalCrawler
from journal_crawler.journals.international_press_crawler import InternationalPressCrawler
from journal_crawler.journals.journal_of_singularities_crawler import JournalOfSingularitiesCrawler

THESISES_PATH: Final[Path] = Path(
    Path(__file__).absolute().parent.parent / 'data' / 'thesises.pkl')
CRAWLER_CLASSES: Final[Tuple[JournalCrawler, ...]] = (
    JournalOfSingularitiesCrawler(), InternationalPressCrawler())


def main() -> None:
    thesises: Set[Thesis] = set()
    for crawler in CRAWLER_CLASSES:
        print('crawler:', type(crawler).__name__)
        thesises |= set(crawler.crawl_thesises())

    from pprint import pprint
    pprint(thesises)
    with open(str(THESISES_PATH), 'wb') as f:
        pickle.dump(thesises, f)

    print('length', len(thesises))


if __name__ == '__main__':
    main()
