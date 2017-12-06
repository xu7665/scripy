# _*_ coding:utf-8 _*_
import requests
import json
import pymongo
import re
import os
from hashlib import md5
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from config import *
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_page_index(offset,KEYWORD):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': KEYWORD,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求出错')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情出错',url)
        return None

def parse_get_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    image_pattarn = re.compile('gallery: JSON.parse\((.*?)\),', re.S)
    result = re.search(image_pattarn,html)
    if result:
        res = result.group(1)
        data = json.loads(json.loads(res))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                dowload_image(image)
            return {
                'url':url,
                'images':images,
                'title':title
            }
    else:
        pass
    # if result:
    #     print(result.group(1))
def save_to_result(result):
    if db[MONGO_TABLE].insert(result):
        print('成功存储到mongodb',result)
        return True
    return False

def dowload_image(url):
    print('正在下载',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_image(content):
    file = '{0}/{1}.{3}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file):
        with open(file,'wb') as f:
            f.write(content)
            f.close()



def main(offset):
    html = get_page_index(offset,'街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_get_detail(html,url)
            if result is not None:
                save_to_result(result)
if __name__ == '__main__':
    group = [x * 20 for x in range(1,20)]
    pool = Pool()
    pool.map(main,group)

