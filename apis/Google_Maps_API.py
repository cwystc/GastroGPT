import requests
import os
import csv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# print(f"API Key: {GOOGLE_API_KEY}")


def get_nearest_restaurants(location, N=10, keyword=None):
    """
    获取最近的 N 家餐厅，支持可选 keyword（餐厅类别）。
    
    参数：
    - location: (latitude, longitude) 元组，表示搜索中心位置
    - N: 需要获取的餐馆数量
    - keyword: 关键词（如 "korean", "japanese"，如果为 None 则搜索所有餐厅）
    
    返回：
    - 最近的 N 家餐厅信息（列表）
    """

    NEARBYSEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    latitude, longitude = location
    restaurants = []
    next_page_token = None

    while len(restaurants) < N:
        params = {
            "location": f"{latitude},{longitude}",
            "type": "restaurant",  # 限制为餐厅
            "rankby": "distance",  # 按距离排序
            "key": GOOGLE_API_KEY
        }
        if keyword:
            params["keyword"] = keyword  # 只有当 keyword 不为空时才加上筛选条件
        if next_page_token:
            params["pagetoken"] = next_page_token  # 处理翻页

        response = requests.get(NEARBYSEARCH_URL, params=params)
        data = response.json()

        if "results" in data:
            restaurants.extend(data["results"])  # 添加新获取的餐厅
        if "next_page_token" in data:
            next_page_token = data["next_page_token"]
        else:
            break  # 没有更多数据了

        import time
        time.sleep(2)

    return restaurants[:N]  # 只返回 N 家餐厅

def get_restaurant_details(place_id):
    """
    获取单个餐厅的详细信息，包括评分、评论、营业时间、联系方式等。

    参数：
    - place_id: Google Places API 的餐厅唯一 ID

    返回：
    - 餐厅详情（dict）
    """
    DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,
        "fields": "name,rating,formatted_address,formatted_phone_number,opening_hours,reviews",
        "key": GOOGLE_API_KEY
    }
    
    response = requests.get(DETAILS_URL, params=params)
    data = response.json()
    
    if "result" in data:
        return data["result"]
    return None

gt_location = (33.7756, -84.3963)
nearest_restaurants = get_nearest_restaurants(gt_location, N=30, keyword='korean')

# 打开 CSV 文件并写入数据
with open("restaurants.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    
    # 写入表头
    writer.writerow(["Name", "Rating", "Address", "Phone", "Review 1", "Review 2", "Review 3"])

    # 写入每家餐厅的数据
    for restaurant in nearest_restaurants[:10]:
        place_id = restaurant["place_id"]
        details = get_restaurant_details(place_id)

        writer.writerow([
            details["name"],
            details["rating"],
            details["formatted_address"],
            details.get("formatted_phone_number", "N/A"),
            details.get("reviews", [{}])[0].get("text", "")[:],  # 第一条评论
            details.get("reviews", [{}])[1].get("text", "")[:],  # 第二条评论
            details.get("reviews", [{}])[2].get("text", "")[:]   # 第三条评论
        ])

print("data saved to `restaurants.csv` successfully")
