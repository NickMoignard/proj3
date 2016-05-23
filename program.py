# ============================================================================
# NICHOLAS MOIGNARD ~ 762877
# COMP10001
# Assignment 3
# ============================================================================

def main():
	

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

	# check if play is in hand
	if play not in hand:
		return False

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
	

def play(curr_trick, hand, prev_tricks, player_no, deck_top, phase_bids,
		player_data=None, suppress_player_data=True, is_valid=is_valid_play,
		score=score_phase):

	""" play() determines the best card to play in a trick for given
		conditions of a game of 'Oh Hell' that takes parameters:

	(1) curr_trick a tuple containing the cards played in the current
		incomplete trick

	(2) hand, the tuple of cards that you currently hold in your hand

	(3) prev_tricks, which takes the form of a tuple of completed tricks
		for the current phase (each of which is a 4-tuple)

	(4) player_no, an integer between 0 and 3 inclusive indicating player
		order for the current phase

	(5) deck_top, the top card of the deck, used to determine trumps for the
		current phase

	(6) phase_bids,a tuple containing the bids of the players for the current
		phase, in order of player_no (startingfromplayer_no = 0)

	(7) optional argument player_data

	(8) optional argument suppress_player_data, a Boolean where True indicates
		that the function should return only the play (and not player_data)

	(9) optional argument is_valid, a function 

	(10) optional argument score, a function

	returning:
		a single string conforming to the 'Oh Hell' representation of a
		playing card or 2-tuple containing the the above string and
		player_data as defined by parameter 7.
	"""

	# Variable initialization for readability 
	leader = player_no == 0
	trump_suit = deck_top[1]

	# Get game state variables
	if leader:
		lead_suit, cur_winner = None, None
	else:
		lead_suit = curr_trick[0][1]
		cur_winner = det_winner(curr_trick, trump_suit,
			lead_suit)

	# Sort cards in hand
	playable_cards = det_playable(hand, lead_suit)
	all_plays = playable_cards[:]
	all_plays = flatten_suits(all_plays, trump_suit)
	winning_cards, losing_cards = analyse_plays(cur_winner, playable_cards, 
		trump_suit, lead_suit)

	

	# Determine if bid has been met

	# Note: in score_phase func call bids arguament is 11 for each player,
	# this stops players from recieving bonus 10 points and returns,
	# only number of wins
	score = score_phase((11, 11, 11, 11), prev_tricks, deck_top)
	met_bid = True if phase_bids[player_no] <= score[player_no] else False

	# Game logic implementation
	#	 1. Only one option so any other logic is extraneous
	#	 2. Playing to lose, but as leader must play absolute worst card
	#	 3. Playing to win, so play best possible card
	#	 4. Playing to lose, so get rid of good cards as long as they lose
	#	 5. Cannot Win, so save good cards for another trick
	#	 6. Playing to win
	#	    Last card to be played so don't play a better card than needed
	#	 7. Playing to win and not the last player so play best possible card

	if len(all_plays) == 1:  # 1
		return all_plays.pop()

	elif leader and met_bid:  # 2
		return losing_cards.pop(0)

	elif leader:  # 3
		return winning_cards.pop()

	elif met_bid:  # 4
		return losing_cards.pop()

	elif len(winning_cards) == 0:  # 5
		return losing_cards.pop(0)

	elif player_no == 3:  # 6
		return winning_cards.pop(0)

	else:  # 7
		return winning_cards.pop()


# ============================================================================
# 								HELPER FUNCTIONS
# ============================================================================

def suit_index(suit):
	""" takes a Char representing a card suit and returns an index
		which can be used in all of the data structures within this
		python3 implementation of 'Oh Hell'
	"""
	return 'CSDH'.find(suit)


def value(card):
	""" takes a string representing a card and returns an integer equivalent
		to the cards value, not taking into account any suits or trumps
	"""
	value_seq = "234567890JQKA"
	return value_seq.find(card[0])


def flatten_suits(sorted_cards, trump_suit):
	""" name: flatten_suits()
    
    	synopsis: a helper function to flatten the sorted_cards data
    		structure. it takes the trump_suit and a nested lists of sorted
    		cards by suit as parameters and returns a single list of cards in
    		order of card value, taking into account the trump suit and
    		correct merging of the other suits
    	
    	input(s): sorted_cards, a list of lists conforming to the sorted_cards
    		data structure used throught this implementation of 'Oh Hell'
    		trump_suit, a character

    	outputs(s): a list of strings

	"""

	# take trump cards out of the nested trump cards list
	trumps = sorted_cards[suit_index(trump_suit)]
	sorted_cards[suit_index(trump_suit)] = []

	nested_suits = []
	flattend_suits = []
	
	# Find Highest and Lowest Cards
	for i in range(len(sorted_cards)):
		if len(sorted_cards[i]) != 0:
			nested_suits.append(sorted_cards[i])

	# Merge sorted suits into flat list retaing order
	for cur_val in range(12):
		for suit in nested_suits:
			if len(suit) == 0:
				continue
			elif value(suit[0]) == cur_val:
				flattend_suits.append(suit.pop(0))

	flattend_suits += trumps

	return flattend_suits


