import telegram
from time import sleep
from telegram.error import NetworkError, Unauthorized

UPDATE_ID = None

def main():
    global UPDATE_ID
    bot = telegram.Bot('') # 토큰 값이 들어가야 할 부분....

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

        if update.message:
            if update.message.text:
                update.message.reply_text(update.message.text)

if __name__ == '__main__':
    main()