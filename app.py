import requests
from bs4 import BeautifulSoup

# 검색하기
# url = https://www.daangn.com/search/%EB%85%B8%ED%8A%B8%EB%B6%81
url = 'https://www.daangn.com/search/'
target = input(">> 검색하고 싶은 물품을 입력해주세요: ")

# 검색 결과 가져오기
response = requests.get(url + target)

# 성공 했을 때만 실행
if response.status_code == 200:
    # 전체 HTML을 TEXT 형식으로 저장
    html = response.text
    # TEXT 형식을 HTML 형식으로 변환
    soup = BeautifulSoup(html, 'html.parser')
    
    # "중고거래"를 통째로 저장
    display_rack = soup.find('div', id='flea-market-wrap')
    # "중고거래"에서 물품들만 저장
    items = display_rack.find_all('a', 'flea-market-article-link')

    # 물품들을 각각의 물품으로 변경
    for item in items:
        article = item.find('div', class_='article-info')

        title = article.find('span', class_='article-title')
        content = article.find('span', class_='article-content')
        region = article.find('p', class_='article-region-name')
        price = article.find('p', class_='article-price')
        print("="*50)
        print(f'제목: {title.get_text()}')
        print(f'내용: {content.get_text()}')
        print(f'지역: {region.get_text(strip=True)}')
        print(f'가격: {price.get_text(strip=True)}')
        print("="*50)

# 성공하지 않았을 때는 실행하지 않음
else:
    print("파싱 실패!", response.status_code)