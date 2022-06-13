import requests
from bs4 import BeautifulSoup
import unittest
from unittest import mock


class TestLogin(unittest.TestCase):
    
    def test01(self):
        anime = mock.Mock(return_value={"code":200, "msg": "搜尋成功"})
        numbers = 5
        res = anime(numbers)
        self.assertEqual(res["code"], 200)
        

def anime(numbers):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
    }
    
    target_url = 'https://ani.gamer.com.tw/'
    res = requests.get(target_url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    
    rows = soup.select_one('.normal-ver > .newanime-block')
    target = rows.select('.newanime-date-area:not(.premium-block)')
    
    content = ""
    counts = 0
    for item in target:
        if counts < numbers:
            anime_name = item.select_one('.anime-name > p').text.strip()
            anime_ep = item.select_one('.anime-episode > p').text.strip()
            anime_watch_number = item.select_one('.anime-watch-number > p').text.strip()
            anime_url = f"https://ani.gamer.com.tw/{item.select_one('.anime-card-block').get('href').strip()}"
            content += f"{anime_name} {anime_ep} 觀看次數{anime_watch_number}\n{anime_url}\n"
        counts += 1
    return content


if __name__ == "__main__":
    unittest.main()
    