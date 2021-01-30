import telegram
from time import sleep

#붙여넣기!
import requests
from bs4 import BeautifulSoup

from telegram.error import NetworkError, Unauthorized

UPDATE_ID = None

def main():
    global UPDATE_ID
    bot = telegram.Bot('')

    try:
        UPDATE_ID = bot.get_updates()[0].update_id
    except IndexError:
        UPDATE_ID = None

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized: # 사용자가 봇을 차단했을때는 Unauthorized가 나타납니다.
            UPDATE_ID = UPDATE_ID + 1

def echo(bot):
    global UPDATE_ID

    # 마지막으로 처리한 메시지는 UPDATE_ID이고, 이후의 메시지를 처리하기 위해 이렇게 합니다.
    for update in bot.get_updates(offset=UPDATE_ID, timeout=10):
        UPDATE_ID = update.update_id + 1
        chat_id = update.message.chat.id

        if update.message:
            if update.message.text:
                daangn_search(bot, chat_id, update.message.text) # 추가!

def daangn_search(bot, chat_id, keyword):
    global UPDATE_ID
    # 검색하기
    # url = https://www.daangn.com/search/%EB%85%B8%ED%8A%B8%EB%B6%81
    url = 'https://www.daangn.com/search/'
    # keyword = input(">> 검색하고 싶은 물품을 입력해주세요: ") # 삭제!

    # 검색 결과 가져오기
    response = requests.get(url + keyword)

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
            bot.sendMessage(chat_id = chat_id, text=f"'제목: {title.get_text()} \n내용: {content.get_text()}\n지역: {region.get_text(strip=True)}\n가격: {price.get_text(strip=True)}")


    # 성공하지 않았을 때는 실행하지 않음
    else:
        print("파싱 실패!", response.status_code)

if __name__ == '__main__':
    main()