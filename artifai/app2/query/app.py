from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import json

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key='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',
)


def count_use(cnt):
    json_path = "../../statistics.json"
    with open(json_path, 'r') as file:
        stats = json.load(file)
    stats['uses'] += cnt
    with open(json_path, 'w') as file:
        json.dump(stats, file)


def gpt(content):
    message = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.3,
        max_tokens=2048,
        messages=content,
    )
    return message.choices[0].message.content


@app.route('/query', methods=['POST'])
def query():
    try:
        content = request.get_json(force=True)
        count_use(len(content))
        return jsonify({
            "error": None,
            "response": gpt(content),
        })
    except Exception as e:
        return jsonify({'error': 'Failed to process the message', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
