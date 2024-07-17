from scripts import rv
from flask import Flask, request, jsonify
from utils import setup_logger

app = Flask(__name__)


@app.route('/run_ai_test', methods=['POST'])
def run_ai_test():
    data = request.json
    path = data.get('path')
    if not path:
        return jsonify({'error': 'No path provided'}), 400
    try:
        status = rv.rv_ai_test(path)
        return jsonify({'status': status})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    setup_logger()
    app.run(debug=True)
    