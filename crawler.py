
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from icecream import ic
from time import sleep

class Crawler:
    def __init__(self) -> None:
        self._base_uri: str = 'https://www.tboi.com'

        self._item_categories: list[str] = ['repentanceitems-container', 'items-container rebirth',
                                            'afterbirthitems-container rebirth', 'afterbirthplusitems-container rebirth',
                                            'trinkets-container rebirth', 'afterbirthtrinkets-container',
                                            'afterbirthplustrinkets-container', 'tarot-container rebirth']

        self._options: webdriver.ChromeOptions = webdriver.ChromeOptions()


        #self._options.add_argument('--headless')
        #self._options.add_argument('window-size=1920x1080')

        self._driver: webdriver.Chrome = webdriver.Chrome(options=self._options)
        self._wait: WebDriverWait = WebDriverWait(self._driver, 5)

        self._driver.get(self._base_uri)

    def search(self, item: str) -> None:
        search_field: WebElement = self._wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-input')))

        search_field.send_keys(item)

        sleep(0.5)

        #items_categorized: list[WebElement] = [self._driver.find_element(By.CSS_SELECTOR, f'.{category.replace(' ', '.')}') for category in self._item_categories]

        #items_found = list(filter(lambda i: bool(i.is_displayed()), self._wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'textbox')))))

        items_found = self._wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'textbox')))

        if len(items_found) > 0:
            print("Found items:\n")
            for i in items_found:
                print(f'{i.text}')



def main() -> None:
    crawler: Crawler = Crawler()

    crawler.search('Polyph')


if __name__ == '__main__':
    main()