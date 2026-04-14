from crawler import Crawler

class Menu:
    def __init__(self) -> None:
        self._crawler: Crawler = Crawler()

    def mainloop(self) -> None:
        while True:
            user_input: str = input("Item to search: ")

            self._crawler.pretty_print_items(user_input)

def main():
    menu: Menu = Menu()

    menu.mainloop()

if __name__ == "__main__":
    main()