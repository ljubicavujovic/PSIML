import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

inputTextFile = "morse_code/case-8.in"
text = []
with open(inputTextFile, "r") as f:
    for line in f:
        text.append(float(line[:-1]))
zero = False
count = 0
number = {}
prev = 1
#
# for i, t in enumerate(text):
#     if t < 0.5:
#         print i
#         if zero is False:
#             if count > 0:
#                 if count in number:
#                     number[count] += 1
#                 else:
#                     number[count] = 1
#             zero = True
#             count = 1
#         else:
#             count += 1
#     else:
#         zero = False
#     prev = t
# print number
# size = min(number)

w = sig.wiener(text, 13)
plt.plot(text)
plt.show()

plt.plot(w)

plt.show()

