from typing import Union

from bs4 import BeautifulSoup


class Reader:
    def __init__(self, input_data: Union[str, BeautifulSoup]):
        if type(input_data) == str:
            self.path = input_data
            self.file = open(self.path, 'r')
            self.content = self.file.read()
            self.soup = BeautifulSoup(self.content, 'html.parser')
        elif type(input_data) == BeautifulSoup:
            self.soup = input_data

    def get_selector(self, selector: str):
        if el := self.soup.select_one(selector):
            return el.get_text().strip()

    def get_name_from_header(self):
        return self.get_selector('titlestmt > title')
