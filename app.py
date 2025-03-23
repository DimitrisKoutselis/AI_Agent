from flask import Flask, request, jsonify
from services.mistral_7b_service import ask_model
from services.rag_service import rag_inference

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

@app.route('/rag', methods=['POST'])
def rag_inference_endpoint():
    data = request.get_json()
    if 'user_input' not in data:
        return jsonify({'error': 'Missing user_input field in request'}), 400

    user_input = data['user_input']
    response = rag_inference(user_input)
    return jsonify({'response': response}), 200