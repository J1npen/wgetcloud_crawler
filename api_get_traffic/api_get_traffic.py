from flask import Flask, request, jsonify, Response
from . import get_today_traffic
import json
import sys
from pathlib import Path
import cloudscraper
from fake_useragent import UserAgent

def load_json(filename="config.json"):
    # main.py 所在目录
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / filename

    if not config_path.exists():
        sys.exit(1)

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    return config

config = load_json()
WG_COOKIE = config.get("WG_COOKIE")
API_TOKEN = config.get("API_TOKEN")

app = Flask(__name__)

@app.route('/')
def index():
    if request.headers.get('X-API-TOKEN') == None:
        return {"error": "None token"}, 401
    
    input_token_encode = request.headers.get('X-API-TOKEN')
    if input_token_encode != API_TOKEN:
        return {"error": "invalid token"}, 401

    today_traffic_dic = get_today_traffic.traffic(WG_COOKIE)
    traffic = today_traffic_dic.get("traffic")
    today_unit = today_traffic_dic.get("unit")

    result = get_today_traffic.parse_traffic_and_reset_date(WG_COOKIE)
    remain_flow = round(result.get("total_traffic") - result.get("used_traffic"), 2)
    unit = result.get("traffic_unit")
    available_days = result.get("available_days")
    message = f"今日已使用：{traffic}{today_unit}\n剩余流量：{remain_flow}{unit}（{available_days}天）"
    return Response(
    json.dumps({"msg": message}, ensure_ascii=False),
    content_type = "application/json; charset=utf-8"
)

@app.route('/refresh')
def refresh():
    if request.headers.get('X-API-TOKEN') == None:
        return {"error": "None token"}, 401
    
    input_token_encode = request.headers.get('X-API-TOKEN')
    if input_token_encode != API_TOKEN:
        return {"error": "invalid token"}, 401
    
        # initial fake_useragent
    ua = UserAgent()

    # initial cloudscraper
    scraper = cloudscraper.create_scraper()

    url = 'https://katp7luhifu2zxnpy8cs.wgetcloud.org/user/link_on'
    headers = {
        'cookie': WG_COOKIE,
        'User-Agent': ua.random
    }

    if not headers['cookie']:
        return {'error': 'cookie not exists'}
    
    responds = scraper.post(url, headers=headers)

    if responds.status_code != 200:
        return {"error": "request fail"}
    
    return {"msg": "success"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
