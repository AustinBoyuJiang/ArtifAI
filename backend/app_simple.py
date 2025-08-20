from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS
CORS(app, 
     origins=['*'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'Accept'],
     supports_credentials=False)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "artifa-backend", "port": "3000"}), 200

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "ArtifAI Backend API", "status": "running"}), 200

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test endpoint working"}), 200

@app.route('/detect', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        return jsonify({
            "error": None,
            "predictions": [0.5, 0.5],
            "heatmap": "",
            "sources": [],
            "message": "Simplified detect endpoint"
        })
    except Exception as e:
        return jsonify({'error': 'Failed to process the image', 'details': str(e)}), 500

@app.route('/query', methods=['POST', 'OPTIONS'])
def query():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        return jsonify({
            "error": None,
            "response": "Simplified query endpoint working",
        })
    except Exception as e:
        return jsonify({'error': 'Failed to process the message', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
