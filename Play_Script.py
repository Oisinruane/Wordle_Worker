import time
import csv
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

VALID_TILE_STATES = {'correct', 'present', 'absent'}

def load_word_list():
    """Load the word list from word_scores.csv file."""
    try:
        word_dict = {}
        with open('word_scores.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                if len(row) >= 2:  # Ensure we have both word and score
                    word = row[0].strip().lower()
                    score = int(row[1].strip())
                    word_dict[word] = score
        print(f"Loaded {len(word_dict)} words from word_scores.csv")
        return word_dict
    except FileNotFoundError:
        print("Error: word_scores.csv file not found. Please ensure it's in the same directory as this script.")
        return {}
    except Exception as e:
        print(f"Error reading word_scores.csv: {e}")
        return {}

class WordleWorker:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.word_scores = load_word_list()
        self.possible_words = set(self.word_scores.keys())
        self.correct_letters = {}  # {index: letter}
        self.present_letters = {}  # {letter: [indices_where_it_is_not]}
        self.absent_letters = set()
        self.guessed_words = set()
        self.game_log = []  # To store guesses and results for the current game
        
        if not self.possible_words:
            print("Warning: No words loaded. The script may not work correctly.")

    def open_wordle(self):
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        self.handle_popups()

    def handle_popups(self):
        # Give the page a moment to settle and for pop-ups to appear.
        time.sleep(2)
        
        try:
            # This logic is based on the successful test in Cookie_Reject.py
            # It handles the cookie consent UI by waiting for the container first.
                
            # Step 1: Wait for the banner container to be visible.
            banner_container_selector = "#fides-banner-container"
            print(f"Waiting for banner container to be visible: '{banner_container_selector}'")
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, banner_container_selector)))
            print("Banner container is visible.")

            # Step 2: Now that the container is visible, wait for the button inside it to be clickable.
            reject_button_selector = '#fides-banner-container button[data-testid="Reject all-btn"]'
            print(f"Waiting for reject button to be clickable: '{reject_button_selector}'")
            reject_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, reject_button_selector)))
            
            print("Cookie button is clickable. Clicking with JavaScript...")
            
            # Step 3: Use JavaScript to perform the click.
            self.driver.execute_script("arguments[0].click();", reject_button)
            
            print("Successfully clicked the 'Reject all' button.")

        except TimeoutException:
            print("No cookie consent pop-up was found or it timed out.")
        except Exception as e:
            print(f"An error occurred while handling the cookie pop-up: {e}")

        try:
            # Close instructions
            print("Waiting for play button...")
            play_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="Play"]')))
            print("Play button found. Clicking with JavaScript...")
            self.driver.execute_script("arguments[0].click();", play_button)
            print("Clicked play button.")
            time.sleep(2)
        except TimeoutException:
            print("Play button not found or timed out.")
        except Exception as e:
            print(f"An error occurred while clicking the play button: {e}")

        # Dismiss any remaining overlay dialogs
        try:
            close_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]')
            self.driver.execute_script("arguments[0].click();", close_btn)
            print("Closed overlay dialog.")
            time.sleep(1)
        except Exception:
            pass

    def make_guess(self, word):
        # Click the game board to ensure it has focus
        try:
            board = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Board-module_board__jeoPS")))
            self.driver.execute_script("arguments[0].click();", board)
            time.sleep(0.5)
        except Exception:
            pass
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(word)
        time.sleep(0.5)
        body.send_keys(Keys.RETURN)
        time.sleep(4)  # Wait for tile flip animations

    def get_results(self, guess_index):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                print(f"Getting results (attempt {attempt + 1})...")
                board = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Board-module_board__jeoPS")))
                rows = board.find_elements(By.CSS_SELECTOR, ".Row-module_row__pwpBq")

                if guess_index >= len(rows):
                    print(f"Error: Row {guess_index} not found, only {len(rows)} rows exist.")
                    return None

                row = rows[guess_index]
                tiles = row.find_elements(By.CSS_SELECTOR, ".Tile-module_tile__UWEHN")

                results = []
                for i, tile in enumerate(tiles):
                    state = tile.get_attribute("data-state")
                    aria_label = tile.get_attribute("aria-label")

                    letter = None
                    if aria_label:
                        parts = aria_label.split(", ")
                        if len(parts) > 1:
                            letter = parts[1].lower()

                    results.append((letter, state))

                if all(state in VALID_TILE_STATES for _, state in results):
                    for i, (letter, state) in enumerate(results):
                        print(f"  Tile {i}: '{letter}' = {state}")
                    return results

                print(f"Tiles not ready yet (states: {[s for _, s in results]}), waiting...")
                time.sleep(2)

            except TimeoutException:
                print("Timed out waiting for game board.")
                return None
            except Exception as e:
                print(f"Error in get_results: {e}")
                return None

        print("Error: Tiles did not resolve after retries.")
        try:
            self.driver.save_screenshot("/tmp/wordle_debug.png")
            print("Debug screenshot saved to /tmp/wordle_debug.png")
            print("Page title:", self.driver.title)
            print("Current URL:", self.driver.current_url)
        except Exception:
            pass
        return None

    def update_knowledge(self, guess, results):
        for i, (letter, state) in enumerate(results):
            if state == 'correct':
                self.correct_letters[i] = letter
                if letter in self.present_letters:
                    del self.present_letters[letter]
            elif state == 'present':
                if letter not in self.present_letters:
                    self.present_letters[letter] = []
                self.present_letters[letter].append(i)
            elif state == 'absent':
                # Only add to absent if not correct or present elsewhere in the word
                if letter not in self.correct_letters.values() and letter not in self.present_letters:
                    self.absent_letters.add(letter)

    def filter_word_list(self):
        new_set = set()
        for word in self.possible_words:
            valid = True
            
            # Check correct letters
            for i, letter in self.correct_letters.items():
                if word[i] != letter:
                    valid = False
                    break
            if not valid: continue

            # Check absent letters
            for letter in self.absent_letters:
                if letter in word:
                    valid = False
                    break
            if not valid: continue

            # Check present letters
            for letter, positions in self.present_letters.items():
                if letter not in word:
                    valid = False
                    break
                for pos in positions:
                    if word[pos] == letter:
                        valid = False
                        break
                if not valid: break
            
            if valid:
                new_set.add(word)
        
        self.possible_words = new_set

    def choose_next_guess(self):
        candidates = self.possible_words - self.guessed_words
        if not candidates:
            return None
        best_word = max(candidates, key=lambda word: self.word_scores[word])
        print(f"Selected '{best_word}' with score {self.word_scores[best_word]} ({len(candidates)} candidates)")
        return best_word

    def save_results_to_csv(self, solved, solution):
        """Saves the results of a single game to results.csv."""
        filepath = 'results.csv'
        
        # Define headers
        headers = ['timestamp', 'solved', 'solution']
        for i in range(1, 7):
            headers.extend([f'guess{i}', f'result{i}'])
            
        # Prepare data row
        row_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'solved': 'yes' if solved else 'no',
            'solution': solution
        }
        
        for i, log_entry in enumerate(self.game_log):
            guess_num = i + 1
            row_data[f'guess{guess_num}'] = log_entry['guess']
            # Format results: e.g., "c:absent,r:present,a:correct,n:absent,e:absent"
            result_str = ",".join([f"{l}:{s}" for l, s in log_entry['results']])
            row_data[f'result{guess_num}'] = result_str
            
        try:
            # Check if file exists to write headers
            file_exists = False
            try:
                with open(filepath, 'r') as f:
                    if f.readline():
                        file_exists = True
            except FileNotFoundError:
                pass

            with open(filepath, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row_data)
            print(f"Game results saved to {filepath}")

        except Exception as e:
            print(f"Error saving results to CSV: {e}")

    def play(self):
        self.open_wordle()
        
        initial_guess = "crane"
        self.game_log = []  # Reset log for a new game
        solved = False
        solution = ""
        
        for i in range(6):
            print(f"--- Guess {i+1} ---")
            
            if i == 0:
                guess = initial_guess
            else:
                self.filter_word_list()
                print(f"Possible words left: {len(self.possible_words)}")
                if len(self.possible_words) < 10:
                    # Show top words with scores for small lists
                    sorted_words = sorted(self.possible_words, key=lambda w: self.word_scores[w], reverse=True)
                    print("Remaining words (with scores):")
                    for word in sorted_words:
                        print(f"  {word}: {self.word_scores[word]}")
                guess = self.choose_next_guess()

            if not guess:
                print("No more possible words found. Something went wrong.")
                break

            print(f"Making guess: {guess}")
            self.make_guess(guess)
            self.guessed_words.add(guess)
            self.possible_words.discard(guess)
            
            results = self.get_results(i)
            if not results:
                print("Could not get results for the guess.")
                break

            print(f"Results: {results}")

            # Log the guess and its results
            self.game_log.append({'guess': guess, 'results': results})

            if all(r[1] == 'correct' for r in results):
                print(f"\nSuccess! The word is {guess.upper()}")
                solved = True
                solution = guess
                break
            
            self.update_knowledge(guess, results)

        else:
            print("\nFailed to solve the Wordle.")
            # If not solved, the solution is unknown. We can leave it blank.
            solution = ""

        self.save_results_to_csv(solved, solution)
        self.driver.quit()

def run_game():
    worker = None
    try:
        worker = WordleWorker()
        worker.play()
    except Exception as e:
        print(f"Game failed with error: {e}")
        if worker and hasattr(worker, 'driver'):
            try:
                worker.driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    run_game()


