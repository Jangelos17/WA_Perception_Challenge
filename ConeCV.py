import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#Loading the image and resizing it to fit on the screen
img = cv.imread('red.png')
img = cv.resize(img, (700, 700))

#Defining the lower and upper bounds of the red color for thresholding
lower_red = np.array([0, 0, 171])
upper_red = np.array([150, 150, 255])

#Thresholding the image based on the bounds to get a mask
mask = cv.inRange(img, lower_red, upper_red)

#Cleaning up the mast to reduce noise and eliminate small instances of red pixels
kernel = np.ones((5, 5), np.uint8)
mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)

#Finding the contours of the mask to determine the location of each cone
contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#Finding the center of each cone and drawing a circle around it
cluster_centers = []
for contour in contours:
    #Filter out non-touple contours that were returned
    if len(contour) == 2:
        continue
    M = cv.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cluster_centers.append((cx, cy))

        cv.drawContours(img, contour, -1, (0, 255, 0), 3)
        cv.circle(img, (cx, cy), 5, (0, 0, 255), -1)

#Drawing lines between cones that are close to each other.
#used a distance threshold of 100 pixels to differentiate between the two lane lines
if len(cluster_centers) >= 2:
    for i in range(len(cluster_centers)):
        for j in range(i + 1, len(cluster_centers)):
            if abs(cluster_centers[i][0] - cluster_centers[j][0]) < 100:  # Adjust the threshold as needed
                cv.line(img, cluster_centers[i], cluster_centers[j], (0, 0, 255), 3)
while True:
    cv.imshow('mask', mask)
    cv.imshow('image', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
plt.imsave('answer.png', img)
        