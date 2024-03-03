import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

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

    #  Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(img_path, img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path))

    # Remove template file
    #os.remove(temp)

    return result


print ('--- Start recognize text from image ---')



def makestring(filename):
    orgtext = get_string(filename)

    # Split the text by newlines and extract lines with percentage values
    ingredient_lines = [line.strip() for line in orgtext.split('\n') if '%' in line]

    return "\n".join(ingredient_lines)




filename = "parleg.png"


data = makestring(filename) 

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

data = get_string(filename)
print (get_string(filename))

print ("------ Done -------")

# Define the healthy and unhealthy ingredient lists
healthy_ingredients = ["Mango", "Water", "Wheat", "Vitamin C"]
unhealthy_ingredients = ["Sugar", "Antioxidant", "Fructose", "Stabilizers"]

# Sample input for list 1
list1_text = data
count = 0
# Parse the ingredients from the text
list1_lines = list1_text.split('\n')

# Create a dictionary to map ingredients to their ranks
ingredient_ranking = {}

# Assign ranks to ingredients in list 1
for i, ingredient in enumerate(list1_lines):
    ingredient = ingredient.strip()
    if ingredient != "":
        ingredient_ranking[ingredient] = i + 1

# Initialize scores
healthy_score = 0
unhealthy_score = 0

# Categorize and score ingredients in list 1
for ingredient in ingredient_ranking:
    rank = ingredient_ranking[ingredient]
    
    for healthy_ingredient in healthy_ingredients:
        if re.search(r'\b' + re.escape(healthy_ingredient) + r'\b', ingredient, re.IGNORECASE):
            healthy_score += rank
            count += 1
    
    for unhealthy_ingredient in unhealthy_ingredients:
        if re.search(r'\b' + re.escape(unhealthy_ingredient) + r'\b', ingredient, re.IGNORECASE):
            unhealthy_score += rank
            count += 1
# Print the scores for each category
print("Healthy Score:", healthy_score)
print("Unhealthy Score:", unhealthy_score)

# Calculate the overall score for list 1
overall_score = (healthy_score - unhealthy_score)*10/count

# Print the overall score
print("Overall Score for List 1:", overall_score)