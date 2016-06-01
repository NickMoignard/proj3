from Player_ABC import Player_ABC
from abc import ABCMeta, abstractmethod
from OhHell_Tools import OhHell_Tools

class OhHell_Player_ABC(Player_ABC, metaclass=ABCMeta):

	tools = OhHell_Tools()
	_bid_for_current_hand = int()

	def get_cur_bid(self):
		""" name: get_cur_bid()
			synopsis: retrieve current players bid
			input(s): None
			output(s): bid for current hand, an integer
		"""
		return self._bid_for_current_hand

	def det_playable(self, lead_suit):
		""" name: det_playable()
			synopsis: determine which cards are able to be played for a given
				trick
			input(s):
				lead_suit, a character or None
			output(s): cards, a list of playable cards
		"""
		hand = self.tools.sort_cards(self._hand, nest=True)

		# Determine if player must play a card from lead_suit
		if lead_suit is not None:
			leads = hand[self.tools.suit_index(lead_suit)]
			if leads != []:
				return leads
		else:
			return self._hand

	@abstractmethod
	def init_bid():
		""" name: init_bid()
			synopsis: determine players bid for a given hand
		"""


if __name__ == "__main__":
	# Perform Tests
	passed = 0

	class MyClass(OhHell_Player_ABC):

		def __init__(self, hand, name, player_no):
			self._hand = hand
			self._player_no =player_no
			self._name = name

		def init_bid():
			pass
		def make_play():
			pass

	player = MyClass(['AS', 'AH', 'AC', '2D'], "NICKO", 1)

	# Test: Get current bid
	bid = player.get_cur_bid()
	if bid == 0:
		passed += 1

	# Test: Determine playable cards with lead suit
	cards = player.det_playable("D")
	if cards == ['2D']:
		passed += 1

	# Test: Determine playable cards without lead suit
	cards = player.det_playable(None)
	if cards == ['AS', 'AH', 'AC', '2D']:
		passed += 1

	print('OhHell_Tool_ABC: {} out of {} tests passed'.format(passed, 3))





