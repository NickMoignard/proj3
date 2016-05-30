from copy import deepcopy
from Tools_ABC import Tools_ABC

class OhHell_Tools(Tools_ABC):

	def sort_cards(self, cards, nest=False, trump_suit=None):
		""" name: sort_cards()
			synopsis: sort list of cards by ascending value
			input(s):
				cards, a list of cards or list of list of  cards
				nest, an optional Boolean
				trump, an optional arg. 
			output(s):
				either a list of lists of cards
				or, a list of cards
		"""
		

		# Flatten Cards if nested
		if isinstance(cards[0], list):
			cards = [card for sublist in cards for card in sublist]

		# convert cards to ints and sort by value
		cards = [self.str_to_int(card) for card in cards]
		cards.sort()

		# Nest sorted cards by suit regardless of trump suit
		if nest:
			cards = [[
				self.int_to_str(card) for card in cards if card%4 == suit
			] for suit in range(4)]

		# Add sorted trumps to end of flat sorted cards list
		elif trump_suit is not None:
			tmp_trumps = []
			for card in cards:
				if card % 4 == self.suit_index(trump_suit):
					card_copy = deepcopy(card)
					tmp_trumps.append(card_copy)
				for card in tmp_trumps:
					if card in cards:
						cards.remove(card)
			cards += tmp_trumps

		# Convert cards to strings before returning
		return cards if nest else [self.int_to_str(card) for card in cards]

	def det_winner(self, cards, lead_suit=None, trump_suit=None):
		""" name: det_winner()
			synopsis: a helper function to determine a winning card
			input(s): cards, a list of cards
				trump_suit, char representation of suit
				lead_suit, char representation of suit
			output(s): a string representation of the winning card
		"""

		trumps, leads = [], []  # empty lists prevent NameErrors
		cards = self.sort_cards(cards, nest=True)

		# determine card heirachy
		if trump_suit is not None:
			trumps = deepcopy(cards[self.suit_index(trump_suit)])
		if lead_suit is not None:
			leads = deepcopy(cards[self.suit_index(lead_suit)])


		# return highest value card after checking for hierarchical winners
		if len(trumps) != 0:
			trumps = self.sort_cards(trumps)	
			return trumps.pop()
		elif len(leads) != 0:
			leads = self.sort_cards(leads)
			return leads.pop()
		else:
			cards = self.sort_cards(cards)  # flatten
			return cards.pop()

if __name__ == "__main__":
	
	tools = OhHell_Tools()
	passed = 0

	if tools._suits == "CSDH":
		passed += 1

	if tools._value_seq == "234567890JQKA":
		passed += 1

	if tools.suit_index("D") == 2:
		passed += 1

	if tools.int_to_str(50) == "AD":
		passed += 1

	if tools.str_to_int("AH") == 51:
		passed += 1

	if tools.sort_cards(('5S','AS','0H','2C')) == ['2C', '5S', '0H', 'AS']:
		passed += 1

	if tools.sort_cards(
						('AS','AC','0C','KH'), nest=True
	) == [['0C', 'AC'], ['AS'], [], ['KH']]:
		passed += 1

	if tools.sort_cards(
						('AS','AC','0C','KH'), trump_suit="H"
	) == ['0C', 'AC', 'AS', 'KH']:
		passed += 1

	if tools.det_winner(('5S','AS','0H','2C')) == "AS":
		passed += 1

	if tools.det_winner(('5S','AS','0H','2C'), lead_suit="H") == "0H":
		passed += 1

	if tools.det_winner(('5S','AS','0H','2C'), trump_suit="C") == "2C":
		passed += 1

	if tools.det_winner(
						('5S','AS','0H','2C'), lead_suit="H",
						trump_suit="C"
	) == "2C":
		passed += 1

	print('OhHell_Tools: {} of 12 tests passed'.format(passed))






