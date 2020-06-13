# 导入相关库
import requests
from bs4 import BeautifulSoup

# 导入Django orm
import sys
import os
# import django
# sys.path.append(os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))))
# os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
# django.setup()

# 导入Model
# from SS.models import Foods

# 排行榜入口url
Top_food_url = 'http://top.meishi.cc/lanmu.php?cid=3'

# 家常菜谱入口url
Home_food_url = 'http://top.meishi.cc/lanmu.php?cid=13'

# 中华菜系入口url
China_food_url = 'http://top.meishi.cc/lanmu.php?cid=2'

# 外国菜入口url
Foreign_food_url = 'http://top.meishi.cc/lanmu.php?cid=10'


def get_html_text(url):
    '''获取html文本'''
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
        # print(r.text)
    except:
        return 'error'


def parse_city_id(url):
    '''解析对应的城市排行榜连接'''

    res = []
    html = get_html_text(url)
    # 做一个简单的判断
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        # 定位到 全国各地特色小吃排行榜分类,<div>
        cityids = soup.find('div', class_='rank_content_top')
        for city in cityids.find_all('a'):
            res.append({'name': city.text, 'url': city['href']})
        return res
    else:
        print('error !!!!')


def parse_food_info(url):
    '''解析对应的美食信息'''

    html = get_html_text(url)
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        # 定位到具体排行榜的位置
        foods = soup.find('div', class_='rank_content_top10_wraper')
        # 开始解析信息
        for food in foods.find_all('li'):
            # 寻找 食品名、做法链接、图片链接
            content = food.find('a', class_='img')
            name = content['title']
            detial_url = content['href']
            img_url = content.img['src']
            print('正在解析美食：{}'.format(name))
            # 构造一个生成器，分别返回 食物名,做法链接,图片链接
            yield name, detial_url, img_url
    else:
        print('error !!!!')


# def save_data(name, cate, detail_url, img_url):
#     '''利用django orm 存储记录'''
#     obj = Foods.objects.create(
#         name=name, cate=cate, detail_link=detail_url, img_link=img_url)
#     print('{}保存完毕'.format(name))


def main():
    '''程序入口'''
    # 构造所有起始url列表
    url_list = [Top_food_url, Home_food_url, China_food_url, Foreign_food_url]
    # 找到所有城市排行榜的url
    for url in url_list:
        print(url)
        # 找到该分类下的所有cid
        res = parse_city_id(url)
        for page in res:
            # 找到菜系名称
            cate = page['name']
            # 利用生成器迭代返回结果
            for food_name, detail_url, img_url in parse_food_info(page['url']):
                #  save data
                # 用try except结构 防止菜名重复
                try:
                    print(food_name,cate,detail_url,img_url)
                    # save_data(food_name, cate, detail_url, img_url)
                except:
                    print("hah")
                    pass


# def get_random_food():
#     '''从数据库随机抓取菜品'''
#     food = Foods.objects.order_by('?')[0]
#     text = '名字：{}\n\n菜系：{}\n\n做法：{}\n\n图片：{}\n\n不满意？再试一次'.format(
#         food.name, food.cate, food.detail_link, food.img_link)
#     return text