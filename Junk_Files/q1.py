
from itertools import cycle


def bid(hand, player_no, phase_no, deck_top, reshuffled=False, player_data=None, suppress_player_data=True):
	"""
		bid() takes a series of parameters defining a game state of 'Oh Hell'
		and returns a bid from given game state

		parameters:
			(1) hand, a tuple of cards (each in the form of a string,
				as described above) that you have been dealt for the current
				phase, or in the case of Phase 1 or 19,
				representing the cards of the other three players

			(2) player_no, an integer between 0 and 3 inclusive indicating
				player order for the current phase,
				where players play in increasing order of player_no value,
				and the player with a player_no of 0 has the lead for the
				first trick

			(3) phase_no, an integer between 1 and 19 inclusive,
				indicating the phase number of the current hand

			(4) deck_top, the top card of the deck,
				used to determine trumps for the current phase

			(5) optional argument reshuffled, a Boolean indicating whether
				the deck was reshuffled as part of the deal for the current
				hand

			(6) optional argument player_data, a user-defined data structure
				containing information about the cur- rent game state

			(7) optionalBooleanargumentsuppress_player_data,
				whereTrueindicatesthatthefunctionshould return only the bid
				(and not player_data) and False indicates that player_data
				may be returned. 

		return values:
			either a bid (integer of value 0-10)
			or a tuple (bid, player_data)

	"""
	if phase_no in [1, 10, 19]:
		# cannot see own cards so logically 0 is safest
		bid = 0
	elif phase_no%4 == 0:
		bid = int(len(hand)/4)
	else:
		bid = len(hand)//4

	return bid if suppress_player_data else (bid, player_data)


def is_valid_play(play, curr_trick, hand):
	""" is_valid_play() checks a move by a player and determines if it
		conforms to 'Oh Hells' rules

		parameters:
			play, a 2 char string conforming to our card model

			curr_trick, a tuple containing cards previously played in round

			hand, a tuple containing all remain cards in hand

		returns a Boolean, T if valid, F if invalid
	"""
	if len(curr_trick) == 0:  # Player is lead
		return True
	else:
		lead_suit = curr_trick[0][1]
		play_suit = play[1]

		if play_suit == lead_suit:
			return True
		else:
			# Check remaining cards in hand
			for card in hand:
				suit = card[1]
				if suit == lead_suit:
					return False
			# no card in hand matches lead_suit
			return True
def score_phase(bids, tricks, deck_top, player_data=None,
	suppress_player_data=True):
	"""
	score_phase() will return the respective scores for each player given a
	series of rounds within a phase of 'Oh Hell'

	parameters:
		bids, 4 tuple of each players bid

		tricks, a tuple containing nested 4 tuples for each round in a phase

		deck_top, string representing the top card of the deck for phase

		player_data, optional arguament for improved decision logic

		suppress_player_data, optional Bool.
			determines if player_data returned
	return:
		a 4 tuple, each value an integer score for each player 0 -> 3
	"""
	score = [0, 0, 0, 0]

	# prepare itertools.cycle() object
	seating_order = cycle([0, 1, 2, 3])
	next(seating_order)  

	# Determine the winner of each trick and increment score
	for trick in tricks:
		_play, winning_index = det_winner(trick, deck_top[1], trick[0][1],
			index_return=True)

		# using seating order determine which player played won the trick
		for _ in range(winning_index):
			winning_player = next(seating_order)

		score[winning_player] += 1

	# Check the results of players bids and increment score acordingly
	for player in range(4):
		if score[player] == bids[player]:
			score[player] += 10

	score = tuple(score)  # Dont want to mess with that PEP8s

	return score if suppress_player_data else (score, player_data)
	
def det_winner(cards, trump_suit, lead_suit, index_return=False):
	trumps, leads = [], []
	winner = ''
	for i in range(len(cards)):
		if cards[i][1] == trump_suit:
			trumps.append(cards[i])
		elif cards[i][1] == lead_suit:
			leads.append(cards[i])

	if len(trumps) == 0:
		leads = sort_cards(leads)
		winner = leads.pop()
	else:
		trumps = sort_cards(trumps)
		winner = trumps.pop()

	return winner, cards.index(winner) if index_return else winner

