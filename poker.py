#poker.py
#
# 5-card draw poker
# Royal Flush    250
# Straight Flush  50
# 4 of a Kind     25
# Full House       9
# Flush            6
# Straight         4
# 3 of a Kind      3
# Two Pair         2
# Jacks or Better  1

from random import shuffle
import os
import sys
from itertools import groupby

def initialize():
    deck = []
    for suit in ['H','C','D','S']:
        for rank in ['2','3','4','5','6','7','8','9','0','J','Q','K','A']:
            deck.append(rank + suit)
    return deck

def deal(deck):
    hand = []
    for card in range(5):
        hand.append(deck.pop(0))
    return hand

def show(hand):
    for card in hand:
        print colorize(card),
    print "\r"

def discard(hand):
    discard_hand = hand
    print "Enter up to 5 cards to discard."
    discarding = True
    discard_count = 0
    while discarding and discard_count < 5:
        input_err = True
        while input_err:
            discard = raw_input("Discard [none when finished]: ")
            if discard.strip() == '':
                input_err = False
                discarding = False
            elif discard.upper() in hand:
                input_err = False
                discard_hand.remove(discard.upper())
                discard_count += 1
                show(discard_hand)
            else:
                sound_bell()
                print "Select a card from [",
                for card in hand:
                    print colorize(card),
                print "]"
    hand = discard_hand
    return hand

def draw(hand, deck, num_hands):
    results = []
    for i in range(num_hands):
        results.append([list(hand),0])
    working_deck = list(deck)
    for i in range(len(results)):
        for card in range(5 - len(results[i][0])):
            results[i][0].append(working_deck.pop(0))
        working_deck = list(deck)
        shuffle(working_deck)
    return results

def show_all(results, num_hands, running_total):
    hands_per_row = 5
    hands_count = 0
    scores = []
    payout = 0
    for hand in results:
        for card in hand[0]:
            print colorize(card),
        score, pay = pays(hand[0])
        hand[1] = pay
        scores.append(score)
        if pay == 0:
            payout -= 1
        else:
            payout += pay + 1
        print hand[1],
        hands_count += 1
        print " "*(4-len(str(hand[1]))),
        if hands_count == hands_per_row:
            hands_count = 0
            print "\r"
    if hands_count != hands_per_row:
        print "\r"
    scores.sort()
    grouped_scores = [(k, sum(1 for i in g)) for k,g in groupby(scores)]
    print grouped_scores
    print payout
    running_total += payout
    print running_total
    return running_total

def pays(hand):
    suits = []
    ranks = []
    for card in hand:
        suits.append(card[1])
        ranks.append(card[0])
    suits.sort()
    ranks.sort()
    grouped_suits = [(k, sum(1 for i in g)) for k,g in groupby(suits)]
    grouped_ranks = [(k, sum(1 for i in g)) for k,g in groupby(ranks)]
    for (suit,count) in grouped_suits:
        if count == 5:
            # Royal Flush
            if ranks == ['0','A','J','K','Q']:
                score = "royal flush"
                pay = 250
            # Straight Flush
            elif ranks in [['2','3','4','5','A'],['2','3','4','5','6'],['3','4','5','6','7'],\
              ['4','5','6','7','8'],['5','6','7','8','9'],['0','6','7','8','9'],['0','7','8','9','J'],\
              ['0','8','9','J','Q'],['0','9','J','K','Q']]:
                score = "straight flush"
                pay = 50
            # Flush
            else:
                score = "flush"
                pay = 6
        else:
            if len(grouped_ranks) == 2:
                for (rank,count) in grouped_ranks:
                    # 4 of a Kind
                    if count == 4:
                        score = "four of a kind"
                        pay = 25
                        break
                    # Full House
                    else:
                        score = "full house"
                        pay = 9
            elif len(grouped_ranks) == 3:
                for (rank,count) in grouped_ranks:
                    # 3 of a Kind
                    if count == 3:
                        score = "three of a kind"
                        pay = 3
                    # Two Pair
                    if count == 2:
                        score = "two pair"
                        pay = 2
            elif len(grouped_ranks) == 4:
                for (rank,count) in grouped_ranks:
                    # Jacks or Better
                    if count == 2 and rank in ['J','Q','K','A']:
                        score = "jacks or better"
                        pay = 1
                        break
                    else:
                        score = "loser"
                        pay  = 0
            elif len(grouped_ranks) == 5:
                # Straight
                if ranks in [['2','3','4','5','A'],['2','3','4','5','6'],['3','4','5','6','7'],\
                  ['4','5','6','7','8'],['5','6','7','8','9'],['0','6','7','8','9'],['0','7','8','9','J'],\
                  ['0','8','9','J','Q'],['0','9','J','K','Q'],['0','A','J','K','Q']]:
                    score = "straight"
                    pay = 4
                else:
                    score = "loser"
                    pay = 0
    return score, pay

def colorize(card):
    if card[1] == 'C':
        cmd = u"\u001b[34m" + card + u"\u001b[0m"
    elif card[1] == 'H':
        cmd = u"\u001b[31m" + card + u"\u001b[0m"
    elif card[1] == 'S':
        cmd = u"\u001b[32m" + card + u"\u001b[0m"
    elif card[1] == 'D':
        cmd = u"\u001b[38;5;208m" + card + u"\u001b[0m"
    return cmd

def sound_bell():
    sys.stdout.write('\a')
    sys.stdout.flush()

#MAIN PROGRAM
play_again = True
running_total = 0

while play_again:

    #game loop
    deck = initialize()
    os.system('clear')
    try:
        num_hands
    except NameError:
        num_hands = 100
    input_err = True
    while input_err:
        input = raw_input("Enter number of hands [%s]: " % str(num_hands))
        if input.strip() == '':
            input_err = False
            input = num_hands
        else:
            try:
                if int(input) > 0:
                    input_err = False
                    num_hands = int(input)
                else:
                    sound_bell()
            except ValueError:
                sound_bell()
    shuffle(deck)
    hand = deal(deck)
    show(hand)
    hand = discard(hand)
    results = draw(hand, deck, num_hands)
    running_total = show_all(results, num_hands, running_total)

    #end of game
    sound_bell()
    print "Game Over."
    print
    again_input_err = True
    while again_input_err:
        again_yn = raw_input("Press Enter to play again or enter Q to quit: ")
        if again_yn.strip() == "":
            again_input_err = False
            print
        elif again_yn.upper() == "Q":
            again_input_err = False
            play_again = False
            print
            print "Thank you for playing!"
            print
        else:
            sound_bell()
            print
