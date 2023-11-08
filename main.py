from html_parser import HTMLParser
from handle_table import handle_colspan_and_rowspan

def main():
    # 웹 페이지의 URL
    url = 'https://www.honestfund.kr/v2/terms/privacy'

    # HTMLParser 인스턴스 생성
    parser = HTMLParser(url)

    # 테이블 데이터 처리
    table_data = parser.get_table_data(handle_colspan_and_rowspan)

    for row in table_data:
        print(row)
    

    # 테이블 헤더를 찾고, 바디 데이터를 매핑
    # ...

    # 예시 출력
    # ...

# 메인 스크립트 실행
if __name__ == "__main__":
    main()
