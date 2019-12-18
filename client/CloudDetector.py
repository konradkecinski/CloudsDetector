import cv2
import argparse
import numpy as np

class CloudDetector:

    def __init__(self, image, threshold):
        self.img = None
        self.original = image
        self.img_gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        self.ret = None
        self.thresh = None
        self.edged = None
        self.gray_threshold = threshold


    def grayscale_thresholding(self):
        self.ret, self.thresh = cv2.threshold(self.img, self.gray_threshold, 255, cv2.THRESH_BINARY)
        # Find Canny edges
        self.edged = cv2.Canny(self.thresh, 30, 200)
        while True:
            cv2.imshow('Original', self.original)
            cv2.imshow('Cloud Detector', self.thresh)
            cv2.imshow('Canny Edges After Contouring', self.edged)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

        cv2.destroyAllWindows()
        return self.thresh, self.edged