def play(curr_trick, hand, prev_tricks, player_no, deck_top, phase_bids,
        player_data=None, suppress_player_data=True, is_valid=is_valid_play,
        score=score_phase):

	leader = player_no != 0
	trump_suit = deck_top[1]
	lead_suit = prev_tricks[0][1] if leader else None
	cur_winner = prev_tricks[_determine_winner(prev_tricks, deck_top)]

	playable_cards = det_playable(hand, lead_suit)
	winning_cards, losing_cards = analyse_hand(playable_cards)

	met_bid = Bool()

	if len(playable_cards) == 1:
		return playable_cards.pop()

	elif leader and met_bid:
		return losing_cards.pop(0)

	elif leader:
		return winning_cards.pop()

	elif met_bid:
		return losing_cards.pop()

	elif len(winning_cards) == 0:
		return losing_cards.pop(0)

	elif player_no == 3:
		return winning_cards.pop(0)

	else:
		return winning_cards.pop()




	# """
	# play() determines the best card to play in a trick for given conditions of a game of 'Oh Hell'

	# that takes as arguments:
	# (1) curr_trick a tuple containing the cards played in the current incomplete trick

	# (2) hand, the tuple of cards that you currently hold in your hand

	# (3) prev_tricks, which takes the form of a tuple of completed tricks for the current phase (each of which is a 4-tuple)

	# (4) player_no, an integer between 0 and 3 inclusive indicating player order for the current phase

	# (5) deck_top, the top card of the deck, used to determine trumps for the current phase

	# (6) phase_bids,a tuple containing the bids of the players for the current phase, in order of player_no (startingfromplayer_no = 0)

	# (7) optional argument player_data

	# (8) optional argument suppress_player_data, a Boolean where True indicates that the function should return only the play (and not player_data)

	# (9) optional argument is_valid, a function 

	# (10) optional argument score, a function

	# return:
	# a single string conforming to the 'Oh Hell' representation of a playing card or 2-tuple containing the the above string and player_data as defined by parameter 7.
	# """


def sort_cards(cards):
	suits = ['C', 'S', 'D', 'H']
	value_seq = "234567890JQKA"
	sorted_cards = []

	def _value(card):
		return value_seq.find(card[0])
	
	# Sort cards by suit then sort each suit by ascending value
	suits_2d = [[card for card in cards if card[1] == suit] for suit in suits]
	for i in range(4):
		temp_list = []
		for card in suits_2d[i]:
			temp_list.append(_value(card))
		suits_2d[i] = sorted(temp_list)

	# Sort each card in list
	num_cards_to_sort = len(cards)
	while num_cards_to_sort > 0:

		# Find suit with lowest value card
		suit_with_lowest_card = None
		i = 0

		# Find initial lowest card
		while i < 4:
			if len(suits_2d[i]) == 0:  # suit is empty
				i += 1
				continue
			else:
				suit_with_lowest_card = suits_2d[i]  
				break

		# Compare initial lowest to lowest in each suit
		while i < 4:
			try: 
				if suit_with_lowest_card[0] > suits_2d[i][0]:
					suit_with_lowest_card = suits_2d[i]
					i += 1
				else:
					i += 1
			except IndexError:
				i += 1

		# Pop the next lowest card and add to a list
		for i in range(4):
			if suit_with_lowest_card is suits_2d[i]:
				low_card = ""
				low_card += value_seq[suit_with_lowest_card[0]] + suits[i]
				sorted_cards.append(low_card)
				suit_with_lowest_card.pop(0)

		num_cards_to_sort -= 1

	return sorted_cards


def det_playable(cur_trick, hand):
	suits = 'CSDH'
	# Sort cards by suit
	hand = [[card for card in hand if card[1] == suit] for suit in suits]

	if len(cur_trick) == 0:
		return hand
	else:
		lead_suit = cur_trick[0][1]
		lead_suit_in_hand = hand[suits.find(lead_suit)]

		return hand if len(lead_suit_in_hand) == 0 else lead_suit_in_hand

def suit_index(suit):
	return 'CSDH'.find(suit)


def analyse_plays(cur_winner, sorted_playable_cards, trump_suit, lead_suit):
	winning_plays, losing_plays = [], []

	# Organise cards by card significance
	leads = sorted_playable_cards[suit_index(lead_suit)]
	trumps = sorted_playable_cards[suit_index(trump_suit)]
	del sorted_playable_cards[suit_index(lead_suit)]
	del sorted_playable_cards[suit_index(trump_suit)]
	losing_plays = [card for suit in sorted_playable_cards for card in suit]


	plays_in_cur_win_suit = trumps if cur_winner[1] == trump_suit else leads

	# compare cards against cur_winner and allocate win/ lose
	for card in plays_in_cur_win_suit:
		comparison = det_winner([cur_winner, card], trump_suit, lead_suit)
		if comparison != cur_winner:
			winning_plays.append(card)
		else:
			losing_plays.append(card)

	# add unallocated cards to respective win/lose lists
	if plays_in_cur_win_suit is not trumps:
		winning_plays += trumps
	else:
		losing_plays += leads


	return winning_plays, losing_plays
