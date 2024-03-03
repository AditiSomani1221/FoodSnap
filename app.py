from flask import Flask, request, render_template
import cv2
import numpy as np
import pytesseract
from PIL import Image
import pandas as pd

app = Flask(__name__)

# Function to read ingredients from Excel files
def read_ingredients_from_excel(file_name):
    return pd.read_excel(file_name, header=None)[0].tolist()

# Define your image processing code in a separate function
def process_uploaded_image(image_path):
    # Read healthy and unhealthy ingredients from Excel
    healthy_ingredients = read_ingredients_from_excel(r'C:\Users\Aditi-PC\Desktop\7th sem project\OCR - 1 (3)\OCR - 1 (2)\OCR - 1\OCR\healthy.xlsx')
    unhealthy_ingredients = read_ingredients_from_excel(r'C:\Users\Aditi-PC\Desktop\7th sem project\OCR - 1 (3)\OCR - 1 (2)\OCR - 1\OCR\unhealthy.xlsx')

    def get_string(img_path):
        # Your existing image processing code...
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        cv2.imwrite("removed_noise.png", img)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        cv2.imwrite(img_path, img)
        result = pytesseract.image_to_string(Image.open(img_path))
        return result

    data = get_string(image_path)

    # Extract the text following "Ingredients:" and remove leading/trailing whitespace
    ingredient_text = data.split("Ingredients:")[1].strip()

    # Split the ingredient text by commas to get individual ingredients
    ingredient_lines = ingredient_text.split(',')

    # Initialize scores
    healthy_score = 0
    unhealthy_score = 0

    # Categorize and score ingredients based on percentages
    for ingredient_line in ingredient_lines:
        parts = ingredient_line.strip().split()
        if len(parts) >= 2:
            ingredient = ' '.join(parts[:-1])
            percentage = parts[-1].strip('%,')
            
            if ingredient in healthy_ingredients:
                healthy_score += float(percentage)
            elif ingredient in unhealthy_ingredients:
                unhealthy_score -= float(percentage)

    # Calculate the overall score for list 1
    overall_score = healthy_score + unhealthy_score

    return overall_score

# Define the route for the web application
@app.route('/', methods=['GET'])
def landing():
    # Render the landing page where the user enters their age
    return render_template('landing.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            if image:
                image_path = "uploaded_image.png"
                image.save(image_path)
                result = process_uploaded_image(image_path)
                return render_template('result.html', result=result)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
