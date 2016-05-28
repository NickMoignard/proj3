 from copy import deepcopy
from itertools import cycle
from random import randint

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
