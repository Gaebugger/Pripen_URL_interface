from html_parser import HTMLParser
from handle_table import handle_colspan_and_rowspan

def main():
    # 웹 페이지의 URL
    url = 'https://www.honestfund.kr/v2/terms/privacy'

    # HTMLParser 인스턴스 생성
    parser = HTMLParser(url)
    
    # 본문과 테이블 데이터를 담은 리스트를 가져옵니다.
    content_with_tables = parser.get_content_with_tables()

    print("its main")
#    print(content_with_tables)
if __name__ == "__main__":
    main()
