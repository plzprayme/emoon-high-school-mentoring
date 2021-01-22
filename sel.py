from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


# with webdriver.Chrome() as driver:
driver = webdriver.Chrome()
url = 'https://www.daangn.com/'
wait = WebDriverWait(driver, 10)

driver.get(url)
driver.implicitly_wait(1)

# search_bar = wait.until(
#     lambda x: x.find_element_by_css_selector('#header-search-input')
# )
search_bar = driver.find_element_by_css_selector('#header-search-input')
search_bar.send_keys('노트북')
search_bar.send_keys(Keys.ENTER)
driver.implicitly_wait(1)

more_button = driver.find_element_by_css_selector('#result > div:nth-child(1) > div.more-btn')
more_button.click()


# 1주차 코드 시작

html = driver.page_source
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

driver.implicitly_wait(100)

    # 검색하기
    # search_bar = driver.find_element_by_css_selector('#header-search-input')
    # search_bar.send_keys('노트북')
    # search_bar.send_keys(Keys.ENTER)


