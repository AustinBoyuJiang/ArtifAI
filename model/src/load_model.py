from keras.models import load_model
import numpy as np
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import tensorflow as tf
import matplotlib.pyplot as plt
import ctypes

# Load the model
model = load_model('./models/model.h5')

# Labels for prediction
labels = ['created_with_ai', 'not_created_with_ai']

# Function to preprocess the image
def preprocess_image(image_path, img_size=256):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (img_size, img_size))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Function to generate Grad-CAM heatmap
def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # Get the last convolutional layer
    last_conv_layer = model.get_layer(last_conv_layer_name)
    last_conv_layer_model = tf.keras.Model(model.inputs, last_conv_layer.output)

    # Create a model that maps the last conv layer output to the final model predictions
    classifier_input = tf.keras.Input(shape=last_conv_layer.output.shape[1:])
    x = classifier_input
    for layer in model.layers[model.layers.index(last_conv_layer) + 1:]:
        x = layer(x)
    classifier_model = tf.keras.Model(classifier_input, x)

    with tf.GradientTape() as tape:
        # Compute activations of the last conv layer
        last_conv_layer_output = last_conv_layer_model(img_array)
        tape.watch(last_conv_layer_output)

        # Use the classifier model to compute the predictions from the last conv layer output
        preds = classifier_model(last_conv_layer_output)

        if pred_index is None:
            pred_index = tf.argmax(preds[0]).numpy()

        # Select the relevant score for the predicted class
        class_channel = preds[:, pred_index]

    # Compute gradients with respect to the activations of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This error should not occur if everything is connected properly
    if grads is None:
        raise ValueError(
            "Could not compute gradients. There might be an issue with the model architecture or the gradient computation setup.")

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output.numpy()[0]
    pooled_grads = pooled_grads.numpy()

    # Weight the channels of the last convolutional layer output by the gradients
    for i in range(pooled_grads.shape[-1]):
        last_conv_layer_output[:, :, i] *= pooled_grads[i]

    heatmap = np.mean(last_conv_layer_output, axis=-1)
    heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
    return heatmap


# Overlay the heatmap on the original image
def overlay_heatmap(heatmap, image_path, alpha=0.4):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed_img = heatmap * alpha + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(superimposed_img)
    plt.title('Image with Grad-CAM')
    plt.axis('off')
    plt.show()

# Main function
def main():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    Tk().withdraw()  # Avoid showing the full GUI
    while True:
        image_path = askopenfilename(title='Select an Image', filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
        if image_path:
            processed_img = preprocess_image(image_path)
            predictions = model.predict(processed_img)
            predictions = predictions[0]
            predictions[0] -= min(predictions[0], predictions[1])/2
            predictions[1] = 1-predictions[0]
            print("Predictions:", predictions)
            print("Probability to be created with ai:", round(predictions[0], 4))
            predicted_class_index = int(predictions[1] > 0.5)
            print("Predicted class:", labels[predicted_class_index])

            # Generate heatmap
            heatmap = make_gradcam_heatmap(processed_img, model, 'conv2d_2', predicted_class_index)
            overlay_heatmap(heatmap, image_path)
        else:
            print("No file selected. Exiting.")
            break


if __name__ == "__main__":
    main()
