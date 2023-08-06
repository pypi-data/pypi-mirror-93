from typing import Tuple


def parse_authors(authors_: str) -> Tuple[str, ...]:
    authors = authors_.strip().replace(' and ', ', ').replace(',and ', ', ').split(',')

    thesis_authors = []
    for author in authors:
        author = author.strip()
        if author == '':
            continue
        thesis_authors.append(author)

    return tuple(thesis_authors)


if __name__ == '__main__':
    assert parse_authors('yassu') == ('yassu',)
    assert parse_authors('yassu, yassu2') == ('yassu', 'yassu2')
    assert parse_authors('yassu, yassu2 and yassu3') == ('yassu', 'yassu2', 'yassu3')
