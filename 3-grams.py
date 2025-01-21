import json
import re
import csv


def extract_3grams(text):
    """Generate and return 3-grams from the input text."""
    # Normalize text: convert to lowercase and remove punctuations
    normalized_text = re.sub(r'[^\w\s]', '', text.lower())
    words = normalized_text.split()
    # Generate 3-grams from the list of words
    return [' '.join(words[i:i+3]) for i in range(min(len(words) - 2, 5))]


def process_file(file_path, output_csv):
    """Process the JSON lines file and generate a CSV."""
    results = []

    # Open and read the JSON lines file
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)

            if data['type'] == 'PushEvent' and data.get('payload', {}).get('commits'):

                commits = data['payload']['commits']
                for commit in commits:
                    author_name = commit['author']['name']
                    message = commit.get('message', '')

                    unique_trigrams = [trigram for trigram in extract_3grams(message) if trigram]
                    # if len(unique_trigrams) > 5:
                    #     unique_trigrams = unique_trigrams[:5]  # Limit to top 5 if more than 5

                    # Append new record with the author and their trigrams if any
                    if unique_trigrams:
                        results.append({
                            'author': author_name,
                            'trigrams': unique_trigrams
                        })

    # Write the output to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['author', 'first 3-gram', 'second 3-gram', 'third 3-gram', 'fourth 3-gram', 'fifth 3-gram'])

        for result in results:
            # Extend the list of trigrams to ensure it has exactly 5 elements
            trigrams = result['trigrams'] + [''] * (5 - len(result['trigrams']))
            writer.writerow([result['author']] + trigrams)


# Define paths to the input JSON and output CSV files
file_path = '10K.github.json'
output_csv = 'output.csv'

# Process the file and produce the CSV
process_file(file_path, output_csv)
