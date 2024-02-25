def solve_recursive_permutations(map, trie, current_word="", visited=set()):
    """
    Recursively generates character permutations within a map (dictionary), checking for unique values.
    Args:
        map (dict): The map to process.
        trie (Trie): A Trie containing the dictionary.
        current_word (str, optional): The current permutation being built. Defaults to "".
        visited (set, optional): A set of values already used in the current permutation. Defaults to an empty set.
    """

    results = []
    for key, value in map.items():
        if value not in visited:
            new_word = current_word + key
            new_visited = visited.copy()  # Important to copy the set
            new_visited.add(value)

            # if (trie.starts_with(new_word)):
            if trie.search(new_word) and len(new_word) >= 3:
                results.append(new_word)
                print(new_word)

            results += solve_recursive_permutations(map, trie, new_word, new_visited)
    return results