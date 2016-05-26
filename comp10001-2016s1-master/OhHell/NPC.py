from itertools import cycle
from copy import deepcopy

class OhHellModel():
	_suits = "CSDH"
	_value_sequence = "234567890JQKA"

	def __init__():
		print('this will be a fun game')

	def suit_index(self, suit):
		""" takes a Char representing a card suit and returns an index
			which can be used in all of the data structures within this
			python3 implementation of 'Oh Hell'
		"""
		return 'CSDH'.find(suit)

	def value(self, card):
		""" takes a string representing a card and returns an integer
			equivalent
			to the cards value, not taking into account any suits or trumps
		"""
		return self._value_sequence.find(card[0])

	def flatten_suits(self, sorted_cards, trump_suit=None):
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
		if trump_suit is not None:
			# take trump cards out of the nested trump cards list
			trumps = sorted_cards[self.suit_index(trump_suit)]
			sorted_cards[self.suit_index(trump_suit)] = []

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
				elif self.value(suit[0]) == cur_val:
					flattend_suits.append(suit.pop(0))

		if trump_suit is not None:
			flattend_suits += trumps

		return flattend_suits

	def det_winner(self, cards, trump_suit, lead_suit, index_return=False):
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
			leads = self.sort_cards(leads)
			winner = leads.pop()
		else:
			trumps = self.sort_cards(trumps)
			winner = trumps.pop()

		return winner, cards.index(winner) if index_return else winner

	def sort_cards(self, cards):
		""" name: sort_cards()

			synopsis: a helper function that takes a list of cards in the same
				suit from which returns a the same list of cards sorted in
				ascending order of card value

			input(s): a list of strings

			output(s): a list of strings
		"""
		suits = self._suits
		value_seq = self._value_sequence
		sorted_cards = []
		
		# Sort cards by suit then sort each suit by ascending value
		suits_2d = [[card for card in cards if card[1] == suit]
			for suit in suits]

		for i in range(4):
			temp_list = []
			for card in suits_2d[i]:
				temp_list.append(self.value(card))
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

	def sort_and_nest(self, cards):
		hand = [[card for card in cards if card[1] == suit]
			for suit in self._suits]

		return [self.sort_cards(hand[i]) for i in range(4)]

	def _score_phase(self, bids, tricks, deck_top):
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
		winning_player = next(seating_order)  

		# Determine the winner of each trick and increment score
		for trick in tricks:
			_winner, winning_index = self.det_winner(
				trick, deck_top[1], trick[0][1], index_return=True
			)

			# using seating order determine which player played won the trick
			for _ in range(winning_index):
				winning_player = next(seating_order)

			score[winning_player] += 1

		# Check the results of players bids and increment score acordingly
		for player in range(4):
			if score[player] == bids[player]:
				score[player] += 10

		return score


