import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from datetime import date
from pathlib import Path

def show_grayscale_image(image_name):
    plt.imshow(image_name, 'gray', vmin=0, vmax=255)
    plt.title(f'{image_name}'), plt.xticks([]), plt.yticks([])
    plt.show()

# place today's date in the format dd-MON-yyyy, i.e., 16-Sep-2024 or 8-Sep-2024
def today_date_rfc():
    day = str(date.today().day)
    month = date.today().month
    year = str(date.today().year)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    rfc_date =  day + '-' + months[month-1] + '-' + year
    return rfc_date

dl_folder = Path('') # folder where your images are stored
if not dl_folder.exists():
    print("Directory does not exist. Exiting...")
    exit()

# get list of files
files = list(os.walk(dl_folder))[0][2]

# date format matches rfc spec to work with the email downloader program
todays_date = today_date_rfc()

dl_today = [image for image in files if todays_date in image] #iterable of filenames to feed to ocr below
if not dl_today:
    print(f"No images found in {dl_folder}")
    print("Exiting...")
    exit()

# feed file names into imread
for image in dl_today:

    img = cv.imread(f'{dl_folder}/{image}', cv.IMREAD_GRAYSCALE)
    if img is None:
        print("File couldn't be read. Verify the path to the image is correct...")
        exit()

    # Perform thresholding on image and dilate image with a 3x3 kernel to remove unnecessary image artifacts
    ret,thresh1 = cv.threshold(img,90,255,cv.THRESH_BINARY)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    dilation = cv.dilate(thresh1, kernel, iterations = 1)
    contours, hierarchy = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    # Creating a copy of image
    img_copy = img.copy()

    file = open(f'trans_{image}', "w+")
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        
        # Drawing a rectangle on copied image
        rect = cv.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Cropping the text block for giving input to OCR
        cropped = img_copy[y:y + h, x:x + w]
        
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        file = open(f'trans_{image}', "a")
        
        # both '\x0c' and '\f' are formfeed character that need removed from file
        if text == '\x0c':
            continue

        file.write(text)     
        file.write("\n")
        file.close()
