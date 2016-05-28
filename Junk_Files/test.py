def det_playable(cur_trick, hand):
	suits = 'CSDH'
	# Sort cards by suit
	hand = [[card for card in hand if card[1] == suit] for suit in suits]

	if len(cur_trick) == 0:
		return hand
	else:
		lead_suit = cur_trick[0][1]
		lead_suit_in_hand = hand[suits.find(lead_suit)]

		return hand if len(lead_suit_in_hand) == 0 else lead_suit_in_hand

print(det_playable(('2S', '4H'), ('QS', 'JS', 'AS', 'AD')))

# def sort_cards(cards):
# 	suits = ['C', 'S', 'D', 'H']
# 	value_seq = "234567890JQKA"
# 	sorted_cards = []
	
# 	# Sort cards by suit then sort each suit by ascending value
# 	suits_2d = [[card for card in cards if card[1] == suit] for suit in suits]
# 	for i in range(4):
# 		temp_list = []
# 		for card in suits_2d[i]:
# 			temp_list.append(value_seq.find(card[0]))
# 		suits_2d[i] = sorted(temp_list)

# 	# Sort each card in list
# 	num_cards_to_sort = len(cards)
# 	while num_cards_to_sort > 0:

# 		# Find suit with lowest value card
# 		suit_with_lowest_card = None
# 		i = 0

# 		# Find initial lowest card
# 		while i < 4:
# 			if len(suits_2d[i]) == 0:  # suit is empty
# 				i += 1
# 				continue
# 			else:
# 				suit_with_lowest_card = suits_2d[i]  
# 				break

# 		# Compare initial lowest to lowest in each suit
# 		while i < 4:
# 			try:
# 				if suit_with_lowest_card[0] > suits_2d[i][0]:
# 					suit_with_lowest_card = suits_2d[i]
# 					i += 1
# 				else:
# 					i += 1
# 			except IndexError:
# 				i += 1
# 		print('lowest suit', suit_with_lowest_card)

# 		# Pop the next lowest card and add to a list
# 		for i in range(4):
# 			if suit_with_lowest_card is suits_2d[i]:
# 				low_card = ""
# 				low_card += value_seq[suit_with_lowest_card[0]] + suits[i]
# 				sorted_cards.append(low_card)
# 				suit_with_lowest_card.pop(0)

# 		num_cards_to_sort -= 1

# 	return sorted_cards

# print(sort_cards(('7H', '7D', '7S', '7C')))