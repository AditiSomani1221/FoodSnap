import re

def calculate_healthiness_score(ingredient_data, ingredient_weights):
    # Use regular expression to extract ingredient information
    ingredient_matches = re.findall(r'(\w+(?: \w+)* \d+%)', ingredient_data)
    
    # Initialize the healthiness score
    healthiness_score = 0
    
    for match in ingredient_matches:
        # Split the match into name and percentage
        name, percentage = match.split()
        name = name.strip()
        percentage = float(percentage[:-1])  # Convert percentage to a float
        
        # Check if the ingredient is in the provided weights
        if name in ingredient_weights:
            # Calculate the contribution to the healthiness score
            contribution = percentage * ingredient_weights[name]
            healthiness_score += contribution
        
    return healthiness_score

# Define the ingredient weights
ingredient_weights = {
    "Water": 1, 
    "Mango": 2, 
    "Sugar": -1, 
    "Fructose": -1.5, 
    "Whitener": -2, 
    "Vegetable Oil": -2
}

# Sample ingredient data
ingredient_data = "Water 30%, Mango 16%, Sugar 11%, Whitener 9%, Vegetable Oil 7%"

# Calculate the healthiness score
healthiness_score = calculate_healthiness_score(ingredient_data, ingredient_weights)

# Print the result
print("Healthiness Score:", healthiness_score)
