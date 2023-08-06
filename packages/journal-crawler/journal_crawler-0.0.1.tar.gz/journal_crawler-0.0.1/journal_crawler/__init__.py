from abc import ABCMeta, abstractmethod
from typing import Generator

from ythesis import Thesis


class JournalCrawler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def crawl_thesises(self) -> Generator[Thesis, None, None]:
        ...
