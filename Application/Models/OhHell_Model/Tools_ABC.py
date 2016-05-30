from abc import abstractmethod, ABCMeta


class Tools_ABC(metaclass=ABCMeta):
	# Data Members to be overridden
	_suits = "CSDH"
	_value_seq = "234567890JQKA"

	def suit_index(self, suit):
		""" name: suit_index()
			synopsis: converts a suit into an integer
			input(s): suit, a character
			output(s): an integer
		"""
		return self._suits.find(suit)

	def str_to_int(self, card):
		""" name: str_to_int()
			synopsis: determines the integer equivalent of a card
			input(s): card, a string representation of a card
			output(s): an integer
		"""
		if isinstance(card, int):
			raise TypeError('card must be a string')

		card_val = self._value_seq.find(card[0])
		suit_val = self._suits.find(card[1]) * 13
		return  card_val + suit_val

	def int_to_str(self, card):
		""" name: value_to_str()
			synopsis:
				convert int representation of card to string representation
			input(s): card, an integer
			output(s): a string
		"""
		if isinstance(card, str):
			raise TypeError('card must be an integer')
		suit = card // 13
		value = card % 13
		return self._value_seq[value] + self._suits[suit]

	# Abstract Base Methods
	@abstractmethod
	def sort_cards():
		""" name: sort_cards()
			synopsis: sort list of cards
			input(s):
			output(s):
		"""

	@abstractmethod
	def det_winner():
		""" name: det_winner()
			synopsis: a helper function to determine the highest value card
			input(s):
			output(s):
		"""
		


if __name__ == "__main__":
	#tests
	pass


