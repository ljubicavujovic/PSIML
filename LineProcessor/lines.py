import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
inputPathFile = "lines_processor/case-0.png"
# inputPathFile = raw_input()

image = cv.imread(inputPathFile)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# gray = cv.morphologyEx(gray, cv.MORPH_TOPHAT, (11, 11))
# gray = cv.dilate(gray, (15, 15))
#
# plt.imshow(gray)
# plt.show()

ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
plt.imshow(thresh)
plt.show()
print thresh.shape

pts = np.transpose(np.nonzero(thresh))
print pts.shape
# pts = np.ndarray(shape=(thresh.shape[0] * thresh.shape[1], 2), dtype=np.uint8)
# cv.findNonZero(thresh, pts)
box = cv.minAreaRect(pts)
print box

# if 1 < np.abs(box[2]) <= 30:
#     print 'usao u if'
#     print box[2]
#     box = ((box[0][0], box[0][1]), (box[1][1], box[1][0]), box[2] + 90)

print box
if box[2] < 0:
    box[2] += 90
# rotated = None
if 1 < np.abs(box[2]) <= 30:
    M = cv.getRotationMatrix2D(box[0], -box[2], 0.6)
    rotated = cv.warpAffine(thresh, M, thresh.shape)
    rotated = cv.erode(rotated, kernel=(11, 11))
else:
    rotated = thresh

plt.imshow(rotated)
plt.show()

lines_number = 0
flag = False
for line in rotated:
    # print(sum(line))
    if sum(line) > ret:
        if flag is False:
            flag = True
            lines_number += 1
    else:
        flag = False

print lines_number
