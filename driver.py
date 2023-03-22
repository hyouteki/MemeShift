from mean_shift import MeanShift
import numpy
import itertools
import cv2
from termcolor import colored

# image extraction
image = cv2.imread("dump/original.png")
features = image.tolist()
width, height, dim = numpy.shape(features)
features = list(itertools.chain.from_iterable(features))

print(colored(f"Dimension of features :: {width*height} x {dim}", "green")) 

meanShift = MeanShift(10)
meanShift.debug = True
# zee = features[100000:125000]
zee = features
meanShift.initRawData(zee)
meanShift.doTheJob()
out = meanShift.data
# mxx = numpy.shape(out)
# width = 250
# height = 100
px = 3
k: int = 0
img = numpy.zeros((width, height, px))
for i in range(width):
    print(k)
    for j in range(height):
        if (k < width*height):
            img[i][j] = out[k].point
            k += 1
cv2.imwrite("segmented-image.jpg", img)
cv2.imshow("image", img)
cv2.waitKey()
