from flask import Flask, request, render_template
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

app = Flask(__name__)

# Path of working folder on Disk
def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite("removed_noise.png", img)

    # Apply threshold to get an image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after applying OpenCV to do some ...
    cv2.imwrite(img_path, img)

    # Recognize text with Tesseract for Python
    result = pytesseract.image_to_string(Image.open(img_path))

    return result

# Create a function to process the image and return a result
def process_image(image_path):
    data = get_string(image_path)

    sections = data.strip().split('\n\n')

    # Create dictionaries to store ingredients for each product
    ingredients = {
        "storia": []
    }

    # Process and store the ingredients for each product
    for section in sections:
        lines = section.split('\n')
        product_name = lines[0].strip(':').lower()
        product_ingredients = [line.strip() for line in lines[1:]]
        ingredients[product_name] = product_ingredients

    # Define the healthy and unhealthy ingredient lists
    healthy_ingredients = ["Potato", "Spices & Condiments", "Mango", "Water", "Rice", "Vitamin C"]
    unhealthy_ingredients = ["Salt", "Sugar", "Vegetable Oil", "Stabilizers"]

    # Sample input text
    list1_text = data

    # Extract the text following "Ingredients:" and remove leading/trailing whitespace
    ingredient_text = list1_text.split("Ingredients:")[1].strip()

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

    # Calculate the overall score
    overall_score = healthy_score + unhealthy_score

    return overall_score

# Define the route for the web application
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            if image:
                # Save the uploaded image to a file
                image_path = "uploaded_image.png"  # Define the path for the uploaded image
                image.save(image_path)

                # Process the uploaded image and get the result
                result = process_image(image_path)

                # Determine healthiness category based on the result
                if result < 0:
                    healthiness = "Non-eatable"
                    bg_color = "red"
                elif result >= 0 and result < 25:
                    healthiness = "Unhealthy"
                    bg_color = "red"
                elif result >= 25 and result < 50:
                    healthiness = "Okay"
                    bg_color = "yellow"
                elif result >= 50 and result < 75:
                    healthiness = "Eatable"
                    bg_color = "lightgreen"
                else:
                    healthiness = "Healthy"
                    bg_color = "green"

                return render_template('result.html', result=result, bg_color=bg_color, healthiness=healthiness)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
