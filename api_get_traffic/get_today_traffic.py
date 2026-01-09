import json
import cloudscraper
from fake_useragent import UserAgent
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import re

# initial fake_useragent
ua = UserAgent()

# initial cloudscraper
scraper = cloudscraper.create_scraper()

today = date.today()
yesterday = today - timedelta(days=1)

def parse_traffic_and_reset_date(cookie: str) -> dict:
    # scrap the web page from the url
    url = "https://3jkkvi9afjjln2yjwnbc.wgetcloud.org/user"
    headers = {
        "cookie": cookie,
        "User-Agent": ua.random
    }
    if not headers['cookie']:
        return {'error': 'cookie not exists'}
    html = scraper.get(url, headers=headers).text

    # use beautiful soup to scrap the remaining traffic from the web page
    soup = BeautifulSoup(html, "html.parser")
    result = {}
    card = soup.select_one("div.card-body.border-top")

    if not card:
        return {"error": "card-body not found"}
    
    for small in card:
        text = small.get_text(strip=True)
        
        if text.startswith("已使用/总流量"):
            m = re.search(
                r"已使用/总流量：\s*([\d.]+)\s*/\s*([\d.]+)\s*([A-Za-z]+)",
                text,
            )
            if m:
                result["used_traffic"] = float(m.group(1))
                result["total_traffic"] = float(m.group(2))
                result["traffic_unit"] = m.group(3)
                result["raw_traffic"] = text
        
        elif text.startswith("重置日期"):
            m = re.search(r"重置日期：\s*(\d{4}-\d{2}-\d{2})", text)
            if m:
                result["reset_date"] = m.group(1)
                result["raw_reset_date"] = text

                # Calculate the number of days until the traffic reset date
                target_date = datetime.strptime(m.group(1), "%Y-%m-%d").date()
                available_days = (target_date - today).days
                result["available_days"] = available_days

    if "used_traffic" not in result or "reset_date" not in result:
        result["warning"] = "some fields not found"

    # result: {'used_traffic': 71.16, 'total_traffic': 320.0, 'traffic_unit': 'G', 
    #          'raw_traffic': '已使用/总流量：71.16/320 G剩余：78%', 
    #          'reset_date': '2026-01-17', 'raw_reset_date': '重置日期：2026-01-17'}
    return result

def traffic(cookie):
    # request body data
    date_str = f"{yesterday} 至 {today}"
    data = {
        'date': date_str,
        'email': ''
    }

    url = 'https://3jkkvi9afjjln2yjwnbc.wgetcloud.org/user/log_month'
    headers = {
        'cookie': cookie,
        'User-Agent': ua.random
    }

    if not headers['cookie']:
        return {'error': 'cookie not exists'}
    
    responds = scraper.post(url, data=data, headers=headers)

    # print(responds)  # <Response [200]>
    # print(responds.status_code)  # 200
    # print(responds.text)  # {"date":["2025-12-15","2025-12-16"],"t":[10.91,0.73],"t_u":[0.06,0.05],"t_d":[10.85,0.68]}

    data_dict = responds.json() # {'date': ['2025-12-15', '2025-12-16'], 't': [10.91, 0.74], 't_u': [0.06, 0.06], 't_d': [10.85, 0.68]}
    traffic = data_dict.get('t')[1]

    # Automatically determine the unit of flow
    if traffic < 1:
        traffic *= 1000
        unit = "M"
        # return f'今日已使用 {traffic}M'
    else:
        unit = "G"
        # return f'今日已使用 {traffic}G'
    
    return {
        "traffic": traffic,
        "unit": unit,
    }
    
if __name__ == "__main__":
    cookie = input("Input your cookie: ")
    result = parse_traffic_and_reset_date(cookie)
    print(result)