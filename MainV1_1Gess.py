# To run this script, you need to install selenium and download a webdriver.
# 1. Install selenium:
#    pip install selenium
#
# 2. Download a webdriver for your browser. For Chrome, download chromedriver:
#    https://chromedriver.chromium.org/downloads
#    Make sure the chromedriver version matches your Chrome browser version.
#    Place the chromedriver executable in the same directory as this script, or in a directory in your system's PATH.

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

WORD_LIST = [
    'cigar', 'rebut', 'sissy', 'humph', 'awake', 'blush', 'focal', 'evade', 'naval', 'serve', 'heath', 'dwarf',
    'model', 'karma', 'stink', 'grade', 'quiet', 'bench', 'abate', 'feign', 'major', 'death', 'fresh', 'crust',
    'stool', 'colon', 'abase', 'marry', 'react', 'batty', 'pride', 'floss', 'helix', 'croak', 'staff', 'paper',
    'unfed', 'whelp', 'trawl', 'outdo', 'adobe', 'crazy', 'sower', 'repay', 'digit', 'crate', 'cluck', 'spike',
    'mimic', 'pound', 'maxim', 'linen', 'unmet', 'flesh', 'booby', 'forth', 'first', 'stand', 'belly', 'ivory',
    'seedy', 'print', 'yearn', 'drain', 'bribe', 'stout', 'panel', 'crass', 'flume', 'offal', 'agree', 'error',
    'swirl', 'argue', 'bleed', 'delta', 'flick', 'totem', 'wooer', 'front', 'shrub', 'parry', 'biome', 'lapel',
    'start', 'greet', 'goner', 'golem', 'lusty', 'loopy', 'round', 'audit', 'lying', 'gamma', 'labor', 'islet',
    'civic', 'forge', 'corny', 'moult', 'basic', 'salad', 'agate', 'spicy', 'spray', 'essay', 'fjord', 'spend',
    'kebab', 'guild', 'aback', 'motor', 'alone', 'hatch', 'hyper', 'thumb', 'dowry', 'ought', 'belch', 'dutch',
    'pilot', 'tweed', 'comet', 'jaunt', 'enema', 'steed', 'abyss', 'growl', 'fling', 'dozen', 'boozy', 'erode',
    'world', 'gouge', 'click', 'briar', 'great', 'altar', 'pulpy', 'blurt', 'coast', 'duchy', 'groin', 'fixer',
    'group', 'rogue', 'badly', 'smart', 'pithy', 'gaudy', 'chill', 'heron', 'vodka', 'finer', 'surer', 'radio',
    'rouge', 'perch', 'retch', 'wrote', 'clock', 'tilde', 'store', 'prove', 'bring', 'solve', 'cheat', 'grime',
    'exult', 'usher', 'epoch', 'triad', 'break', 'rhino', 'viral', 'conic', 'masse', 'sonic', 'vital', 'trace',
    'using', 'peach', 'champ', 'baton', 'brake', 'pluck', 'craze', 'gripe', 'weary', 'picky', 'acute', 'ferry',
    'aside', 'tapir', 'troll', 'unify', 'rebus', 'boost', 'truss', 'siege', 'tiger', 'banal', 'slump', 'crank',
    'gorge', 'query', 'drink', 'favor', 'abbey', 'tangy', 'panic', 'solar', 'shire', 'proxy', 'point', 'robot',
    'prick', 'wince', 'crimp', 'knoll', 'sugar', 'whack', 'mount', 'perky', 'could', 'wrung', 'light', 'those',
    'moist', 'shard', 'pleat', 'aloft', 'skill', 'elder', 'frame', 'humor', 'pause', 'ulcer', 'ultra', 'robin',
    'cynic', 'agora', 'aroma', 'caulk', 'shake', 'pupal', 'dodge', 'swill', 'tacit', 'other', 'thorn', 'trove',
    'bloke', 'vivid', 'spill', 'chant', 'choke', 'rupee', 'nasty', 'mourn', 'ahead', 'brine', 'cloth', 'hoard',
    'sweet', 'month', 'lapse', 'watch', 'today', 'focus', 'smelt', 'tease', 'cater', 'movie', 'lynch', 'saute',
    'allow', 'renew', 'their', 'slosh', 'purge', 'chest', 'depot', 'epoxy', 'nymph', 'found', 'shall', 'harry',
    'stove', 'lowly', 'snout', 'trope', 'fewer', 'shawl', 'natal', 'fibre', 'comma', 'foray', 'scare', 'stair',
    'black', 'squad', 'royal', 'chunk', 'mince', 'slave', 'shame', 'cheek', 'ample', 'flair', 'foyer', 'cargo',
    'oxide', 'plant', 'olive', 'inert', 'askew', 'heist', 'shown', 'zesty', 'hasty', 'trash', 'fella', 'larva',
    'forgo', 'story', 'hairy', 'train', 'homer', 'badge', 'midst', 'canny', 'fetus', 'butch', 'farce', 'slung',
    'tipsy', 'metal', 'yield', 'delve', 'being', 'scour', 'glass', 'gamer', 'scrap', 'money', 'hinge', 'album',
    'vouch', 'asset', 'tiara', 'crept', 'bayou', 'atoll', 'manor', 'creak', 'showy', 'phase', 'froth', 'depth',
    'gloom', 'flood', 'trait', 'girth', 'piety', 'payer', 'goose', 'float', 'donor', 'atone', 'primo', 'apron',
    'blown', 'cacao', 'loser', 'input', 'gloat', 'awful', 'brink', 'smite', 'beady', 'rusty', 'retro', 'droll',
    'gawky', 'hutch', 'pinto', 'gaily', 'egret', 'lilac', 'sever', 'field', 'fluff', 'hydro', 'flack', 'agape',
    'wench', 'voice', 'stead', 'stalk', 'berth', 'madam', 'night', 'bland', 'liver', 'wedge', 'augur', 'roomy',
    'wacky', 'flock', 'angry', 'bobby', 'trite', 'aphid', 'tryst', 'midge', 'power', 'elope', 'cinch', 'motto',
    'stomp', 'upset', 'bluff', 'cramp', 'quart', 'coyly', 'youth', 'rhyme', 'buggy', 'alien', 'smear', 'unfit',
    'patty', 'cling', 'glean', 'label', 'hunky', 'khaki', 'poker', 'gruel', 'twice', 'twang', 'shrug', 'treat',
    'unlit', 'waste', 'merit', 'woven', 'octal', 'needy', 'clown', 'widow', 'irony', 'ruder', 'gauze', 'chief',
    'onset', 'prize', 'fungi', 'charm', 'gully', 'inter', 'whoop', 'taunt', 'leery', 'class', 'theme', 'lofty',
    'tibia', 'booze', 'alpha', 'thyme', 'eclat', 'doubt', 'parer', 'chute', 'stick', 'trice', 'alike', 'sooth',
    'recap', 'saint', 'liege', 'glory', 'grate', 'admit', 'brisk', 'soggy', 'usurp', 'scald', 'scorn', 'leave',
    'twine', 'sting', 'bough', 'marsh', 'sloth', 'dandy', 'vigor', 'howdy', 'enjoy', 'valid', 'ionic', 'equal',
    'unset', 'floor', 'catch', 'spade', 'stein', 'exist', 'quirk', 'denim', 'grove', 'spiel', 'mummy', 'fault',
    'foggy', 'flout', 'carry', 'sneak', 'libel', 'waltz', 'aptly', 'piney', 'inept', 'aloud', 'photo', 'dream',
    'stale', 'vomit', 'ombre', 'fanny', 'unite', 'snarl', 'baker', 'there', 'glyph', 'pooch', 'hippy', 'spell',
    'folly', 'louse', 'gulch', 'vault', 'godly', 'threw', 'fleet', 'grave', 'inane', 'shock', 'crave', 'spite',
    'valve', 'skimp', 'claim', 'rainy', 'musty', 'pique', 'daddy', 'quasi', 'arise', 'aging', 'valet', 'opium',
    'avert', 'stuck', 'recut', 'mulch', 'genre', 'plume', 'rifle', 'ranch', 'tarot', 'crane'
]

