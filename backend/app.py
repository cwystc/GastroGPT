from flask import Flask, request, jsonify, send_from_directory
from fetch_maps_data import fetch_and_create_index
from query_llm import answer_to_user
import os

import logging

from flask_cors import CORS, cross_origin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



app = Flask(__name__, static_folder='../rag-frontend/build', static_url_path='')
# print("✅ 初始化 CORS 前")
CORS(app, supports_credentials=True)
# print("✅ 初始化 CORS 后")

# CORS(app)  # ✅ 最通用、无路径限制
# CORS(app, resources={r"/rag/*": {"origins": "*"}})
# CORS(app, supports_credentials=True)


current_index = None
index_mapping = None

@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/rag/init', methods=['POST', 'OPTIONS'])
@cross_origin()
def rag_init():
    global current_index, index_mapping
    data = request.json
    lat = data.get('latitude')
    lon = data.get('longitude')
    if lat is None or lon is None:
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        location = (lat, lon)
        current_index, index_mapping = fetch_and_create_index(location)
        return jsonify({'message': 'Index initialized successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rag/ask', methods=['POST', 'OPTIONS'])
@cross_origin()
def rag_ask():
    global current_index, index_mapping
    data = request.json
    question = data.get('question')
    lat = data.get('latitude')
    lon = data.get('longitude')

    logging.info(f"🛰️ 收到问题: {question}")
    logging.info(f"📍 经纬度: ({lat}, {lon})")

    if not question or lat is None or lon is None:
        return jsonify({'error': 'Missing required fields'}), 400
    if current_index is None or index_mapping is None:
        return jsonify({'error': 'Index not initialized. Please fetch location first.'}), 400
    try:
        answer = answer_to_user(question, current_index, index_mapping)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