def sort_cards(cards):
	""" name: sort_cards()

		synopsis: a helper function that takes a list of cards in the same
			suit from which returns a the same list of cards sorted in
			ascending order of card value

		input(s): a list of strings

		output(s): a list of strings
	"""
	suits = ['C', 'S', 'D', 'H']
	value_seq = "234567890JQKA"
	sorted_cards = []
	
	# Sort cards by suit then sort each suit by ascending value
	suits_2d = [[card for card in cards if card[1] == suit] for suit in suits]
	for i in range(4):
		temp_list = []
		for card in suits_2d[i]:
			temp_list.append(value(card))
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

def det_playable(hand, lead_suit):
	""" name: det_playable()

		synopsis: a helper function which determines the playable cards from
			within a hand for a given trick

		input(s): hand, a tuple of strings
			lead_suit, a character

		output(s): a list of lists
	""" 
	# sort cards by suit
	suits = 'CSDH'
	return_list = [[], [], [], []] # Clubs, Spades, Diamonds, Hearts
	hand = [[card for card in hand if card[1] == suit] for suit in suits]

	if lead_suit == None or len(hand[suit_index(lead_suit)]) == 0:
		# no leads present so return whole hand sorted
		return [sort_cards(hand[i]) for i in range(4)]
	else:
		# leads present so return only the sorted leads 
		leads = sort_cards(hand[suit_index(lead_suit)])
		return_list[suit_index(lead_suit)] = leads
		return return_list

def det_winner(cards, trump_suit, lead_suit, index_return=False):
	""" name: det_winner()

		synopsis: a helper function that will determine the highest value card
			for a given situation

		input(s): cards, a list of strings
			trump_suit, a character
			lead_suit, a character
			index_return, an optional arguament which defaults to False. By
			stipulating true, the index of the winning card from the given
			list is returned along with the string representation of the
			winning card

		output(s): a string representation of the winning card
			or
			a 2-tuple containing the winning card and said cards index from
			input list
	"""

	# variable initialization
	trumps, leads = [], []
	winner = ''

	# Sort into suits and remove cards from losing suits
	for i in range(len(cards)):
		if cards[i][1] == trump_suit:
			trumps.append(cards[i])
		elif cards[i][1] == lead_suit:
			leads.append(cards[i])

	# Sort suits and take the highest value card  as the winner
	if len(trumps) == 0:
		leads = sort_cards(leads)
		winner = leads.pop()
	else:
		trumps = sort_cards(trumps)
		winner = trumps.pop()

	return winner, cards.index(winner) if index_return else winner

def analyse_plays(cur_winner, sorted_playable_cards, trump_suit, lead_suit):
	""" name: analyse_plays()

		synopsis: a helper function which organises a hand into winning plays
			and losing plays sorted in order of ascending card value

		input(s): cur_winner, a string - the current leading play
			sorted_playable_cards, a list of lists
			trump_suit, a character
			lead_suit, a character

		output(s): a 2-tuple containing lists of strings
			(winning_plays, losing_plays)
	"""
	# return varaiable initialization
	winning_plays, losing_plays = [], []

	# determine if leader, then move and flatten cards accordingly
	if cur_winner == None:
		winning_plays = flatten_suits(sorted_playable_cards, trump_suit)
		not_the_leader = False
	else:
		leads = sorted_playable_cards.pop(suit_index(lead_suit))
		not_the_leader = True
	trumps = sorted_playable_cards.pop(suit_index(trump_suit))
	losing_plays = flatten_suits(sorted_playable_cards, trump_suit)

	# Sort cards respective to the current leading play
	if not_the_leader:
		cur_win_suit = trumps if cur_winner[1] == trump_suit else leads

		# compare cards against cur_winner and allocate win/ lose
		for card in cur_win_suit:
			comparison = det_winner([cur_winner, card], trump_suit, lead_suit)
			if comparison != cur_winner:
				winning_plays.append(card)
			else:
				losing_plays.append(card)

		# add unallocated cards to respective win/lose lists
		if cur_win_suit is not trumps:
			winning_plays += trumps
		else:
			losing_plays += leads

	return winning_plays, losing_plays

main()

