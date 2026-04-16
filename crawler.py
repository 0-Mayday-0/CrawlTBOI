from icecream import ic
import colorama
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
import requests as rq
import re


class Crawler:
    def __init__(self) -> None:
        colorama.init(autoreset=True)

        self._quality_to_background: dict[str, str] = {'0': colorama.Back.WHITE,
                                                       '1': colorama.Back.LIGHTBLUE_EX, '2': colorama.Back.GREEN,
                                                       '3': colorama.Back.LIGHTCYAN_EX, '4': colorama.Back.MAGENTA}


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


    def _search_items(self, item_name: str) -> list[Tag] | None:
        if not item_name:
            return None

        matches: list[Tag] = self._match_titles(item_name)

        matches.extend(self._match_tags(item_name))

        return matches


    def pretty_print_items(self, item_name: str) -> None:
        matches: list[Tag] = self._search_items(item_name)

        if not matches:
            print(f'{colorama.Fore.RED}No item found with that name, or empty string detected.\n')
            return None

        for tag in matches:
            lines: list[Tag] = tag.find_all('p', class_=False)

            try:
                quality: str = tag.find('p', {'class': 'quality'}).string[-1]
                print(f'Item name: {colorama.Fore.LIGHTBLUE_EX}{tag.p.string}{colorama.Fore.RESET}\n'
                      f'{tag.find('p', {'class': 'r-itemid'}).string}\n'
                      f'Quality: {self._quality_to_background[quality]}{colorama.Fore.BLACK}{quality}'
                      f'{colorama.Back.RESET}{colorama.Fore.RESET}\n\nItem Description:\n\n')
            except AttributeError:
                try:
                    print(f'Item name: {tag.p.string}\n{tag.find('p', {'class': 'r-itemid'}).string}\n')

                except AttributeError:
                    print(f'{colorama.Fore.RED}Search too broad, try narrowing the search term.')

            for line in lines:
                print(f'{colorama.Fore.LIGHTBLUE_EX}{line.string}')
            print(f'{colorama.Fore.RED}-'*40, '\n')



def main() -> None:
    crawler: Crawler = Crawler()

    crawler.pretty_print_items("")



if __name__ == '__main__':
    main()