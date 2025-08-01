from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tifffile
from tensorflow.keras.models import load_model

# Flask setup
app = Flask(__name__)

# Load Model
MODEL_PATH = 'Model/UNet_ResNet34_model.keras'
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    model = None
    print("Error: Model not found!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Build a folder to save the image; to help in prediction
        app.config['UPLOAD_FOLDER'] = 'uploads'
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print(f"[INFO] File saved: {filepath}")

        # Read image
        image = tifffile.imread(filepath)
        print(f"[INFO] Image shape: {image.shape}")

        # Preprocess image
        input_img = preprocess_image(image)
        print(f"[INFO] Image preprocessed: {input_img.shape}")

        # Predict mask
        pred = model.predict(np.expand_dims(input_img, axis=0))[0, :, :, 0]
        mask = pred >= 0.5

        # Save predicted mask
        mask_io = BytesIO()
        plt.imsave(mask_io, mask, cmap='gray', format='png')
        mask_io.seek(0)
        mask_b64 = base64.b64encode(mask_io.getvalue()).decode()

        # Save bands visualization
        band_io = BytesIO()
        visualize_image_bands(image, save_obj=band_io)
        band_io.seek(0)
        bands_b64 = base64.b64encode(band_io.getvalue()).decode()

        # Build response with correct relative paths
        response = {
            'mask': f"data:image/png;base64,{mask_b64}",
            'bands': f"data:image/png;base64,{bands_b64}"
        }

        print("[INFO] JSON Response:", response)
        print("[INFO] Prediction complete.")
        return jsonify(response)

    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Delete the folder used to store image during prediction
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
            print(f"[INFO] Deleted uploads folder: {app.config['UPLOAD_FOLDER']}")

# Preprocess input image
BAND_STATS_PATH = 'Deployment/static/band_stats.csv'
band_stats_df = pd.read_csv(BAND_STATS_PATH)
global_mins = band_stats_df['Min'].values
global_maxs = band_stats_df['Max'].values

def preprocess_image(image):
    num_bands = image.shape[-1]

    norm_img = np.zeros_like(image, dtype=np.float32)
    for b in range(num_bands):
        norm_img[:, :, b] = (image[:, :, b] - global_mins[b]) / (global_maxs[b] - global_mins[b] + 1e-5)

    return norm_img

# Bands Visualization
BAND_LABELS = ['Coastal aerosal', 'Blue', 'Green', 'Red', 'NIR', 'SWIR1', 'SWIR2',
                'QA Band', 'Merit DEM', 'Copernicus DEM', 'ESA world cover map',
                'Water occurence probability']

def visualize_image_bands(image, save_obj=None):
    num_bands = image.shape[-1]
    fig, axes = plt.subplots(1, num_bands, figsize=(25, 3))
    
    for i in range(num_bands):
        ax = axes[i]
        ax.imshow(image[:, :, i], cmap='gray')
        ax.set_title(f'Band {i+1}\n{BAND_LABELS[i]}', fontsize=8)
        ax.axis('off')

    plt.tight_layout()
    if save_obj:
        plt.savefig(save_obj, format='png', bbox_inches='tight')
    else:
        plt.show()
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)
