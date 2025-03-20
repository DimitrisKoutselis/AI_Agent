from flask import Flask, request, jsonify
from services.mistral_7b_service import ask_model

app = Flask(__name__)

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({'message': 'API is working correctly'}), 200

@app.route('/process_query', methods=['POST'])
def process_query():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'Missing text field in request'}), 400

    query = data['text']
    answer = ask_model(query)
    try:
        articles = answer["articles"]
        return jsonify(articles), 200
    except TypeError:
        return jsonify(answer), 200