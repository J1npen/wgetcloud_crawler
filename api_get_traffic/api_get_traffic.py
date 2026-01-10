from flask import Flask, request, jsonify, Response
from . import get_today_traffic
import json
import sys
from pathlib import Path

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

    traffic_dic = get_today_traffic.traffic(WG_COOKIE)
    traffic = traffic_dic.get("traffic")
    unit = traffic_dic.get("unit")
    return Response(
    json.dumps({"msg": f"今日已使用 {traffic}{unit} "}, ensure_ascii=False),
    content_type = "application/json; charset=utf-8"
)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
