import cv2
import numpy as np

vec_file = "samples.vec"
samples = np.load(vec_file)

for i in range(5):  # Display 5 random samples
    sample = samples[i].reshape(100, 100)
    cv2.imshow("Sample", sample)
    cv2.waitKey(0)
