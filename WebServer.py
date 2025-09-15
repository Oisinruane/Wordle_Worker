import csv
from flask import Flask, render_template

app = Flask(__name__)

def parse_results(result_string):
    """Parses a result string like 'c:absent,r:present' into a list of tuples."""
    if not result_string:
        return []
    
    parsed = []
    pairs = result_string.split(',')
    for pair in pairs:
        parts = pair.split(':')
        if len(parts) == 2:
            parsed.append({'letter': parts[0], 'state': parts[1]})
        else:
            # Handle cases where a letter might be missing (e.g., from an error)
            parsed.append({'letter': '?', 'state': 'empty'})
    return parsed

def load_game_data():
    """Loads and processes game data from results.csv."""
    games = []
    try:
        with open('results.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                game = {
                    'timestamp': row.get('timestamp', ''),
                    'solved': row.get('solved', 'no'),
                    'solution': row.get('solution', 'N/A'),
                    'guesses': []
                }
                for i in range(1, 7):
                    guess_word = row.get(f'guess{i}')
                    if guess_word:
                        guess_info = {
                            'word': guess_word,
                            'results': parse_results(row.get(f'result{i}', ''))
                        }
                        game['guesses'].append(guess_info)
                games.append(game)
    except FileNotFoundError:
        print("results.csv not found.")
        return None, []
    except Exception as e:
        print(f"Error reading or parsing CSV: {e}")
        return None, []

    if not games:
        return None, []

    # Sort games by timestamp in descending order (most recent first)
    games.sort(key=lambda g: g.get('timestamp', ''), reverse=True)
    
    today = games[0]
    history = games[1:]
    
    return today, history

def calculate_guess_distribution(games):
    """Calculate the distribution of number of guesses across all games."""
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 'X': 0}  # X for failed games
    
    for game in games:
        if game['solved'] == 'yes':
            num_guesses = len(game['guesses'])
            if 1 <= num_guesses <= 6:
                distribution[num_guesses] += 1
        else:
            distribution['X'] += 1
    
    return distribution

@app.route('/')
def index():
    today, history = load_game_data()
    
    # Calculate guess distribution for all games
    all_games = []
    if today:
        all_games.append(today)
    all_games.extend(history)
    
    guess_distribution = calculate_guess_distribution(all_games)
    
    return render_template('index.html', today=today, history=history, guess_distribution=guess_distribution)

def run_website():
    app.run(debug=False, port=5001)

if __name__ == '__main__':
    run_website()

