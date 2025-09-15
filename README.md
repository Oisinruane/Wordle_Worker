# Wordle Worker

Plays wordle for me so everyone things I know all the words really good

This script automates playing the popular game Wordle by using Selenium to interact with the New York Times Wordle webpage. It uses a **word-scoring system** and **deductive reasoning** to find the correct five-letter word in as few guesses as possible.

-----

## 🚀 Getting Started

### Prerequisites

Before you can run the bot, you need to install a few dependencies:

1.  **Python:** Make sure you have Python installed on your system.
2.  **Selenium:** Install the Selenium library via `pip`:
    ```bash
    pip install selenium
    ```
3.  **A WebDriver:** The script needs a WebDriver to control your browser. For Chrome, download **ChromeDriver** from the official site.
      - **Important:** The version of the ChromeDriver must match your Chrome browser's version. You can check your Chrome version by going to `chrome://version/` in your browser's address bar.
      - Place the `chromedriver` executable file in the same directory as this script, or in a directory that's included in your system's PATH.

### Installation

1.  Save the provided Python script as a `.py` file (e.g., `wordle_solver.py`).
2.  Make sure you have a `word_scores.csv` file in the same directory. This file should contain a list of five-letter words and their corresponding scores, which the bot uses to prioritize guesses. The first line should be a header (e.g., `word,score`).

### How to Run

Simply execute the script from your terminal:

```bash
python wordle_solver.py
```

-----

## ⚙️ How It Works

The bot follows a systematic approach to solving the Wordle puzzle:

  - **Initial Guess:** It always starts with the word **"crane"** as its first guess. This is a common strategy in Wordle as it contains highly frequent letters.
  - **Analyzing Results:** After each guess, the bot analyzes the color-coded tiles (`correct`, `present`, or `absent`) to update its knowledge of the puzzle.
  - **Filtering Words:** Based on the results, it **filters its internal word list**, removing any words that don't match the new information (e.g., words with absent letters or words where a "present" letter is in the wrong spot).
  - **Choosing the Next Guess:** From the remaining possible words, it selects the word with the **highest score** from the `word_scores.csv` file. This scoring system helps it choose words that are more likely to contain the correct letters.
  - **Logging:** The bot logs each game's guesses and results to a `results.csv` file, providing a record of its performance.

-----

## 📝 Word Scores CSV Format

The `word_scores.csv` file is crucial for the bot's performance. It should be a simple CSV with two columns: `word` and `score`.

| word | score |
|:---:|:---:|
| crane | 100 |
| slate | 95 |
| trace | 92 |

You can create this file yourself or find a pre-compiled list online. The higher the score, the more "optimal" a word is considered for guessing.
