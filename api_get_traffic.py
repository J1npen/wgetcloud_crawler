from flask import Flask, request, jsonify, Response
import get_today_traffic
import hashlib
import os
import json

TOKEN = os.getenv('WG_TOKEN', 'error')

app = Flask(__name__)

@app.route('/')
def index():
    if request.headers.get('X-API-TOKEN') == None:
        return {"error": "None token"}, 401
    
    input_token_encode = hashlib.md5(request.headers.get('X-API-TOKEN').encode())
    if input_token_encode.hexdigest() != TOKEN:
        return {"error": "invalid token"}, 401

    traffic_text = get_today_traffic.traffic()
    return Response(
    json.dumps({"msg": traffic_text}, ensure_ascii=False),
    content_type = "application/json; charset=utf-8"
)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
