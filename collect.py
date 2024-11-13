import json
import csv
import pandas as pd
from datetime import datetime

# Read JSON file
with open('final_filtered_qa.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare data list
rows = []
for qa in data['qa_pairs']:
    if qa.get('text_input') and qa.get('output'):  # Ensure input and output exist and are valid
        row = {
            'input': qa['text_input'].strip(),
            'output': qa['output'].strip(),
            'input_word_count': len(qa['text_input'].split()),
            'output_word_count': len(qa['output'].split())
        }
        rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Save as CSV
output_filename = f'training_data_{datetime.now().strftime("%Y%m%d")}.csv'
df.to_csv(output_filename, index=False, encoding='utf-8')

# Print statistics
print(f"Conversion complete! Saved as: {output_filename}")
print(f"Total rows: {len(df)}")
print("\nData preview:")
print(df.head())
print("\nBasic statistics:")
print(df.describe())