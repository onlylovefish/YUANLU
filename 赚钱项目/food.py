#%%
import requests        #加载requests库
from bs4 import BeautifulSoup         #加载BeautifulSoup库

res_foods = requests.get('http://www.xiachufang.com/explore/')     #从网站获取数据
bs_foods = BeautifulSoup(res_foods.text,'html.parser')       #解析数据
list_foods = bs_foods.find_all('div',class_ = 'info pure-u')     #找到我们需要提取数据的最小父级标签
list_all = []       #创建空列表
for food in list_foods:            #因为有多个层级的标签，需要使用循环进行操作
	tag_a = list_foods[0].find('a')      #我们只提取第一个数据，所以别忘记加入角标[0],再接着寻找正确的标签
	name = tag_a.text.strip()       #获取菜名
	url = 'http://www.xiachufang.com'+tag_a['href']       #获取网址链接
	tag_p = food.find('p',class_ = 'ing ellipsis')       #提取食材信息
	shi_c = tag_p.text.strip()         #得到食材的信息
	list_all.append([name,url,shi_c])         #将菜名，链接，食材添加到列表中
print(list_all)


# %%
