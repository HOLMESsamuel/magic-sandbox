import json

# Load the JSON data from the file
with open('cards.json', 'r') as file:
    data = json.load(file)

# Iterate through each card and add the 'number' field
for card in data.get('cards', []):
    card['number'] = 1

# Save the updated JSON data back to the file
with open('cards.json', 'w') as file:
    json.dump(data, file, indent=4)