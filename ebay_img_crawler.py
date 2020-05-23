import requests
from bs4 import BeautifulSoup
import os
from random import choice
import time
from tqdm import tqdm
from threading import Thread

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


class EbayImgCrawler():
    def __init__(self, keyword, page_num, size=800, output_dir='./'):
        self.imgs_all = []
        self.keyword = keyword
        self.page_num = page_num
        self.size = size
        self.output_dir = output_dir

    def crawl_by_page(self):
        for page in tqdm(range(1, self.page_num + 1)):
            try:
                response = requests.get(
                    f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={self.keyword}&_sacat=0&_pgn={page}',
                    headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                [s.extract() for s in soup('script')]
                [s.extract() for s in soup('style')]
                imgs = [img.get('src') for img in soup.select('img')]
                imgs = list(filter(lambda x: '225' in x, imgs))
                imgs = [img.replace('225', str(self.size)) for img in imgs]
                self.imgs_all += imgs

                time.sleep(3)  # 防止封ip
            except:
                break

    def download_image(self, url, idx):
        try:
            response = requests.get(url)
            with open(os.path.join(self.output_dir, self.keyword + str(idx + 1) + '.jpg'), 'wb') as f:
                f.write(response.content)
        except:
            pass

    def main(self):
        print('crawl image urls...')
        self.crawl_by_page()
        threads = []
        print('download images...')
        for idx, url in enumerate(self.imgs_all):
            t = Thread(target=self.download_image, args=(url, idx))
            t.start()
            threads.append(t)
        for thread in tqdm(threads):
            thread.join()


if __name__ == '__main__':
    crawler = EbayImgCrawler('ipad', 3)
    crawler.main()
