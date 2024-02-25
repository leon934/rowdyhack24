def get_h_map(horizontals, verticals, singles):
    """
    Returns map for use for horizontal permutations. Keys are letters or strings (based on if the tiles are horizontal/vertical tiles) and tile ids

    Args:
        horizontals (arr): The horizontal tiles.
        verticals (arr): The vertical tiles.
        singles (arr): The single tiles.
    
    """

    h_map = dict()
    counter = 0

    # add individual vertical letters with unique pair value
    # example output: { "g" : 1, "h" : 1, "i" : 2, "j" : 2 }
    for i, s in enumerate(verticals):
        for c in s:
            h_map[c] = i
            counter += 1

    # add horizontal strings and singles with unique value
    # example output: { "ab" : 3, "dc" : 4, "k" : 5, "l" : 6 }
    for s in horizontals + singles:
        h_map[s] = counter
        counter += 1

    return h_map

def get_v_map(horizontals, verticals, singles):
    """
    Returns map for use for vertical permutations. Keys are letters or strings (based on if the tiles are horizontal/vertical tiles) and tile ids

    Args:
        horizontals (arr): The horizontal tiles.
        verticals (arr): The vertical tiles.
        singles (arr): The single tiles.
    
    """

    v_map = dict()
    counter = 0

    # add individual horizonal letters with unique pair value
    # example output: { "g" : 1, "h" : 1, "i" : 2, "j" : 2 }
    for i, s in enumerate(horizontals):
        for c in s:
            v_map[c] = i
            counter += 1

    # add vertical strings and singles with unique value
    # example output: { "ab" : 3, "dc" : 4, "k" : 5, "l" : 6 }
    for s in verticals + singles:
        v_map[s] = counter
        counter += 1

    return v_map