import random
import multiprocessing
import math
import time

simulations = 100000
num_decks = 6
shuffle_perc = 75

def simulate(queue, batch_size):

    deck = []

    def new_deck():
        # Creating deck
        std_deck = [
            # 2  3  4  5  6  7  8  9  10  J   Q   K   A
              2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
              2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
              2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
              2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
        ]

        std_deck = std_deck * num_decks
        random.shuffle(std_deck)

        return std_deck[:]

    def play_hand():

        dealer_cards = []
        player_cards = []

        # Deal starting cards
        player_cards.append(deck.pop())
        dealer_cards.append(deck.pop())
        player_cards.append(deck.pop())
        dealer_cards.append(deck.pop())

        while sum(player_cards) < 17:
            player_cards.append(deck.pop())
            if sum(player_cards) > 21:
                for i, card in enumerate(player_cards):
                    if card == 11:
                        player_cards[i] = 1

        while sum(dealer_cards) < 17:
            dealer_cards.append(deck.pop())
            if sum(dealer_cards) > 21:
                for i, card in enumerate(dealer_cards):
                    if card == 11:
                        dealer_cards[i] = 1

        d_sum = sum(dealer_cards)
        p_sum = sum(player_cards)

        if p_sum > 21:
            return -1
        if d_sum > 21:
            return 1
        if d_sum < p_sum:
            return 1
        if d_sum == p_sum:
            return 0
        if d_sum > p_sum:
            return -1

    deck = new_deck()

    win = 0
    draw = 0
    loss = 0

    for i in range(batch_size):

        # Shuffle condition
        if (float(len(deck))/(52*num_decks))*100 < shuffle_perc:
            deck = new_deck()

        result = play_hand()

        if result == 1:
            win += 1
        if result == 0:
            draw += 1
        if result == -1:
            loss += 1

    # Adding into queue
    queue.put([win, draw, loss])

start_time = time.time()

# simulate
cpus = multiprocessing.cpu_count()
batch_size = int(math.ceil(simulations / float(cpus)))

queue = multiprocessing.Queue()

# create n processes
processes = []

for i in range(0, cpus):
	process = multiprocessing.Process(target=simulate, args=(queue, batch_size))
	processes.append(process)
	process.start()

# wait for everything to finish
for proc in processes:
	proc.join()

finish_time = time.time() - start_time

# get totals
win = 0
draw = 0
loss = 0

for i in range(0, cpus):
    results = queue.get()
    win += results[0]
    draw += results[1]
    loss += results[2]

print ('  cores used: %d' % cpus)
print ('  total simulations: %d' % simulations)
print ('  simulations/s: %d' % (float(simulations) / finish_time))
print ('  execution time: %.2fs' % finish_time)
print ('  win percentage: %.2f%%'  % ((win / float(simulations)) * 100))
print ('  draw percentage: %.2f%%' % ((draw / float(simulations)) * 100))
print ('  lose percentage: %.2f%%' % ((loss / float(simulations)) * 100))
