from copy import deepcopy
from itertools import cycle
from random import randint

def main():
	pass
	# phase1 = Phase()
	# phase1

class Seating():
	def move_lead(self, new_lead):
		""" name: move_lead()
			synopsis: rotate lead seat to the new lead player
			input(s): new_lead, and integer between 0 - 3 inclusive
			output(s): None
		"""
		finshed = False
		while not finshed:
			seat = next(self._seat)
			if seat == new_lead:
				finshed = True


	def rotate_dealer(self):
		""" name: rotate_dealer()
			synopsis: analogous to moving the deck of cards to the next player
				 to deal
			input(s): None
			output(s): None
		"""
		self._leading_player = next(self._seat)

	def __init__(self, first_player):
		self._seat = cycle([0, 1, 2, 3])
		self._first_player = int(first_player)

		for i in range(self._first_player):
			self._leading_player = next(self._seat)

class OhHellModel():
	_suits = "CSDH"
	_value_sequence = "234567890JQKA"

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

		return scor

class Phase(OhHellModel):
	def __init__(self, phase_no, first_player_of_phase):
		_phase_num, _num_tricks = int(), int()
		_prev_tricks = tuple()
		_bids = tuple()
		_deck_top = str()
		_cur_trick = tuple()
		self.initialize_seating_order(first_player_of_phase)
	
	def score_phase(
		self, bids, tricks, deck_top, player_data=None,
		suppress_player_data=True
	):
		pass

	def display_hand(self):
		

		pass

	def display_bids(self):
		pass

	def next_trick(self):
		""" score previous phase, reset player order and call the next trick
		"""
		pass
	def get_bids(self):
		""" show users cards and ask for input """
		pass

main()