import random
import math
import time

def new_deck():

    # Creating deck
    deck = [
        # 2  3  4  5  6  7  8  9  10  J   Q   K   A
          2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
          2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
          2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
          2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
    ]

    decks = deck*4
    random.shuffle(decks);
    return decks

def deal(deck, player_cards, dealer_cards):

    player_cards.append(deck.pop())
    dealer_cards.append(deck.pop())
    player_cards.append(deck.pop())
    dealer_cards.append(deck.pop())

def check_player_lose(player_cards):
    if sum(player_cards) > 21:
        return True
    else:
        return False

def setup():
    print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")
    print("Welcome to Blackjack, enter deposit amount:\n")

    while 1:
        x = input()
        if (x.isdigit() == False):
            print("Invalid deposit - deposit amount must be > 0")
        else:
            return int(x)

def get_wager(player_money):

    print("Enter Wager:\n")
    while 1:
        x = input()
        if x.isdigit() == False or int(x) > player_money:
            print("Invalid wager - wager amount must be > 0, < balance")
        else:
            return int(x)

def draw_card(player_cards, deck):
    card = deck.pop()
    player_cards.append(card)
    print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")
    print("Your Cards: {} ({})".format(player_cards, sum(player_cards)))
    if sum(player_cards) == 21:
        print("Blackjack!")
    print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")

def play(player_money):
    print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")
    print("You currently have ${}, good luck!\n".format(player_money))
    wager = get_wager(player_money)
    double = 1;

    deck = new_deck()
    player_cards = []
    dealer_cards = []

    deal(deck, player_cards, dealer_cards)
    print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")
    print("Your Cards: {}".format(player_cards))
    print("Dealer Cards: {}".format(dealer_cards))
    print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")

    turn = 1
    # Player move
    while sum(player_cards) < 21:
        if (turn == 1):
            print("Hit, Stand, or Double?\n")
        else:
            print("Hit or Stand?\n")

        x = input()
        if x == "hit":
            draw_card(player_cards, deck)
            if (check_player_lose(player_cards)):
                time.sleep(1.5)
                print("Bad luck, dealer got you this time!")
                return -1*wager

        elif x == "stand":
            break

        elif x == "split":
            pass

        elif x == "double":
            if wager > player_money/2:
                print("\nNot enough money to do so!")
                print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")
                turn -= 1;
            elif (turn == 1):
                double = 2;
                draw_card(player_cards, deck)
                time.sleep(1.5)
                if (check_player_lose(player_cards)):
                    time.sleep(1.5)
                    print("Bad luck, dealer got you this time!")
                    return -1*wager*double
                break
            else:
                print("Invalid, input must be: 'hit', 'stand'")

        else:
            print("Invalid, input must be: 'hit', 'stand', 'split', 'double'")

        turn += 1;

    # Deal for dealer
    while (sum(dealer_cards) < 17):
        dealer_cards.append(deck.pop())

    print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")
    print("Dealer Cards: {} ({})".format(dealer_cards, sum(dealer_cards)))
    print("\n=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=\n")
    player_sum = sum(player_cards)
    dealer_sum = sum(dealer_cards)

    time.sleep(1.5)
    if dealer_sum > 21:
        print("Dealer busted!")
        print("Congratulations, you won: ${}".format(wager*double))
        return wager*double
    else:
        if player_sum > dealer_sum:
            print("Congratulations, you won: ${}".format(wager*double))
            return wager*double
        elif player_sum < dealer_sum:
            print("Unlucky, dealer got you this time!")
            return -1*wager*double
        else:
            print("Push!")
            return 0

player_money = setup()
while (player_money > 0):
    time.sleep(1)
    player_money += play(player_money)

print("\nYou are now broke :(\n")
