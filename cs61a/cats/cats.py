"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    selected_paragraphs = [p for p in paragraphs if select(p)]
    if k < len(selected_paragraphs):
        return selected_paragraphs[k]
    else:
        return ""


def about(subject):
    """Return a select function that returns whether
    a paragraph contains one of the words in SUBJECT.

    Arguments:
        subject: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    def select(paragraph):
        words = paragraph.split()
        for word in words:
            cleaned_word = ''.join(filter(str.isalpha, word))
            if cleaned_word.lower() in subject:
                return True
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of SOURCE that was typed.

    Arguments:
        typed: a string that may contain typos
        source: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    typed_words = typed.split()
    source_words = source.split()
    if not typed_words:
        if not source_words:
            return 100.0
        return 0.0
    correct_count = sum(1 for tw, sw in zip(typed_words, source_words) if tw == sw)
    return (correct_count / len(typed_words)) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    words_typed = len(typed)
    words_typed = words_typed / 5
    minutes = elapsed / 60
    return words_typed / minutes
    # END PROBLE
    # M 4


############
# Phase 2A #
############


def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    difference is greater than LIMIT, instead return TYPED_WORD.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    closest_word = typed_word
    closest_diff = limit
    flag = 1
    for word in word_list:
        if word == typed_word:
            return typed_word
        diff = diff_function(typed_word, word, limit)
        if flag == 1:
            if diff <= closest_diff:
                closest_diff = diff
                closest_word = word
                flag = 0
        if diff < closest_diff:
            closest_diff = diff
            closest_word = word
    return closest_word
    # END PROBLEM 5


def feline_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    """
    # Base case: If one of the strings is empty, return the absolute difference in lengths
    if typed == '' or source == '':
        return abs(len(typed) - len(source))

    # Base case: If limit is reached, return a value greater than the limit
    if limit < 0:
        return limit + 1

    # Base case: If both characters are the same, proceed to the next character
    if typed[0] == source[0]:
        return feline_fixes(typed[1:], source[1:], limit)

    # If characters are different and limit allows further operations, recursively explore options
    diff_substitute = 1 + feline_fixes(typed[1:], source[1:], limit - 1)
    
    # Return the minimum difference
    min_diff = diff_substitute
    
    # If the minimum difference exceeds the limit, return a value greater than the limit
    if min_diff > limit:
        return limit + 1
    else:
        return min_diff



    # END PROBLEM 6
    

############
# Phase 2B #
############


def minimum_mewtations(typed, source, limit):
    """A diff function that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.
    
    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits
        
    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    if limit < 0:
        return float('inf')
    if not typed:
        return len(source)
    if not source:
        return len(typed)
    
    if typed[0] == source[0]:
        return minimum_mewtations(typed[1:], source[1:], limit)
    else:
        add = 1 + minimum_mewtations(typed, source[1:], limit - 1)
        remove = 1 + minimum_mewtations(typed[1:], source, limit - 1)
        substitute = 1 + minimum_mewtations(typed[1:], source[1:], limit - 1)
        return min(add, remove, substitute)



def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    if limit < 0:
        return float('inf')
    if not typed:
        return len(source)
    if not source:
        return len(typed)
    
    if typed[0] == source[0]:
        return final_diff(typed[1:], source[1:], limit)
    else:
        add = 1 + final_diff(typed, source[1:], limit - 1)
        remove = 1 + final_diff(typed[1:], source, limit - 1)
        substitute = 1 + final_diff(typed[1:], source[1:], limit - 1)
        return min(add, remove, substitute)
    
FINAL_DIFF_LIMIT = 6 # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, source, user_id, upload):
    """
    Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    Examples:
        >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
        >>> # The above function displays progress in the format ID: __, Progress: __
        >>> print_progress({'id': 1, 'progress': 0.6})
        ID: 1 Progress: 0.6
        >>> typed = ['how', 'are', 'you']
        >>> source = ['how', 'are', 'you', 'doing', 'today']
        >>> report_progress(typed, source, 2, print_progress)
        ID: 2 Progress: 0.6
        0.6
        >>> report_progress(['how', 'aree'], source, 3, print_progress)
        ID: 3 Progress: 0.2
        0.2
    """
    correct_words = 0
    
    for typed_word, source_word in zip(typed, source):
        if typed_word != source_word:
            break
        correct_words += 1
    
    progress = correct_words / len(source)
    
    # Upload progress using the provided upload function
    upload({'id': user_id, 'progress': progress})
    
    return progress



def time_per_word(words, timestamps_per_player):
    """Given timing data, return a match data abstraction, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        timestamps_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_all_words(match)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_all_times(match)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    times = []
    for player in timestamps_per_player:
        player_times = []
        for i in range(len(words)):
            player_times.append(player[i + 1] - player[i])
        times.append(player_times)
    return match(words, times)


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match data abstraction as returned by time_per_word.

    Examples:
        >>> p0 = [5, 1, 3]
        >>> p1 = [4, 1, 6]
        >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
        [['have', 'fun'], ['Just']]
        >>> p0  # input lists should not be mutated
        [5, 1, 3]
        >>> p1
        [4, 1, 6]
    """
    words = get_all_words(match)
    times = get_all_times(match)
    
    num_players = len(times)
    num_words = len(words)
    
    # Initialize a list to store the fastest words for each player
    fastest_for_players = [[] for _ in range(num_players)]
    
    for word_index in range(num_words):
        # Get the times for the current word from all players
        word_times = [times[player_num][word_index] for player_num in range(num_players)]
        
        # Find the minimum time for the current word
        min_time = min(word_times)
        
        # Find the player(s) with the minimum time and the lowest index
        fastest_players = [player_num for player_num, time_taken in enumerate(word_times) if time_taken == min_time]
        fastest_player = min(fastest_players)
        
        # Add the current word to the list of fastest words for the corresponding player
        fastest_for_players[fastest_player].append(words[word_index])
    
    return fastest_for_players





def match(words, times):
    """A data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(get_all_words(match)), "word_index out of range of words"
    return get_all_words(match)[word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(get_all_words(match)), "word_index out of range of words"
    assert player_num < len(get_all_times(match)), "player_num out of range of players"
    return get_all_times(match)[player_num][word_index]

def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]

def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match data abstraction and returns a string representation of it"""
    return f"match({get_all_words(match)}, {get_all_times(match)})"

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, source))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)