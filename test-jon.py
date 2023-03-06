import asyncio
import requests
from bs4 import BeautifulSoup
import telegram

async def main():
    bot = telegram.Bot("6263023646:AAGazIM4dn0eRPh1TEUcOzXhrMmb6Atv8rw")
    async with bot:
        # print(await bot.get_me())
        # print((await bot.get_updates())[0])
        await bot.send_message(text='Hi John!', chat_id=-1001872135066)

def test2():
    url = 'http://localhost:8501/pm1_detector'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

if __name__ == '__main__':
    # asyncio.run(main())
    test2()
