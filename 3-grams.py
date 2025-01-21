import json
import re
import csv
from collections import defaultdict, Counter


def extract_3grams(text):
    """Generate and return 3-grams from the input text."""
    normalized_text = re.sub(r'[^\w\s]', '', text.lower())
    words = normalized_text.split()
    return [' '.join(words[i:i + 3]) for i in range(max(0, len(words) - 2))]


def process_file(file_path, output_csv):
    author_3grams = defaultdict(Counter)

    # Open and read the JSON lines file
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)

            if data['type'] == 'PushEvent' and data.get('payload', {}).get('commits'):
                commits = data['payload']['commits']
                for commit in commits:
                    author_name = commit['author']['name']
                    message = commit.get('message', '')

                    # Extract and count 3-grams
                    for trigram in extract_3grams(message):
                        author_3grams[author_name][trigram] += 1

    # Write the output to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['author', 'first 3-gram', 'second 3-gram', 'third 3-gram', 'fourth 3-gram', 'fifth 3-gram'])

        for author, trigrams in author_3grams.items():
            # Sort trigrams based on frequency and select top 5
            top_trigrams = [trigram for trigram, count in trigrams.most_common(5)]
            # Ensure exactly 5 entries in top_trigrams
            top_trigrams.extend([''] * (5 - len(top_trigrams)))
            writer.writerow([author] + top_trigrams)


# Define paths to the input JSON and output CSV files
file_path = '10K.github.json'
output_csv = 'output.csv'

# Process the file and produce the CSV
if __name__ == "__main__":
    process_file(file_path, output_csv)
