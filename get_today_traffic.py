import json
import cloudscraper
from fake_useragent import UserAgent
from datetime import date, timedelta
import os

def traffic():
    # initial fake_useragent
    ua = UserAgent()

    # initial cloudscraper
    scraper = cloudscraper.create_scraper()

    # request body data
    today = date.today()
    yesterday = today - timedelta(days=1)
    date_str = f"{yesterday} 至 {today}"
    data = {
        'date': date_str,
        'email': ''
    }

    url = 'https://3jkkvi9afjjln2yjwnbc.wgetcloud.org/user/log_month'
    headers = {
        'cookie': os.getenv('WG_COOKIE', ''),
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
        return f'今日已使用 {traffic}M'
    else:
        return f'今日已使用 {traffic}G'