from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from handle_table import handle_colspan_and_rowspan

class HTMLParser:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.main_content = None
        self.initialize_soup()

    def initialize_soup(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # 상태 코드 검사 (200 OK가 아니면 예외 발생)
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_main_content(self):
        if self.soup:
            main_content = self.soup.find('main')
            if main_content:
                self.main_content = main_content  # main_content는 이제 BeautifulSoup 객체입니다.
            else:
                print("The <main> tag could not be found in the HTML content.")
                self.main_content = None
        else:
            print("Soup object is not initialized.")
            self.main_content = None


    def get_content_with_tables(self):
        self.extract_main_content()  # main_content를 설정하는 메서드라고 가정합니다.
        main_content = self.main_content

        # table 태그 내부에 있는지 확인하는 함수
        def is_inside_table(tag):
            while tag is not None:
                if tag.name == 'table':
                    return True
                tag = tag.parent
            return False

        content = []
        for element in main_content.find_all():
            if element.name == 'table':
                # get_table_data 메소드를 사용하여 table 데이터를 전처리합니다.
                table_data_list = self.get_table_data(element, handle_colspan_and_rowspan)
                # 리스트 안의 딕셔너리들을 문자열로 변환하여 content 리스트에 추가합니다.
                for table_data in table_data_list:
                    table_data_str = ', '.join(f"{key}: {value}" for key, value in table_data.items())
                    print("table_data is")
                    print(table_data_str)
                    content.append(table_data_str)
                
            elif not is_inside_table(element):
                text = element.get_text(separator='\n', strip=True)
                if text:  # 빈 문자열이 아닌 경우에만 추가합니다.
                    content.append(text)  # 텍스트를 리스트에 추가합니다.


        return '\n'.join(content).strip()  # 리스트의 모든 요소를 개행 문자로 결합하여 문자열로 변환합니다









    def get_table_data(self, table_soup, table_handler):
        # 테이블 헤더를 찾습니다. (첫 번째 행이라고 가정합니다)
        header_soup = table_soup.find('thead').find_all('th')
        headers = [th.get_text(strip=True) for th in header_soup]

        # 테이블 바디를 찾습니다.
        body_soup = table_soup.find('tbody')
        table_data = table_handler(body_soup)
        
        return [dict(zip(headers, row)) for row in table_data]
    
