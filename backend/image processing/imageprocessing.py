import cv2 as cv
# import numpy as np

from matplotlib import pyplot as plt

img = cv.imread('./test_images/WIN_20240224_14_33_38_Pro.png',0)
# img = cv.imread('./test_images/wordbite.png', 0)

th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)

images = [img, th3]
titles = ['Original Image', 'Gaussian Threshold']

cv.imwrite('./test_images/gauss_wordbite_hist.png', th3)

for i in range(2):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()