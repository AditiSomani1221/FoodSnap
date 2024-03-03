import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load the image
image = cv2.imread('lays.png')

# Grayscale, Gaussian blur, Adaptive threshold
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 5)

# Perform morphological operations to merge letters together
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

# Find contours and extract ROI
cnts, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
for c in cnts:
    area = cv2.contourArea(c)
    if 1000 < area < 5000:  # Adjust these values based on your images
        x, y, w, h = cv2.boundingRect(c)
        ROI = original[y:y + h, x:x + w]
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)

# Check if a valid ROI was found
if 'ROI' in locals():
    # Perform text extraction
    ROI = cv2.GaussianBlur(ROI, (3, 3), 0)
    data = pytesseract.image_to_string(ROI, lang='eng', config='--psm 6')
    print(data)

    cv2.imshow('ROI', ROI)
    cv2.imshow('close', close)
    cv2.imshow('image', image)
    cv2.waitKey(0)
else:
    print("No valid ROI found.")
