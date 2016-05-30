
from OhHell_Tools import OhHell_Tools
from copy import deepcopy
from random import shuffle

class Deck():
	def __init__(self):
		self.tools = OhHell_Tools()  # think this might be bad practice
		self._cards_in_deck = list(range(52))
		self._cards_in_hands = []
		self._discarded_cards = []
		self._no_card_packs_used = 1
		self.shuffle_deck()

	def add_card_pack_to_deck(self):
		""" name: add_card_pack_to_deck()
			synopsis: add an additional 52 cards to deck
			input(s): None
			output(s): None
		"""
		
		self._cards_in_deck += list(range(52))
		self._no_card_packs_used += 1
		self.shuffle_deck()

	def deal_card(self):
		""" name: deal_card()
			synopsis: deal single card from deck
			input(s): None
			outputs(s): string represntation of card
		"""

		# Check if enough cards to deal
		if len(self._cards_in_deck) == 0 and len(self._discarded_cards) == 0:
			self.add_card_pack_to_deck()
		elif len(self._cards_in_deck) == 0:
			self.shuffle_deck()  # Shuffle in burnt cards
			
				
		card = self._cards_in_deck.pop()
		self._cards_in_hands.append(deepcopy(card))

		return self.tools.int_to_str(card)

	def burn(self, no_cards):
		""" name: burn()
			synopsis: discard x no cards from deck
			input(s): no_cards, integer
			output(s): None
		"""
		# check if enough cards in deck to burn
		while no_cards > len(self._cards_in_deck):
			# Shuffle burnt cards back into deck
			self.shuffle_deck()
			if no_cards > len(self._cards_in_deck):
				# Add additional pack of cards to deck
				self.add_card_pack_to_deck()

		cards_to_burn = [self._cards_in_deck.pop() for _ in range(no_cards)]
		self._discarded_cards += cards_to_burn

	def shuffle_deck(self):
		""" name: shuffle_deck()
			synopsis: take discarded cards and re shuffle them into deck
			input(s): None
			output(s): None
		"""
		deck = self._cards_in_deck + self._discarded_cards
		self._discarded_cards = []
		shuffle(deck)
		self._cards_in_deck = deck

	def discard(self, card_to_discard):
		""" name: discard()
			synopsis: take card from players hand and add to discard pile
			input(s): card_to_discard, a string representation of a card
			output(s): None
		"""
		card = self.tools.str_to_int(card_to_discard)

		if card in self._cards_in_hands:
			self._cards_in_hands.remove(card)
			self._discarded_cards.append(card)
		else:
			raise ValueError(
				'{} is not currently in any players hands'.format(card)
			)

# perfom tests
if __name__ == "__main__":

	players_hands = [[], [], [], []]
	passed = 0
	deck = Deck()

	# Test: Deal one card
	card = deck.deal_card()
	if len(deck._cards_in_deck) == 51 and len(deck._cards_in_hands) == 1:
		passed += 1

	del deck
	deck = Deck()

	# Test: Deal Mutiple cards
	for _ in range(2):
		for i in range(4):
			players_hands[i].append(deck.deal_card())

	if len(deck._cards_in_deck) == (44) and len(deck._cards_in_hands) == 8:
		passed += 1

	# Test: Discard card from a hand
	rm_card = players_hands[0].pop()
	deck.discard(rm_card)

	if len(deck._discarded_cards) == 1 and len(deck._cards_in_hands) == 7:
		# discard a card
		passed += 1

	del deck
	players_hands = [[], [], [], []]
	deck = Deck()

	# Test: Burn cards from top of deck
	deck.burn(10)
	if len(deck._discarded_cards) == 10 and len(deck._cards_in_deck) == 42:
		# discard a card
		passed += 1

	# Test: Shuffle the burnt cards back into deck
	deck.shuffle_deck()
	if len(deck._cards_in_deck) == 52 and len(deck._discarded_cards) == 0:
		passed += 1

	# Test: Multiple Decks
	deck.add_card_pack_to_deck()
	if len(deck._cards_in_deck) == 104 and deck._no_card_packs_used == 2:
		passed += 1

	del deck
	deck = Deck()

	# Test: Deal cards until additional deck is added
	for _ in range(100):
		players_hands[0].append(deck.deal_card())
	if len(deck._cards_in_deck) == 4 and len(deck._cards_in_hands) == 100:
		passed += 1

	# Test: Discarding with multiple decks
	for _ in range(100):
		rm_card = players_hands[0].pop()
		deck.discard(rm_card)
	if len(deck._cards_in_hands) == 0 and len(deck._discarded_cards) == 100:
		passed += 1

	# Test: Shuffle Cards back into deck
	deck.shuffle_deck()
	if len(deck._cards_in_deck) == 104 and len(deck._discarded_cards) == 0:
		passed += 1

	del deck
	deck = Deck()

	# Test: Burn cards until additional deck is added
	deck.burn(53)
	if len(deck._cards_in_deck) == 51 and len(deck._discarded_cards) == 53:
		passed += 1

	print('Deck: {} out of 10 tests passed'.format(passed))