class NPC(OhHellModel):
	

	def __init__(self, player_no):
		self._name = "NPC_" + str(player_no)
		self._player_no = player_no
		self._hand = [[], [], [], []]

	# Public Methods =========================================================
	def make_play(
		self, curr_trick, prev_tricks, deck_top, phase_bids, seat
	):

		""" name:play()
			synopsis: determines the best card to play in a trick for given
				conditions of a game of 'Oh Hell' that takes parameters:
		
			inputs(s):
				curr_trick a tuple containing the cards played in the current
				incomplete trick

				prev_tricks, which takes the form of a tuple of completed
					tricks for the current phase (each of which is a 4-tuple)


				deck_top, the top card of the deck, used to determine trumps
					for the current phase

				phase_bids, a tuple containing the bids of the players for the
					current phase, in order of player_no
					(startingfromplayer_no = 0)

				seat, an integer 0-3 inclusive. determines number of plays
					before players turn

			output(s):
				a single string conforming to the 'Oh Hell' representation of
				a playing card or 2-tuple containing the the above string and
				player_data as defined by parameter 7.
		"""
		player_no = seat
		hand = self._hand
		# Variable initialization for readability 
		leader = player_no == 0
		trump_suit = deck_top[1]

		# Get game state variables
		if leader:
			lead_suit, cur_winner = None, None
		else:
			lead_suit = curr_trick[0][1]
			cur_winner = self.det_winner(curr_trick, trump_suit,
				lead_suit)

		# Sort cards in hand
		playable_cards = self._det_playable(lead_suit)

		#1 If only one card playbable. must play that card
		all_plays = deepcopy(playable_cards)
		all_plays = self.flatten_suits(all_plays, trump_suit)
		if len(all_plays) == 1:  # 1
			return self._remove_card_from_hand(all_plays.pop())


		winning_cards, losing_cards = self._analyse_plays(
			cur_winner, playable_cards, trump_suit, lead_suit
		)


		# Determine if bid has been met

		# Note: in score_phase func call bids arguament is 11 for each player,
		# this stops players from recieving bonus 10 points and returns,
		# only number of wins
		score = self._score_phase((11, 11, 11, 11), prev_tricks, deck_top)
		
		met_bid = True if score[player_no] == phase_bids[player_no] else False
		# Game logic implementation
		#	 1. Only one option so any other logic is extraneous
		#	 2. Playing to lose, but as leader must play absolute worst card
		#	 3. Playing to win, so play best possible card
		#	 4. Playing to lose, so get rid of good cards as long as they lose
		#	 5. Cannot Win, so save good cards for another trick
		#	 6. Playing to win
		#	    Last card to be played so don't play a better card than needed
		#	 7. Playing to win and not the last player so play best possible card

		print(winning_cards, losing_cards)

		if leader and met_bid:  # 2
			play = losing_cards.pop(0)
			print('2')

		elif leader:  # 3
			play = winning_cards.pop()
			print('3')

		elif met_bid:  # 4
			play = losing_cards.pop()
			print('4')

		elif len(winning_cards) == 0:  # 5
			play = losing_cards.pop(0)
			print('5')

		elif player_no == 3:  # 6
			play = winning_cards.pop(0)
			print('6')

		else:  # 7
			play = winning_cards.pop()
			print('7')

		return self._remove_card_from_hand(play)

	def bid(self, hand, phase_no):
		""" name: bid()
			synopsis: returns a the number of rounds a NPC aims to win for 
				a given phase

			input(s):
				hand, a tuple of cards that you have been dealt for the current
					phase, or in the case of Phase 1 or 19,
					representing the cards of the other three players

				phase_no, an integer between 1 and 19 inclusive,
					indicating the phase number

			return values:
				either a bid (integer of value 0-10)
				or a tuple (bid, player_data)
		"""

		if phase_no in [1, 10, 19]:
			# cannot see own cards so logically 0 is safest
			bid = 0
		else:
			bid = len(hand)//4

		return bid

	def _remove_card_from_hand(self, chosen_card):
		""" name: remove_card_from_hand()

			synopsis: remove a card from a players hand and return it

			input(s): card to be removed, a string. & self

			output(s): the removed card a string
		"""
		flat_hand = self.flatten_suits(self._hand)
		if chosen_card in flat_hand:
			flat_hand.remove(chosen_card)

		hand = self.sort_and_nest(flat_hand)

		self._hand = hand

		return chosen_card


	# Getter Methods =========================================================
	def get_name(self):
		return self._name

	def get_player_no(self):
		return self._player_no

	# Setter Methods =========================================================
	def set_new_hand(self, list_of_cards):
		# sort and nest cards
		self._hand = self.sort_and_nest(list_of_cards)


	def set_player_number(self, player_no):
		self._player_no = player_no

	def set_player_name(self, name):
		self._name = name

	# Non-Public Methods =====================================================
	def _det_playable(self, lead_suit):
		""" name: det_playable()

			synopsis: a helper function which determines the playable cards
				from within a hand for a given trick

			input(s): hand, a tuple of strings
				lead_suit, a character

			output(s): a list of lists
		""" 
		# sort cards by suit
		suits = self._suits
		return_list = [[], [], [], []] # Clubs, Spades, Diamonds, Hearts

		hand = self._hand

		if lead_suit == None or len(hand[self.suit_index(lead_suit)]) == 0:
			# no leads present so return whole hand sorted
			return [self.sort_cards(hand[i]) for i in range(4)]
		else:
			# leads present so return only the sorted leads 
			leads = self.sort_cards(hand[self.suit_index(lead_suit)])
			return_list[self.suit_index(lead_suit)] = leads
			return return_list

	def _analyse_plays(
		self, cur_winner, sorted_playable_cards, trump_suit, lead_suit
	):
		""" name: analyse_plays()

			synopsis: a private helper function which organises a hand into
				winning plays and losing plays sorted in order of ascending
				card value

			input(s): cur_winner, a string - the current leading play
				sorted_playable_cards, a list of lists
				trump_suit, a character
				lead_suit, a character

			output(s): a 2-tuple containing lists of strings
				(winning_plays, losing_plays)
		"""


		winning_plays, losing_plays = [], []
		all_suits = {0, 1, 2, 3}
		trump_index = self.suit_index(trump_suit)
		cards = deepcopy(sorted_playable_cards)

		# determine losing suits and store indexes
		if cur_winner is not None:
			the_leader = False
			lead_index = self.suit_index(lead_suit)
			win_suits = {lead_index, trump_index}
			lose_suits = all_suits.difference(win_suits)
		else:  
			# Lead player so all cards are both winning and losing
			the_leader = True
			lead_index = None
			lose_suits = all_suits	

		# use stored indexes to correctly copy lists
		for i in range(4):
			if i == lead_index:
				leads = deepcopy(sorted_playable_cards[i])

			if i == trump_index:
				trumps = deepcopy(sorted_playable_cards[i])

			if i in lose_suits:
				losing_plays.append(cards[i])

		losing_plays = self.flatten_suits(losing_plays)

		# Sort cards respective to the current leading play
		if not the_leader:
			cur_win_suit = trumps if cur_winner[1] == trump_suit else leads

			# compare cards against cur_winner and allocate win/ lose
			for card in cur_win_suit:
				comparison = self.det_winner(
					[cur_winner, card], trump_suit, lead_suit
				)
				if comparison != cur_winner:
					winning_plays.append(card)
				else:
					losing_plays.append(card)

			# add unallocated cards to respective win/lose lists
			if cur_win_suit  != trumps:
				winning_plays += trumps
			else:
				losing_plays += leads
		else: # leader

			winning_plays = self.flatten_suits(
				sorted_playable_cards, trump_suit
			)


		return winning_plays, losing_plays


if __name__ == "__main__":

	hand = ('AH', '2D', '3D')
	prev_tricks = (('QD', '9D', '3S', '0D'), ('KH', '8S', 'AS', 'JS'))
	deck_top = 'KH'
	phase_bids = (2, 0, 0, 0)
	seat = 1
	curr_trick = ('AD',)

	NPC_1 = NPC(1)
	NPC_1.set_new_hand(hand)

	print(NPC_1.get_name())
	print(NPC_1.get_player_no())
	print(NPC_1.bid(hand, 3))
	print(NPC_1.make_play(curr_trick, prev_tricks, deck_top, phase_bids, seat))
	