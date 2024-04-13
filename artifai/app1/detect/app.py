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
from serpapi import GoogleSearch

app = Flask(__name__)
CORS(app)

# Load the model and define labels
model = load_model('./models/model.h5')
labels = ['created_with_ai', 'not_created_with_ai']


def count_use(cnt):
    json_path = "../../statistics.json"
    with open(json_path, 'r') as file:
        stats = json.load(file)
    stats['uses'] += cnt
    with open(json_path, 'w') as file:
        json.dump(stats, file)


def image_source(image_data):
    json_path = "data.json"
    with open(json_path, 'r') as file:
        data = json.load(file)
    image_id = data['image id'] + 1
    data['image id'] = image_id
    with open(json_path, 'w') as file:
        json.dump(data, file)
    image_file_path = f'../../public/{image_id}.png'
    image_data = bytes(image_data)
    with open(image_file_path, 'wb') as file:
        file.write(image_data)
    with open('../../api.json', 'r') as file:
        api_key = json.load(file)['serp-api-key']
    params = {
        "engine": "google_reverse_image",
        "api_key": api_key,
        "image_url": f"http://artifai.aj-coder.com/public/{image_id}.png",
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if os.path.exists(image_file_path):
        os.remove(image_file_path)
    if results.get("inline_images"):
        results = results["inline_images"]
    else:
        results = []
    count_use(len(results))
    return results


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


@app.route('/detect', methods=['POST'])
def predict():
    try:
        count_use(4)
        data = request.get_json(force=True)
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        # Decode the base64 image and convert it to a NumPy array
        image_data = base64.b64decode(data['image'])
        image = np.array(Image.open(BytesIO(image_data)))

        processed_img = preprocess_image(image)
        predictions = model.predict(processed_img)
        predictions = predictions[0]
        predicted_class_index = int(predictions[1] > 0.5)

        heatmap = make_gradcam_heatmap(processed_img, model, 'conv2d_2', predicted_class_index)
        heatmap_image_base64 = overlay_heatmap(heatmap, image)

        return jsonify({
            "error": None,
            "predictions": predictions.tolist(),
            "heatmap": heatmap_image_base64,
            "sources": image_source(image_data),
        })
    except Exception as e:
        return jsonify({'error': 'Failed to process the image', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
