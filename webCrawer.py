import requests
import urllib
import re
from bs4 import BeautifulSoup

## 打开网页
# base_url 不仅打开目标网站 还包括了筛选信息 这个程序筛选的信息为MA/MA
base_url = "http://www.us168tc.com/cis/Transfer/Index/rtf?AreaIds=0dc46e6e-70f4-4f28-9e91-e8866c137de5&AreaIds=0dc46e6e-70f4-4f28-9e91-e8866c137de5&AreaId=0dc46e6e-70f4-4f28-9e91-e8866c137de5"
# 头内容 固定格式 不用管
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
# 获得base_url网页内容
r = requests.get(base_url, headers= headers)
# r.text为提取获得网页内容的纯HTML内容
main_page = r.text



##分析获取的HTML内容
analyze = BeautifulSoup(main_page,"lxml")
#找到所有标签为li并且class为individual-page的标签内容 目的： 遍历之后的所有网页
pages = analyze.findAll("li",{"class":"individual-page"})
#插入0元素到pages头部 目的：遍历遍历到主页
pages.insert(0,None)
print(pages)
#所有的page循环遍历
for page in pages:
    #如果page本身不是空，
    if not(page == None):
        # redirect网页地址 组成： baseurl + 目录所对应的href redirect
        redirect = base_url+page.a.get("href")
    else:
        # 如果当前pages为空 直接访问baseurl网页 对应： 0元素
        redirect = base_url
    #抓取当前网页所有内容并用beautifulsoup分析
    main_page = requests.get(redirect).text
    analyze = BeautifulSoup(main_page,"lxml")
    # 搜寻当前网页所有的shops信息 对应标签 a class=t
    shops = analyze.findAll("a",{"class":"t"})
    #遍历所有的shops
    for shop in shops:
        # shop所对应的HTML网页地址
       redirect_page = "http://www.us168tc.com"+shop.get("href")
       print(shop.get_text())
       # get到子网页地址并分析
       second_page = requests.get(redirect_page).text
       second_analyze = BeautifulSoup(second_page,"lxml")
       #搜寻租金信息
       rent = second_analyze.find(text=re.compile("租金")).strip()
       print(rent)
       #搜寻类别信息
       category = second_analyze.find(text=re.compile("类别")).strip()
       print(category)
       #搜寻位置信息
       area = second_analyze.find(text=re.compile("区域")).strip()
       print(area)
    print('-----------------------------------')
