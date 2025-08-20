from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
import numpy as np
import cv2
import base64
import os
import json
from io import BytesIO
import tensorflow as tf
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='/public')

# Configure CORS - Use Flask-CORS directly
CORS(app, 
     origins=['*'],  # Allow all origins for testing
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'Accept'],
     supports_credentials=False)  # Disable credentials for wildcard origin

# Load the model and define labels
model = load_model('./models/model.h5')
labels = ['created_with_ai', 'not_created_with_ai']

# Initialize OpenAI
try:
    import openai
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        openai.api_key = openai_api_key
        print("OpenAI API initialized successfully")
    else:
        print("Warning: OPENAI_API_KEY not found in environment variables")
        openai.api_key = None
except ImportError as e:
    print(f"Warning: OpenAI import failed: {e}")
    openai = None

# Initialize SerpAPI
try:
    from serpapi import GoogleSearch
    serp_available = True
    print("SerpAPI initialized successfully")
except ImportError as e:
    print(f"Warning: SerpAPI import failed: {e}")
    serp_available = False


def count_use(cnt):
    json_path = "statistics.json"
    with open(json_path, 'r') as file:
        stats = json.load(file)
    stats['uses'] += cnt
    with open(json_path, 'w') as file:
        json.dump(stats, file)


def image_source(image_data):
    if not serp_available:
        print("Warning: SerpAPI not available, skipping image source search")
        return []
        
    api_key = os.getenv('SERP_API_KEY')
    if not api_key:
        print("Warning: SERP_API_KEY not found, skipping image source search")
        return []
    
    json_path = "data.json"
    with open(json_path, 'r') as file:
        data = json.load(file)
    image_id = data['image id'] + 1
    data['image id'] = image_id
    with open(json_path, 'w') as file:
        json.dump(data, file)
    image_file_path = f'public/{image_id}.png'
    image_data = bytes(image_data)
    with open(image_file_path, 'wb') as file:
        file.write(image_data)
    
    try:
        # Create GoogleSearch instance
        search = GoogleSearch({
            "engine": "google_reverse_image",
            "api_key": api_key,
            "image_url": f"https://artifai.apps.austinjiang.com/public/{image_id}.png"
        })
        results = search.get_dict()
        
        # Clean up temporary file after a delay to ensure API can access it
        import time
        time.sleep(2)  # Wait 2 seconds for API to access the image
        if os.path.exists(image_file_path):
            os.remove(image_file_path)
            
        # Extract results
        if results and results.get("inline_images"):
            results = results["inline_images"]
        else:
            results = []
            
        count_use(len(results))
        return results
    except Exception as e:
        print(f"Error in image source search: {e}")
        # Clean up temporary file on error
        if os.path.exists(image_file_path):
            os.remove(image_file_path)
        return []


def preprocess_image(image, img_size=256):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR format
    img = cv2.resize(img, (img_size, img_size))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    last_conv_layer = model.get_layer(last_conv_layer_name)
    last_conv_layer_model = tf.keras.Model(model.inputs, last_conv_layer.output)

    classifier_input = tf.keras.Input(shape=last_conv_layer.output.shape[1:])
    x = classifier_input
    for layer in model.layers[model.layers.index(last_conv_layer) + 1:]:
        x = layer(x)
    classifier_model = tf.keras.Model(classifier_input, x)

    with tf.GradientTape() as tape:
        last_conv_layer_output = last_conv_layer_model(img_array)
        tape.watch(last_conv_layer_output)
        preds = classifier_model(last_conv_layer_output)

        if pred_index is None:
            pred_index = tf.argmax(preds[0]).numpy()
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output.numpy()[0]
    pooled_grads = pooled_grads.numpy()

    for i in range(pooled_grads.shape[-1]):
        last_conv_layer_output[:, :, i] *= pooled_grads[i]

    heatmap = np.mean(last_conv_layer_output, axis=-1)
    heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
    return heatmap


def overlay_heatmap(heatmap, original_img, alpha=0.4):
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed_img = heatmap * alpha + original_img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)

    # Convert to base64
    buffered = BytesIO()
    img_encoded = cv2.cvtColor(superimposed_img, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.png', img_encoded)
    buffered.write(buffer)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def gpt(content):
    if not openai or not openai.api_key:
        return "Sorry, the GPT service is currently unavailable due to missing API configuration."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            messages=content,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in GPT request: {e}")
        return f"Sorry, there was an error processing your request: {str(e)}"


@app.route('/detect', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['*'], supports_credentials=False)
def predict():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        print("Starting /detect request processing...")
        count_use(4)
        
        # Parse JSON data
        try:
            data = request.get_json(force=True)
            if 'image' not in data:
                return jsonify({'error': 'No image provided'}), 400
        except Exception as e:
            print(f"JSON parsing error: {e}")
            return jsonify({'error': 'Invalid JSON data'}), 400

        # Decode the base64 image
        try:
            image_data = base64.b64decode(data['image'])
            image = np.array(Image.open(BytesIO(image_data)))
            print(f"Image decoded successfully, shape: {image.shape}")
        except Exception as e:
            print(f"Image decoding error: {e}")
            return jsonify({'error': 'Invalid image data'}), 400

        # Process image with AI model
        try:
            processed_img = preprocess_image(image)
            print("Image preprocessed successfully")
            
            predictions = model.predict(processed_img, verbose=0)  # Disable verbose output
            predictions = predictions[0]
            predicted_class_index = int(predictions[1] > 0.5)
            print(f"Model prediction completed: {predictions.tolist()}")
        except Exception as e:
            print(f"AI model error: {e}")
            return jsonify({'error': 'AI model processing failed', 'details': str(e)}), 500

        # Generate heatmap
        try:
            heatmap = make_gradcam_heatmap(processed_img, model, 'conv2d_2', predicted_class_index)
            heatmap_image_base64 = overlay_heatmap(heatmap, image)
            print("Heatmap generated successfully")
        except Exception as e:
            print(f"Heatmap generation error: {e}")
            # Continue without heatmap
            heatmap_image_base64 = ""

        # Skip image source search for now to isolate the issue
        sources = []  # Temporarily disable image source search
        
        print("Returning successful response...")
        return jsonify({
            "error": None,
            "predictions": predictions.tolist(),
            "heatmap": heatmap_image_base64,
            "sources": sources,
        })
    except Exception as e:
        print(f"Unexpected error in /detect endpoint: {e}")
        return jsonify({'error': 'Failed to process the image', 'details': str(e)}), 500


@app.route('/query', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['*'], supports_credentials=False)
def query():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        content = request.get_json(force=True)
        count_use(len(content))
        return jsonify({
            "error": None,
            "response": gpt(content),
        })
    except Exception as e:
        return jsonify({'error': 'Failed to process the message', 'details': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "artifa-backend", "port": "3000"}), 200


@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "ArtifAI Backend API", "status": "running"}), 200


@app.route('/test-static', methods=['GET'])
def test_static():
    """Test endpoint to verify static file serving"""
    try:
        # Check if public directory exists and is accessible
        public_dir = os.path.join(os.getcwd(), 'public')
        if os.path.exists(public_dir):
            files = os.listdir(public_dir)
            return jsonify({
                "status": "success",
                "public_dir": public_dir,
                "files": files,
                "static_url_path": app.static_url_path,
                "static_folder": app.static_folder
            }), 200
        else:
            return jsonify({"status": "error", "message": "Public directory not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500








if __name__ == '__main__':
    # For development only
    app.run(debug=True, host='0.0.0.0', port=5000)