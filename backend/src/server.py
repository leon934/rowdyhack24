import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'src/uploads'  # Create an 'uploads' folder where images will be saved
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    filename = file.filename
    print(filename)

    # Basic saving:
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(filepath)
    file.save(filepath) 

    # Conversion - (using Pillow):
    try:
        img = Image.open(filepath)
        img.save(filepath, format='PNG')
        return jsonify({'message': 'Image uploaded and converted to PNG'}), 200
    except Exception as e:
        return jsonify({'error': 'Image conversion failed'}), 500
    
    # TODO: feed image to model and letters
    # TODO: find all possible words with letters

if __name__ == '__main__':
    app.run(debug=True)
