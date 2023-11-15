#!/usr/bin/env python

import os
import cv2
import pytesseract
import imutils


def ocr_core(filename):
    img = cv2.imread(filename)
    img = imutils.resize(img, width=6400)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    img = cv2.GaussianBlur(img, (3, 3), 0)

    text = pytesseract.image_to_string(img, config='--psm 12')

    return text


def split_filter_and_print(text):
    strings = text.split()
    for string in strings:
        if len(string) >= 4:
            print(string)


def main():
    source_path = 'Dataset2'
    src_files = os.listdir(source_path)
    for file_name in src_files:
        full_file_name = os.path.join(source_path, file_name)
        print(full_file_name)
        text = ocr_core(full_file_name)
        split_filter_and_print(text)


if __name__ == "__main__":
    main()
