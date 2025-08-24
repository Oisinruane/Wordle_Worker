import csv
from collections import Counter

def calculate_word_scores(input_file: str, output_file: str):
    """
    Calculates a score for each word in a list based on the frequency of its letters.

    The score is determined by summing the total counts of each unique letter
    found in the entire word list. This helps prioritize words that contain
    the most common letters, which is useful for games like Wordle.

    Args:
        input_file (str): The path to the text file containing one word per line.
        output_file (str): The path to the CSV file where the results will be saved.
    """
    try:
        # Step 1: Read all words from the input file
        with open(input_file, 'r') as f:
            words = [word.strip().upper() for word in f if word.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    # Step 2: Calculate the frequency of each letter across all words
    all_letters = "".join(words)
    letter_counts = Counter(all_letters)
    print(f"Calculated letter frequencies based on {len(words)} words.")
    
    # Step 3: Score each word
    word_scores = []
    for word in words:
        # Use a set to count each letter only once per word (e.g., 'APPLE'
        # scores based on 'A', 'P', 'L', 'E', not 'P' twice)
        unique_letters = set(word)
        score = sum(letter_counts.get(letter, 0) for letter in unique_letters)
        word_scores.append((word, score))
    
    # Sort the words by score in descending order for easy viewing
    word_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Step 4: Write the results to a CSV file
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(['word', 'score'])
            # Write the scored words
            writer.writerows(word_scores)
        print(f"Successfully wrote {len(word_scores)} words and their scores to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred while writing the CSV file: {e}")

# --- Example Usage ---
# If you have a file named 'wordlist.txt', this will create 'word_scores.csv'
if __name__ == "__main__":
    calculate_word_scores('word_list.txt', 'word_scores.csv')
