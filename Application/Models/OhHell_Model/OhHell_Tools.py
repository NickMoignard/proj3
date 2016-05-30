from copy import deepcopy
from Tools_ABC import Tools_ABC

class OhHell_Tools(Tools_ABC):

	def __init__(self):
		pass

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
				self.int_to_str(card) for card in cards if card//13 == suit
			] for suit in range(4)]

		# Add sorted trumps to end of flat sorted cards list
		elif trump_suit is not None:
			print('entered')
			tmp_trumps = []
			for card in cards:
				if card//13 == self.suit_index(trump_suit):
					card_copy = deepcopy(card)
					tmp_trumps.append(card_copy)
				for card in tmp_trumps:
					if card in cards:
						cards.remove(card)
			cards += tmp_trumps

		# Convert cards to strings before returning
		return cards if nest else [self.int_to_str(card) for card in cards]

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

if __name__ == "__main__":
	tools = OhHell_Tools()
	print(tools._suits)
	print(tools._value_seq)
	print(tools.suit_index("H"))
	print(tools.int_to_str(50))
	print(tools.str_to_int("KH"))
	print(tools.sort_cards(('AS','AC','0C','KH')))
	print(tools.sort_cards(('AS','AC','0C','KH'), nest=True))
	print(tools.sort_cards(('AS','AC','0C','KH'), trump_suit="H"))