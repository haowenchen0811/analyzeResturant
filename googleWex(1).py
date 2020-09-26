import requests
import urllib
from urllib.parse import quote
## 此程序运行前必须先拿到Google_Place API_KEY 和 Wextractor API_KEY 否则无法运行！
## 请注意调取次数 调取次数有限！！！

## 谷歌的API_KEY （自行输入 已省略）
API_KEY = "XXXXXXXXXXXXXXXX"

## Wextractor 的 API_KEY (自行输入 已省略)
WEX_KEY = "XXXXXXXXXXXXXXXX"

## 谷歌Place Search 和 Details的网址入口
PLACE_SEARCH = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
PLACE_DETAIL = "https://maps.googleapis.com/maps/api/place/details/output?"

## Wextractor 的 网址入口
WEX_REVIEW = "https://wextractor.com/api/v1/reviews?id="

## 波士顿经纬度坐标
Boston_location = ["42.361145","-71.057083"]

## 文本搜索 使用 Google 引擎
## 根据搜索内容，位置信息和半径信息返回目标位置信息指定半径内符合搜索内容的地点
## 输入: 搜索内容（String），位置信息（2 elements list），半径信息（number）
## 输出: JSON格式的结果
def text_search(content,location,radius):
    search_website = f"{PLACE_SEARCH}{quote(content)}&location={location[0]},{location[1]}&radius={radius}"         
    search_website = search_website + "&key=" + API_KEY 
    print(search_website)
    response = requests.request('GET',search_website)
    return response.json()

## 返回指定位置的reviews信息 一次返回10个
## 输入: place_reference信息
## 输出: JSON格式的结果
def place_reviews(place_reference):
    auth_token = "&auth_token="
    website = f"{WEX_REVIEW}{place_reference}{auth_token}{WEX_KEY}"
    response = requests.request('GET',website)
    return response.json()


## 这是一个调取示例 写完程序后一定要谨慎运行 因为Wextractor调取次数十分有限！！！！
## 以下代码为示例 可删除
results = text_search("Chinese",Boston_location,500)
for result in results["results"]:
    print(result["name"])
    print(result["reference"])
    print(place_reviews(result["reference"]))

    

    