class WordleWorker:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)  # Increased wait time
        self.possible_words = WORD_LIST.copy()
        self.correct_letters = {}  # {index: letter}
        self.present_letters = {}  # {letter: [indices_where_it_is_not]}
        self.absent_letters = set()

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
        except TimeoutException:
            print("Play button not found or timed out.")
        except Exception as e:
            print(f"An error occurred while clicking the play button: {e}")

    def make_guess(self, word):
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(word)
        body.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for animations

    def get_results(self, guess_index):
        try:
            # Use an explicit wait to ensure the game-app element is loaded
            print("Attempting to get results...")
            print("Waiting for game-app element to be present...")
            game_app = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "game-app")))
            print("Found game-app element. Accessing its shadow root to find rows...")
            
            game_rows = game_app.shadow_root.find_elements(By.CSS_SELECTOR, "game-row")
            print(f"Found {len(game_rows)} game rows.")
            
            if guess_index >= len(game_rows):
                print(f"Error: Trying to access row {guess_index}, but only {len(game_rows)} rows exist.")
                return None

            print(f"Accessing row {guess_index} for the current guess...")
            row = game_rows[guess_index]
            print("Accessing shadow root of the row to find tiles...")
            tiles = row.shadow_root.find_elements(By.CSS_SELECTOR, "game-tile")
            print(f"Found {len(tiles)} tiles in row {guess_index}.")
            
            results = []
            for i, tile in enumerate(tiles):
                print(f"  - Processing tile {i}:")
                state = tile.get_attribute("evaluation")
                letter = tile.get_attribute("letter")
                print(f"    > Letter: '{letter}', State: '{state}'")
                results.append((letter, state))
            
            print("Successfully processed all tiles and got results.")
            return results
        except TimeoutException:
            print("Error: Timed out waiting for 'game-app' element. The game may not have loaded correctly.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred in get_results: {e}")
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
        new_list = []
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
                new_list.append(word)
        
        self.possible_words = new_list

    def choose_next_guess(self):
        if not self.possible_words:
            return None
        # A simple strategy: just pick the first possible word.
        # A better strategy would be to pick a word that reveals more information.
        return self.possible_words[0]

    def play(self):
        self.open_wordle()
        
        initial_guess = "crane"
        
        for i in range(6):
            print(f"--- Guess {i+1} ---")
            
            if i == 0:
                guess = initial_guess
            else:
                self.filter_word_list()
                print(f"Possible words left: {len(self.possible_words)}")
                if len(self.possible_words) < 10:
                    print(self.possible_words)
                guess = self.choose_next_guess()

            if not guess:
                print("No more possible words found. Something went wrong.")
                break

            print(f"Making guess: {guess}")
            self.make_guess(guess)
            
            results = self.get_results(i)
            if not results:
                print("Could not get results for the guess.")
                break

            print(f"Results: {results}")

            if all(r[1] == 'correct' for r in results):
                print(f"\nSuccess! The word is {guess.upper()}")
                break
            
            self.update_knowledge(guess, results)

        else:
            print("\nFailed to solve the Wordle.")

        time.sleep(10) # Keep browser open to see the result
        self.driver.quit()

if __name__ == "__main__":
    worker = WordleWorker()
    worker.play()
