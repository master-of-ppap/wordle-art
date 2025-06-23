from enum import Enum

with open('words.txt', 'r') as file:
    words = file.read().splitlines()

class Color(Enum):
    Gray = "⬛"
    Yellow = "🟨"
    Green = "🟩"

    def __str__(self):
        return self.value

wordle_word = "oddly"

possible_characters = "⬛🟩🟨"

ideal_image = """
⬛⬛🟩🟩🟩
⬛🟨🟨🟨⬛
🟨⬛🟨⬛🟨
⬛🟨🟩🟨⬛
⬛🟩🟩🟩⬛
⬛🟨🟨🟨⬛
"""

ideal_image = """
🟨🟨⬛🟨⬛
🟨🟨🟨⬛⬛
⬛🟨🟨🟨⬛
🟨🟨🟨⬛⬛
🟨🟨⬛🟨🟨
🟨⬛⬛🟨⬛
"""


# ideal_image = """
# 🟨⬛🟨⬛🟨
# 🟨🟨🟨🟨🟨
# 🟨🟩🟩🟩🟨
# ⬛🟨🟩🟨⬛
# 🟩🟩⬛🟩🟩
# 🟩🟨🟨🟨🟩
# """  # Green

# ideal_image = """
# ⬛⬛⬛⬛⬛
# ⬛🟩🟩🟩⬛
# ⬛🟨🟨🟩🟩
# ⬛🟨🟨🟩🟩
# ⬛🟩🟩🟩🟩
# ⬛🟩⬛🟩⬛
# """

def parse_ideal_image(image_str):
    print(f"Parsing ideal image: {image_str}")
    symbol_to_color = {
        '⬛': Color.Gray,
        '🟨': Color.Yellow,
        '🟩': Color.Green
    }
    lines = [line for line in image_str.strip().split('\n') if line]
    return [
        [symbol_to_color[char] for char in line]
        for line in lines
    ]


def test_generate_color_array():
    test_cases = [
        # Wordle word, guessed word, expected color array
        ("prank", "brank", [Color.Gray, Color.Green, Color.Green, Color.Green, Color.Green]),
        ("prank", "prank", [Color.Green, Color.Green, Color.Green, Color.Green, Color.Green]),
        ("prank", "rpakn", [Color.Yellow, Color.Yellow, Color.Green, Color.Yellow, Color.Yellow]),
        ("apple", "axplp", [Color.Green, Color.Gray, Color.Green, Color.Green, Color.Yellow]),
        ("apple", "applp", [Color.Green, Color.Green, Color.Green, Color.Green, Color.Gray]),
        ("apple", "pxplp", [Color.Yellow, Color.Gray, Color.Green, Color.Green, Color.Gray]),
        ("apple", "paplp", [Color.Yellow, Color.Yellow, Color.Green, Color.Green, Color.Gray]),
        ("thrum", "mudim", [Color.Gray, Color.Yellow, Color.Gray, Color.Gray, Color.Green]),
        
    ]

    
    for wordle_answer, word, expected in test_cases:
        result = generate_color_array(wordle_answer, word)
        assert result == expected, f"Failed for {wordle_answer} with {word}: expected {expected}, got {result}"
    print("All tests passed!")


def generate_color_array(wordle_answer: str, word: str) -> list[Color]:
    # If the word is "apple" and i guess "applp"

    color_array: list[Color] = []
    non_green_letter_count: dict[str, int] = {}
    non_green_final_letter_count: dict[str, int] = {}
    green_count: dict[str, int] = {}
    
    for char in wordle_answer + word:
        if char not in non_green_letter_count:
            non_green_letter_count[char] = 0
        if char not in green_count:
            green_count[char] = 0
        if char not in non_green_final_letter_count:
            non_green_final_letter_count[char] = 0

    for i, char in enumerate(wordle_answer):
        if char == word[i]:
            green_count[char] += 1
        else:
            non_green_final_letter_count[char] += 1
    
    # print("Wordle answer:", wordle_answer)
    # print("Word:", word)
    # print("Green count:", green_count)
    # print("Final letter count:", non_green_final_letter_count)

    for i, char in enumerate(word):

        if char == wordle_answer[i]:
            color_array.append(Color.Green)
            continue
        non_green_letter_count[char] += 1
        if char in wordle_answer:
            # print(f"Attempting to add yellow for" f" {char} at index {i}, with letter count {non_green_letter_count[char]} and final letter count {non_green_final_letter_count[char]}")
            # print("Letter count:", non_green_letter_count)
            
            if non_green_letter_count[char] <= non_green_final_letter_count[char]:
                color_array.append(Color.Yellow)
                continue
        color_array.append(Color.Gray)

    return color_array

def does_word_have_no_gray(wordle_answer: str, word: str) -> bool:
    color_array = generate_color_array(wordle_answer, word)
    
    for color in color_array:
        if color == Color.Gray:
            return False
    return True

def amount_of_yellow(wordle_answer: str, word: str) -> int:
    color_array = generate_color_array(wordle_answer, word)
    # Value: 1 for each yellow, 0.5 for each green
    return sum(1 if color == Color.Yellow else 0.5 if color == Color.Green else 0 for color in color_array)

def amount_of_green(wordle_answer: str, word: str) -> int:
    color_array = generate_color_array(wordle_answer, word)
    return sum(1 if color == Color.Green else 0.5 if color == Color.Yellow else 0 for color in color_array)

def does_word_match_ideal_image(wordle_answer: str, word: str, ideal_image: list[Color]) -> bool:

    color_array = generate_color_array(wordle_answer, word)
    
    for i in range(len(ideal_image)):
        if color_array[i] != ideal_image[i]:
            return False
    return True

def get_words_that_match_ideal_image(wordle_answer, words, ideal_image):
    return [word for word in words if does_word_match_ideal_image(wordle_answer, word, ideal_image)]


def get_words_that_have_no_gray(wordle_answer, words):
    return [word for word in words if does_word_have_no_gray(wordle_answer, word)]

def get_and_sort_by_amount_of_yellow(wordle_answer, words):
    return sorted(words, key=lambda word: amount_of_yellow(wordle_answer, word), reverse=True) 

def get_and_sort_by_amount_of_green(wordle_answer, words):
    # Ignore first one because it is the wordle word itself
    return sorted(words, key=lambda word: amount_of_green(wordle_answer, word), reverse=True)

# test_generate_color_array()

print(f"Parsing ideal image: {ideal_image}")
ideal_image_array = parse_ideal_image(ideal_image)
for ideal_image in ideal_image_array:
    matches = get_words_that_match_ideal_image(wordle_word, words, ideal_image)
    print(f"Matches for ideal image {len(matches)}: {matches[:3]}")

yellows = get_and_sort_by_amount_of_yellow(wordle_word, words)
print(f"Words sorted by amount of yellow: {len(yellows)} words: {yellows[:6]}")

greens = get_and_sort_by_amount_of_green(wordle_word, words)
print(f"Words sorted by amount of green: {len(greens)} words: {greens[1:7]}")


# matches = get_words_that_have_no_gray(wordle_word, words)
# print(f"Matches for ideal image with no gray {len(matches)}: {matches}")