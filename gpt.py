# Define the healthy and unhealthy ingredient lists
healthy_ingredients = ["Potato", "Vegetable Oil", "Spices & Condiments"]
unhealthy_ingredients = ["Salt", "Sugar"]

# Sample input text
list1_text = """
Ingredients: Potato 45%, Vegetable Oil 26%, Spices & Condiments(Tamarind Powder, Onion Powder, Black Pepper) 14%, Salt 10%, Sugar 5%
"""

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

# Print the scores for each category
print("Healthy Score:", healthy_score)
print("Unhealthy Score:", unhealthy_score)

# Calculate the overall score for list 1
overall_score = healthy_score + unhealthy_score

# Print the overall score
print("Overall Score for List 1:", overall_score)