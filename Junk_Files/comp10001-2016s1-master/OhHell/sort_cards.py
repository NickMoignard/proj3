def main():
	print(sort_cards(['AH', '0H', 'JH', '2C', '3C', '7C', 'QD','AD']))

def suit_index(suit):
	""" takes a Char representing a card suit and returns an index
		which can be used in all of the data structures within this
		python3 implementation of 'Oh Hell'
	"""
	return 'CSDH'.find(suit)

def value(card):
	""" takes a string representing a card and returns an integer
		equivalent
		to the cards value, not taking into account any suits or trumps
	"""
	value_seq = "234567890JQKA"
	return value_seq.find(card[0])

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

main()