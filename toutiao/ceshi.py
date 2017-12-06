import requests
import re
import json

response = requests.get('https://www.toutiao.com/a6495303154979045901/')
cool = response.text
# image_pattarn = re.compile('BASE_DATA.galleryInfo = (.*?)</script>', re.S)
#result = re.search(image_pattarn,cool)
ii_pattern = re.compile('gallery: JSON.parse\((.*?)\),', re.S)
result = re.search(ii_pattern,cool)
res = result.group(1)
# res_s = result_q.group(1)
# dd = res.replace("\\","")
dd = json.loads(res)
print(type(dd))
sss = json.loads(dd)
print(type(sss))
# for key,value in dd.item():
#     print(key,value)

if sss and 'sub_images' in sss.keys():
    sub_images = sss.get('sub_images')
    print(sub_images)
    images = [item.get('url') for item in sub_images]
    print(images)
    print(type(images))

# ll = dd_s['url']

# print(res)
# # print(res_s)
# print(dd)
# print(sss)
# # print(dd)
# print(type(sss))
# print(dd)
# print(type(res))
# dd = json.loads(res.replace("'",'"'))
# dd = json.loads(ss)
#
# print(dd)
# print(type(dd))
