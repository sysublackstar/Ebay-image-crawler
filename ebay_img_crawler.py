import requests
from bs4 import BeautifulSoup
import re
from random import choice
import time

OUTPUT_DIR = './'

headers = {
    "User-Agent": choice([
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",

    ]),
    'Accept': 'image/webp,*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive'
}

def img_crawler(key_word, page_num):
    imgs_all = []
    for page in range(1, page_num):
        try:
            response = requests.get(f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={keyword}&_sacat=0&_pgn={page}', 
                                    headers=headers)

            soup = BeautifulSoup(response.text, 'lxml')
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
            imgs = [img.get('src') for img in soup.select('img')]
            imgs = list(filter(lambda x: '225' in x, imgs))
            imgs = [img.replace('225', '800') for img in imgs]
            imgs_all += imgs

            time.sleep(3) # 防止封ip
        except:
            break
    return imgs_all

imgs_all = img_crawler('mask', 1)

def download_images(ds):
    for idx, url in enumerate(imgs_all):
        try:
            response = requests.get(url)
            with open(os.path.join(OUTPUT_DIR, idx), 'wb') as f:
                f.write(response.content)
        except:
            continue