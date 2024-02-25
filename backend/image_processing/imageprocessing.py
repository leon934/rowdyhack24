import pytesseract
import cv2
import numpy as np

arr = [['']* 8] * 9

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('C:/Users/leonl/Documents/GitHub/rowdyhack24/backend/image_processing/testing/test_cases/testcase2.jpg')

def invert_color(image): # Makes the board parseable for create_board_matrix to go through.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    return invert

def create_grid(image):
    arr = []

    height, width = image.shape
    counter = 1
    square_height = round(height / 9)
    square_width = round(width / 8)

    for i in range(9):
        line = ''
        for j in range(8):
            image_slice = image[square_height * i:square_height * (i + 1), square_width * j:square_width * (j + 1)]
            img_height, img_width = image_slice.shape

            image_slice[0:img_height, 0:6] = 255
            image_slice[0:6, 0:img_width] = 255
            image_slice[0:img_height, img_width - 6:img_width] = 255
            image_slice[img_height - 6:img_height, 0:img_width] = 255
            
            # image_slice = cv2.copyMakeBorder(image_slice, 50,50,50,50, cv2.BORDER_CONSTANT, value=255)
            # image_slice = cv2.resize(image_slice, dsize=(300, 300))

            # Not required; used for testing purposes.
            filename = f'C:/Users/leonl/Documents/GitHub/rowdyhack24/backend/image_processing/squares/{counter}.png'
            cv2.imwrite(filename, image_slice)

            # Accounts for false positives by finding the black pixel to white pixel ratio.
            # black_pixel_ratio = (np.count_nonzero(image_slice == 0)) / (47 * 47) * 100

            inner_black_pixel_ratio = (np.count_nonzero(image_slice[6:img_height - 6, 6:img_width - 6] == 0)) / (35 * 35) * 100

            image_slice = clear_black_bars(image_slice, inner_black_pixel_ratio, img_height, img_width)

            # Converts the image into a string and cleans it up.
            value = pytesseract.image_to_string(filename, config=r'--psm 7')
            value = value.strip()

            # print(f'{value} BPR: {black_pixel_ratio}; IBPR: {inner_black_pixel_ratio}; WIDTH: {img_width}; HEIGHT: {img_height}; LEFT COUNT: {np.count_nonzero(image_slice[0:img_height, 6:7] == 0)}; BOTTOM COUNT: {np.count_nonzero(image_slice[img_height - 7:img_height - 7 + 1, 0:width] == 0)}; RIGHT COUNT: {np.count_nonzero(image_slice[0:img_height, img_width - 7:img_width - 6] == 0)}')



            if value and inner_black_pixel_ratio < 80:
                if len(value) >= 2: # stupid edge case
                    value = value[0]

                value = value.upper()

                if value == '°':
                    value = 'O'

                line += value + " "
            else: # Used for testing purposes.

                value = '#'
                line += value + " "
                
            value = ''
            counter += 1
        
        line.strip()
        arr.append(line.split(" "))

        print(line)

        new_arr = [[x[:-1] for x in row] for row in arr]

# Using numpy
        new_arr = np.delete(arr, -1, axis=1)

    return new_arr

def clear_black_bars(image, ratio, height, width):
    n = 6

    side = [False, False, False, False]
    side_amt = [0, 0, 0, 0]

    while ratio < 90 and np.count_nonzero(image[0:height, n:n + 1] == 0) / (height - 12) >= 0.9:  # left
        side[0] = True
        side_amt[0] += 1
        n += 1

    n = 6  # Reset n for the next loop

    while ratio < 90 and np.count_nonzero(image[0:height, width - n - 1:width - n] == 0) / (height - 12) >= 0.9:
        side[1] = True
        side_amt[1] += 1
        n += 1
    
    n = 6  # Reset n for the next loop

    while ratio < 90 and np.count_nonzero(image[n:n + 1, 0:width] == 0) / (width - 12) >= 0.9:
        side[2] = True
        side_amt[2] += 1
        n += 1

    n = 6  # Reset n for the next loop

    while ratio < 90 and np.count_nonzero(image[height - n - 1:height - n, 0:width] == 0) / (width - 12) >= 0.9:
        side[3] = True
        side_amt[3] += 1
        n += 1

    # Update the image values
    if side[0]:
        for j in range(side_amt[0]):
            image[0:height, j + 6:j + 7] = 255

    if side[1]:
        for j in range(side_amt[1]):
            image[0:height, width - j - 7:width - j - 6] = 255

    if side[2]:
        for j in range(side_amt[2]):
            image[height - j + 6:height - j + 7, 0:width] = 255

    if side[3]:
        for j in range(side_amt[3]):
            image[height - j - 6:height - j - 5, 0:width] = 255

    return image
    

def test_image(image):
    cv2.imwrite('C:/Users/leonl/Documents/GitHub/rowdyhack24/backend/image_processing/testing/test_result/testresult2.jpg', image)

def create_matrix(board):
    vert_matrix, horizontal_matrix, single_matrix = [], [], []

    for i in range(9):
        for j in range(8):
            current_value = board[i][j]

            # Check right
            right_value = board[i][j + 1] if j + 1 < 8 else ' '
            if current_value != ' ' and right_value != ' ':
                horizontal_matrix.append(current_value + right_value)
            elif current_value != ' ':
                single_matrix.append(current_value)

            # Check below
            below_value = board[i + 1][j] if i + 1 < 9 else ' '
            if current_value != ' ' and below_value != ' ':
                vert_matrix.append(current_value + below_value)

    return vert_matrix, horizontal_matrix, single_matrix

board = [
    ['E', 'C', ' ', ' ', 'G', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'I', ' ', 'E', ' '],
    [' ', 'I', 'H', ' ', ' ', ' ', ' ', 'F'],
    ['H', ' ', ' ', ' ', 'F', ' ', ' ', ' '],
    ['D', ' ', ' ', 'H', ' ', 'C', ' ', ' '],
    [' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
    [' ', 'F', ' ', ' ', ' ', ' ', 'B', 'H'],
    [' ', ' ', ' ', ' ', 'A', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'H', ' ', ' ', 'G']
]

vert, horiz, single = create_matrix(board)
print("Vertical Matrix:", vert)
print("Horizontal Matrix:", horiz)
print("Single Matrix:", single)


