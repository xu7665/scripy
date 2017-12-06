import requests
import re
import json
from  multiprocessing import Pool
from requests.exceptions import RequestException

def get_one_page(url):
    headers = {
                  'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept - Encoding': 'gzip,deflate,sdch',
                  'Accept-Language':'zh - CN,zh;q=0.8',
                  'Cache-Control':'no-cache',
                  'Connection':'keep-alive',
                  'User-Agent':'Mozilla/5.0(Windows NT 10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/55.0.2883.87Safari/537.36'
    }
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'socre':item[5]+item[6]
        }

def wirte_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://www.maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        wirte_to_file(item)

if __name__ == '__main__':

    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
