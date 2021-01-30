import urllib.parse
import telegram
import requests
from bs4 import BeautifulSoup
from time import sleep


TOKEN = ""
UPDATE_ID = None
LOWER_PRICE = None


def main() -> None:
    global UPDATE_ID
    # 텔레그램 봇으로 봇 API 키를 인증받기
    bot = telegram.Bot(token = TOKEN)

    try:
        UPDATE_ID = bot.getUpdates()[0].update_id
    except IndexError:
        UPDATE_ID = None

    while True:
        try:
            reply_received_message(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            UPDATE_ID = UPDATE_ID + 1
    

def reply_received_message(bot: telegram.Bot) -> None:
    global UPDATE_ID
    for update in bot.getUpdates(offset=UPDATE_ID, timeout=10):
        UPDATE_ID = update.update_id + 1
        print(update.message.text)
        if update.message:
            if update.message.text == "/현재 최저가 물품 조회":
                Search
        else:
            print("뭐 임마.")


def Search(keyword: str, pageNum: int):
    global LOWER_PRICE
    keyword = urllib.parse.quote(keyword)
    for page_number in range(1, pageNum + 1):
        url = f'https://www.daangn.com/search/{keyword}/more/flea_market?page={page_number}'
        response = requests.get(url)
        
        if response.status_code == 200:
            articles = []
            # 전체 HTML을 TEXT 형식으로 저장
            html = response.text
            # TEXT 형식을 HTML 형식으로 변환
            soup = BeautifulSoup(html, 'html.parser')
            # "중고거래"에서 물품들만 저장
            items = soup.find_all('a', 'flea-market-article-link')
            # print(len(items))
            for item in items:
                article = item.find('div', class_='article-info')

                title = article.find('span', class_='article-title').get_text()
                content = article.find('span', class_='article-content').get_text()
                region = article.find('p', class_='article-region-name').get_text(strip=True)
                price = article.find('p', class_='article-price').get_text(strip=True)
                # print("="*50)
                # print(f'제목: {title.get_text()}')
                # print(f'내용: {content.get_text()}')
                # print(f'지역: {region.get_text(strip=True)}')
                # print(f'가격: {price.get_text(strip=True)}')
                # print("="*50)

                article = {
                    "title": title,
                    "content": content,
                    "region": region,
                    "price": price
                }

                articles.append(article)
        else:
            return "잠시 후 다시 시도해주세요!"

    if LOWER_PRICE
    return url

if __name__ == '__main__':
    # main()
    Search("컴퓨터", 5)
    print(articles[0]["title"])
