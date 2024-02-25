import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from Trie import Trie
from mapper import *
from solver import *

from imageprocessing import *

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

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
    except Exception as e:
        return jsonify({'error': 'Image conversion failed'}), 500
    
    # TODO: feed image to model and letters

    img = cv2.imread('C:/Users/leonl/Documents/GitHub/rowdyhack24/backend/src/uploads/image.png')
    img = board_capture(img)
    inv_img = invert_color(img)
    arr = create_grid(inv_img)

    verticals, horizontals, singles = create_matrix(arr)

    # TODO: find all possible words with letters
    def load_word_list(filepath):
        with open(filepath) as file:
            return [word.strip().lower() for word in file]

    word_list = load_word_list(r'backend\src\Collins_Scrabble_Words_2019.txt')

    def build_trie(word_list):
        trie = Trie()
        for word in word_list:
            trie.insert(word)
        return trie
        
    trie = build_trie(word_list)
    
    h_map = get_h_map(verticals, horizontals, singles)
    v_map = get_v_map(verticals, horizontals, singles)

    permutations = solve_recursive_permutations(h_map, trie) + solve_recursive_permutations(v_map, trie)
    unique_list = list(set(permutations))
    sorted_list = sorted(unique_list, key=len, reverse=True)

    return jsonify(success=True, data=sorted_list), 200


if __name__ == '__main__':
    app.run(debug=True)
