
from icecream import ic
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
import requests as rq
import re


class Crawler:
    def __init__(self) -> None:
        self._base_uri: str = 'https://www.tboi.com'

        self._item_categories: list[str] = ['repentanceitems-container', 'items-container rebirth',
                                            'afterbirthitems-container rebirth', 'afterbirthplusitems-container rebirth',
                                            'trinkets-container rebirth', 'afterbirthtrinkets-container',
                                            'afterbirthplustrinkets-container', 'tarot-container rebirth']

        self._base_soup: BeautifulSoup = BeautifulSoup(rq.get(self._base_uri).content, 'lxml')

        self._all_categories: list[ResultSet[Tag]] = [self._base_soup.find_all('div', {'class': i}) for i in self._item_categories]

        self._all_items: list[ResultSet[Tag]] = []
        for result_set in self._all_categories:
            for tag in result_set:
                self._all_items.append(tag.find_all('li', {'class': 'textbox'}))

        self._all_tags: list[str] = []

        for result_set in self._all_items:
            for tag in result_set:
                self._all_tags.append(tag.find('p', {'class': 'tags'}).string)



    def _match_titles(self, item_name: str) -> list[Tag]:
        matches: list[Tag] = []
        for result_set in self._all_items:
            for tag in result_set:
                current_test: re.Match = re.match(f'.*{item_name}.*', tag.p.string, flags=re.I)

                if not current_test:
                    continue
                else:
                    matches.append(tag)

        return matches


    def _match_tags(self, item_name: str) -> list[Tag]:
        matches: list[Tag] = []

        for result_set in self._all_items:
            for item, tag in zip(result_set, self._all_tags):
                current_test: re.Match = re.match(f'.*{item_name}.*', tag, flags=re.I)

                if not current_test:
                    continue
                else:
                    matches.append(item)

        return matches


    def _search_items(self, item_name: str) -> list[Tag]:

        matches: list[Tag] = self._match_titles(item_name)

        matches.extend(self._match_tags(item_name))

        return matches


    def pretty_print_items(self, item_name: str) -> None:
        matches: list[Tag] = self._search_items(item_name)

        for tag in matches:
            lines: list[Tag] = tag.find_all('p', class_=False)

            try:
                print(f'Item name: {tag.p.string}\n{tag.find('p', {'class': 'r-itemid'}).string}\n'
                      f'{tag.find('p', {'class': 'quality'}).string}\n\nItem Description:\n\n')
            except AttributeError:
                print(f'Item name: {tag.p.string}\n{tag.find('p', {'class': 'r-itemid'}).string}\n')

            for line in lines:
                print(line.string)
            print('-'*40, '\n')



def main() -> None:
    crawler: Crawler = Crawler()

    crawler.pretty_print_items("tech")



if __name__ == '__main__':
    main()