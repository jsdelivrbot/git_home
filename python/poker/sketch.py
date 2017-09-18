#!/usr/bin/python3

"""
    This program plays poker.
    The first one plays out the hand wins.
    N cards are hidden from the players.
    Legal moves are:
        1) Single card
        2) Double
        3) 5 or more consecutive singles
        4) 3 or more consecutive doubles
        5) Triple with either a single or a double
        6) 2 or more consecutive triples
        7) Bomb (4 same value cards)
        8) Jet (4 same value cards with any two cards)
"""

import random

# Initialize the whole deck
deck = [14, 15]
for i in range(1,14):
    deck.extend([i]*4)

# Randomly hide N cards
N = 8
random.seed(42)
random.shuffle(deck)
hide_out = deck[:N]

# Then assign the cards to players
n_players = 2
player = deck[N:(N+(54-N)//n_players)]

def find_legal_move(move):
    """If opponent plays move."""
    pass

def guess_counter_move(move):
    """Guess what the opponent will play."""
    pass

def play_game(p, N):
    """Start a game with p player and N hidden cards."""
    deck = [14, 15]
    for i in range(1, 14):
        deck.extend([i]*4)

    random.seed(42)
    random.shuffle(deck)
    hide_out = deck[:N]

    player_decks = list()
    for i in range(N, len(deck)):
        if len(player_decks) < p:
            player_decks.append([deck[i]])
        else:
            player_decks[(i-N)%p].append(deck[i])

    return player_decks, hide_out

if __name__ == '__main__':

    # print(deck)
    # print(player, "Total: ", len(player))
    player_decks, hidden_deck = play_game(3, 2)
    print(player_decks)
    print(hidden_deck)
