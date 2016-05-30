from itertool import cycle
import OhHell_Tools
from copy import deepcopy

class Deck(self):
	def __init__(self):
		self._cards_in_deck = list(range(52))
		self._cards_in_hands = []
		self._discarded_cards = []
		self._no_card_packs_used = 1

	def add_card_pack_to_deck(self):
		""" name: add_card_pack_to_deck()
			synopsis: add an additional 52 cards to deck
			input(s): None
			output(s): None
		"""
		self._cards_in_deck += list(range(52))
		self._no_card_packs_used += 1
		self.shuffle_deck()

	def deal(self, no_cards, seats=1):
		""" name: deal()
			synopsis: deal x number of cards from deck to n number of seats
			input(s):
				no_cards an integer,
				Optional Arg seats, takes an int, will deal x no cards to n
				number of seats
			outputs(s):
				a list of cards or nested lists of dealt cards for each player
		"""
		deck = self._cards_in_deck

		# Check if enough cards to deal
		tot_cards_needed = no_cards*seats
		if tot_cards_needed > len(deck):
			self.shuffle_deck()  # Shuffle in burnt cards
			if tot_cards_needed > len(deck):
				self.add_card_pack_to_deck()
				

		# deal cards from deck
		if seats == 1:
			cards_to_deal = [deck.pop() for _ in range(no_cards)]
		else:
			cards_to_deal = [
				[deck.pop() for _ in range(no_cards)] for seat in range(seats)
			]

		# Add dealt cards to cards_in_hands to keep track of each card in deck
		cards = deepcopy(cards_to_deal)
		cards = OhHell_Tools.sort_cards(cards)
		self._cards_in_hands += cards

		return cards_to_deal

	def burn(self, no_cards):
		""" name: burn()
			synopsis: discard x no cards from deck
			input(s): no_cards, integer
			output(s): None
		"""
		# check if enough cards in deck to burn
		if no_cards > len(deck):
			# Shuffle burnt cards back into deck
			self.shuffle_deck()
			if no_cards > len(deck):
				# Add additional pack of cards to deck
				self.add_card_pack_to_deck()

		cards_to_burn = [self.cards_in_deck.pop() for _ in range(no_cards)]
		self._discarded_cards += cards_to_burn

	def shuffle_deck(self):
		""" name: shuffle_deck()
			synopsis: take discarded cards and re shuffle them into deck
			input(s): None
			output(s): None
		"""
		deck = self._cards_in_deck + self._discarded_cards
		shuffle(deck)
		self._cards_in_deck = deck

	def discard(self, card_to_discard):
		""" name: discard()
			synopsis: take card from players hand and add to discard pile
			input(s): card_to_discard, a string representation of a card
			output(s): None
		"""
		if card in self._cards_in_hands:
			self._cards_in_hands.remove(card)
			self._discarded_cards += card
		else:
			raise ValueError(
				'{} is not currently in any players hands'.format(card)
			)


if __name__ == "__main__":
	# create a deck
	new_deck = Deck()

	deck_top = new_deck.deal(1)
	# deal one card
	# deal 10 cards
	# deal 10 cards with 4 seats 
	# burn
	# shuffle
	# discard

















