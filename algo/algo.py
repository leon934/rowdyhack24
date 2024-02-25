def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file)

def generate_combinations(grid):
    combinations = set()

    # Add individual letters
    for row in grid:
        combinations.update(row)

    # Add horizontal combinations
    for row in grid:
        combinations.update([''.join(row[i:]) for i in range(len(row))])

    # Add vertical combinations
    for i in range(len(grid[0])):
        combinations.update([''.join(row[i] for row in grid)])

    return combinations

def find_valid_words(grid, dictionary):
    valid_words = []
    combinations = generate_combinations(grid)

    for word in combinations:
        if word in dictionary:
            valid_words.append(word)

    return valid_words

def main():
    dictionary = load_dictionary('valid_guess.txt')
    
    # Example Word Bites grid
    word_bites_grid = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f'],
        ['g', 'h', 'i']
    ]

    valid_words = find_valid_words(word_bites_grid, dictionary)

    print("Valid Words:")
    print(valid_words)

if __name__ == "__main__":
    main()
