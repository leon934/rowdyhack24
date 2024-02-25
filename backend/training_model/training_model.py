import cv2 as cv
import os

count = 1

for image in os.listdir('./data_content/preprocessed_images'):
    img = cv.imread(f"./data_content/preprocessed_images/{image}", 0)

    image = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
    
    cv.imwrite(f'./data_content/processed_images/{count}.png', image)
    count += 1

with open('positive_images.txt', 'w') as file:
    for i in range(1, 55):
        file.write(f'C:/Users/leonl/Documents/GitHub/rowdyhack24/backend/training_model/data_content/processed_images/{i}.png\n')