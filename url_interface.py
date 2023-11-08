import requests
from bs4 import BeautifulSoup

# rowspan_tracker를 업데이트하는 부분을 수정합니다.
def handle_colspan_and_rowspan(table_soup):
    # 테이블의 모든 행을 가져옵니다.
    rows = table_soup.find_all('tr')
    # 처리된 테이블 데이터를 저장할 리스트를 초기화합니다.
    processed_table = []

    # rowspan을 처리하기 위해 임시로 저장할 딕셔너리입니다.
    rowspan_tracker = {}

    for row_index, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)
        row_data = []
        cell_counter = 0

        for cell_index, cell in enumerate(cells):
            # rowspan이 이전 행에서 설정되었는지 확인합니다.
            while cell_counter in rowspan_tracker:
                # 이전 행에서의 rowspan 값을 현재 행에 추가합니다.
                row_data.append(rowspan_tracker[cell_counter]['text'])
                # rowspan 추적기를 업데이트합니다.
                rowspan_tracker[cell_counter]['count'] -= 1
                if rowspan_tracker[cell_counter]['count'] == 0:
                    # 해당 열의 rowspan 처리가 완료되었으면 삭제합니다.
                    del rowspan_tracker[cell_counter]
                cell_counter += 1

            # 현재 셀의 colspan, rowspan을 가져옵니다.
            colspan, rowspan = int(cell.get('colspan', 1)), int(cell.get('rowspan', 1))
            cell_text = cell.get_text(strip=True)

            # colspan에 따라 셀 데이터를 추가합니다.
            for _ in range(colspan):
                row_data.append(cell_text)
                cell_counter += 1

            # rowspan에 따라 추적기에 현재 셀의 텍스트를 추가합니다.
            if rowspan > 1:
                for i in range(1, rowspan):
                    next_row_index = row_index + i
                    rowspan_tracker.setdefault(cell_counter - 1, {'text': cell_text, 'count': rowspan - 1})

        # 모든 셀을 추가한 후에도 rowspan 처리가 남아있다면, 빈 셀을 채웁니다.
        while cell_counter in rowspan_tracker:
            row_data.append(rowspan_tracker[cell_counter]['text'])
            rowspan_tracker[cell_counter]['count'] -= 1
            if rowspan_tracker[cell_counter]['count'] == 0:
                del rowspan_tracker[cell_counter]
            cell_counter += 1

        # 처리된 현재 행을 테이블 데이터에 추가합니다.
        processed_table.append(row_data)

    # 모든 행의 길이를 동일하게 맞춥니다.
    max_length = max(len(row) for row in processed_table)
    for row in processed_table:
        row.extend([""] * (max_length - len(row)))

    return processed_table



# 메인 함수
def main():
    # 웹 페이지의 URL
    url = 'https://www.honestfund.kr/v2/terms/privacy'

    # requests를 사용하여 웹 페이지의 HTML을 가져옵니다.
    response = requests.get(url)

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')

    # 예시로 첫 번째 테이블을 사용합니다.
    table_soup = soup.find('table')

    # 테이블 헤더를 찾습니다. (첫 번째 행이라고 가정합니다)
    header_soup = table_soup.find('thead').find_all('th')
    headers = [th.get_text(strip=True) for th in header_soup]

    # 테이블 바디를 찾습니다.
    body_soup = table_soup.find('tbody')
    table_data = handle_colspan_and_rowspan(body_soup)

    # 각 행을 딕셔너리 형태로 변환 (키-값 쌍으로 매핑)
    table_dicts = [dict(zip(headers, row)) for row in table_data]

    # 예시 출력
    for entry in table_dicts:
        print(entry)


# 메인 스크립트 실행
if __name__ == "__main__":
    main()
