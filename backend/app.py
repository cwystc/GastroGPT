from flask import Flask, request, jsonify
from fetch_maps_data import fetch_and_create_index
from query_llm import answer_to_user

app = Flask(__name__)

# 内存中暂存（测试用，不适合大规模生产）
current_index = None
index_mapping = None


@app.route('/', methods=['GET'])
def home():
    return "<h1>RAG backend is running!</h1>"


@app.route('/rag/ask', methods=['POST'])
def rag_ask():
    global current_index, index_mapping

    data = request.json
    print("🛰️ 收到请求数据:", data)

    question = data.get('question')
    lat = data.get('latitude')
    lon = data.get('longitude')

    if not question or lat is None or lon is None:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        location = (lat, lon)
        print("📍 获取位置:", location)

        current_index, index_mapping = fetch_and_create_index(location)

        print("✅ Index 构建完成，开始调用 LLM")

        answer = answer_to_user(question, current_index, index_mapping)

        print("🎯 LLM 回答:", answer)

        return jsonify({'answer': answer})

    except Exception as e:
        print("❌ 发生错误:", e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
