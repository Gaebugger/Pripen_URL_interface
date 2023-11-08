import requests
from bs4 import BeautifulSoup

class HTMLParser:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self):
        response = requests.get(self.url)
        return BeautifulSoup(response.text, 'html.parser')

    def get_table_data(self, table_handler):
        table_soup = self.soup.find('table')
        
        # 테이블 헤더를 찾습니다. (첫 번째 행이라고 가정합니다)
        header_soup = table_soup.find('thead').find_all('th')
        headers = [th.get_text(strip=True) for th in header_soup]

        # 테이블 바디를 찾습니다.
        body_soup = table_soup.find('tbody')
        table_data = table_handler(body_soup)
        
        return [dict(zip(headers, row)) for row in table_data]
