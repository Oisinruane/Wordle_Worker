import csv
import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

from Play_Script import WordleWorker, load_word_list

WORD_SCORES = load_word_list()


def score(guess, answer):
    """Wordle's colouring: greens first, then yellows only while unmatched copies remain."""
    states = ['absent'] * 5
    remaining = list(answer)
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            states[i] = 'correct'
            remaining[i] = None
    for i, g in enumerate(guess):
        if states[i] != 'correct' and g in remaining:
            states[i] = 'present'
            remaining[remaining.index(g)] = None
    return list(zip(guess, states))


def solver():
    w = WordleWorker.__new__(WordleWorker)
    w.word_scores = WORD_SCORES
    w.reset_knowledge()
    return w


def apply(w, guess, answer):
    w.guessed_words.add(guess)
    w.possible_words.discard(guess)
    w.update_knowledge(guess, score(guess, answer))
    w.filter_word_list()


def simulate(answer):
    """Mirrors play(); returns the guesses made and whether the answer was ever filtered out."""
    w = solver()
    guesses, lost_answer = [], False
    for i in range(6):
        guess = 'crane' if i == 0 else w.choose_next_guess()
        if not guess:
            break
        guesses.append(guess)
        if guess == answer:
            break
        apply(w, guess, answer)
        lost_answer |= answer not in w.possible_words
    return guesses, lost_answer


class DuplicateLetterTests(unittest.TestCase):
    def test_grey_copy_of_green_letter_keeps_letter(self):
        # 2026-10-26: 'yeuky' has a grey Y at 0 and a green Y at 4; Y must not be ruled out
        w = solver()
        for guess in ['crane', 'solei', 'dempt', 'yeuky']:
            apply(w, guess, 'geeky')
        self.assertIn('geeky', w.possible_words)

    def test_grey_copy_caps_letter_count(self):
        # 'level' vs 'hotel': E at 1 is grey and E at 3 green, so the answer has exactly one E
        w = solver()
        w.possible_words = {'hotel', 'ezeel', 'bevel', 'repel'}
        w.update_knowledge('level', score('level', 'hotel'))
        w.filter_word_list()
        self.assertEqual(w.possible_words, {'hotel'})

    def test_grey_copy_of_yellow_letter_keeps_letter(self):
        # 'speed' vs 'abide': first E yellow, second E grey -> exactly one E, not at 2 or 3
        w = solver()
        w.possible_words = {'abide', 'eerie', 'speed', 'ideal'}
        w.update_knowledge('speed', score('speed', 'abide'))
        w.filter_word_list()
        self.assertIn('abide', w.possible_words)
        self.assertNotIn('eerie', w.possible_words)

    def test_fully_absent_letter_is_excluded(self):
        w = solver()
        w.possible_words = {'crane', 'brine', 'stomp'}
        w.update_knowledge('stomp', score('stomp', 'brine'))
        w.filter_word_list()
        self.assertEqual(w.possible_words, {'crane', 'brine'})


class HistoryTests(unittest.TestCase):
    def test_answer_never_filtered_out_for_past_solutions(self):
        with open('results.csv', newline='') as f:
            answers = {r['solution'] for r in csv.DictReader(f) if r['solution']}
        answers |= {'geeky', 'dress', 'river', 'wider', 'gaffe', 'fence', 'joist', 'wager', 'waken'}
        answers &= set(WORD_SCORES)
        broken = [a for a in sorted(answers) if simulate(a)[1]]
        self.assertEqual(broken, [], f"answer wrongly ruled out for: {broken}")


if __name__ == '__main__':
    unittest.main()
