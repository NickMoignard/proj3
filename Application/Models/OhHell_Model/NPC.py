from OhHell_Player_ABC import OhHell_Player_ABC
from copy import deepcopy

class NPC(OhHell_Player_ABC):
	
	def __init__(self, player_no):
		self._name = "NPC_" + str(player_no)
		self._player_no = player_no
		self._hand = []

	def make_play(self, cur_trick, cur_score, deck_top, seat):
		""" name:play()
			synopsis: determines the best card to play in a trick for given
				conditions of a game of 'Oh Hell' that takes parameters:
		
			inputs(s):
				curr_trick a tuple containing the cards played in the current
				incomplete trick
				cur_score, 4-tuple, contains the current phase score to
					determine if player has met a bid
				deck_top, the top card of the deck, used to determine trumps
					for the current phase
				seat, an integer 0-3 inclusive. determines number of plays
					before players turn
			output(s): card, a string
		"""
		player_no = seat
		hand = self._hand
		# Variable initialization for readability 
		leader = player_no == 0
		trump_suit = deck_top[1]

		# Get game state variables
		if leader:
			lead_suit, cur_winner = None, None
		else:
			lead_suit = cur_trick[0][1]
			cur_winner = self.tools.det_winner(cur_trick, trump_suit,
				lead_suit)

		# Sort cards in hand
		playable_cards = self.det_playable(lead_suit)

		#1 If only one card playbable. must play that card
		all_plays = deepcopy(playable_cards)
		all_plays = self.tools.sort_cards(all_plays, trump_suit=trump_suit)
		if len(all_plays) == 1:  # 1
			return self.remove_card_from_hand(all_plays.pop())

		winning_cards, losing_cards = self._analyse_plays(
			cur_winner, playable_cards, trump_suit, lead_suit
		)


		# Determine if bid has been met
		if cur_score[self._player_no] == phase_bids[self._player_no]:
			met_bid = True
		else:
			met_bid = False
		# Game logic implementation
		#	 1. Only one option so any other logic is extraneous
		#	 2. Playing to lose, but as leader must play absolute worst card
		#	 3. Playing to win, so play best possible card
		#	 4. Playing to lose, so get rid of good cards as long as they lose
		#	 5. Cannot Win, so save good cards for another trick
		#	 6. Playing to win
		#	    Last card to be played so don't play a better card than needed
		#	 7. Playing to win and not the last player so play best possible card

		print(winning_cards, losing_cards)

		if leader and met_bid:  # 2
			play = losing_cards.pop(0)
			print('2')

		elif leader:  # 3
			play = winning_cards.pop()
			print('3')

		elif met_bid:  # 4
			play = losing_cards.pop()
			print('4')

		elif len(winning_cards) == 0:  # 5
			play = losing_cards.pop(0)
			print('5')

		elif player_no == 3:  # 6
			play = winning_cards.pop(0)
			print('6')

		else:  # 7
			play = winning_cards.pop()
			print('7')

		return self.remove_card_from_hand(play)

	def init_bid(self, hand, phase_no):
		""" name: bid()
			synopsis: returns a the number of rounds a NPC aims to win for 
				a given phase

			input(s):
				hand, a tuple of cards that you have been dealt for the current
					phase, or in the case of Phase 1 or 19,
					representing the cards of the other three players

				phase_no, an integer between 1 and 19 inclusive,
					indicating the phase number

			return values:
				either a bid (integer of value 0-10)
				or a tuple (bid, player_data)
		"""

		if phase_no in [1, 10, 19]:
			# cannot see own cards so logically 0 is safest
			bid = 0
		else:
			bid = len(hand)//4

		return bid

	def _analyse_plays(self, cur_winner, cards, trump_suit, lead_suit):
		""" name: analyse_plays()

			synopsis: a private helper function which organises a hand into
				winning plays and losing plays sorted in order of ascending
				card value

			input(s): cur_winner, a string - the current leading play
				cards, a list of strings
				trump_suit, a character
				lead_suit, a character

			output(s): a 2-tuple containing lists of strings
				(winning_plays, losing_plays)
		"""
		cards_duplicate = deepcopy(cards)
		nested_cards = self.tools.sort_cards(cards, nest=True)
		trump_index = self.tools.suit_index(trump_suit)

		winning_plays, losing_plays = [], []
		all_suits = {0, 1, 2, 3}

		# determine losing suits and store indexes
		if cur_winner is not None:
			the_leader = False
			lead_index = self.tools.suit_index(lead_suit)
			win_suits = {lead_index, trump_index}
			lose_suits = all_suits.difference(win_suits)
		else:  
			# Lead player so all cards are both winning and losing
			the_leader = True
			lead_index = None
			lose_suits = all_suits

		# use stored indexes to correctly copy lists
		for i in range(4):
			if i == lead_index:
				leads = deepcopy(nested_cards[i])

			if i == trump_index:
				trumps = deepcopy(nested_cards[i])

			if i in lose_suits:
				losing_plays.append(nested_cards[i])

		losing_plays = self.tools.sort_cards(
											losing_plays,
											trump_suit=trump_suit
		)

		# Sort cards respective to the current leading play
		if not the_leader:
			cur_win_suit = trumps if cur_winner[1] == trump_suit else leads

			# compare cards against cur_winner and allocate win/ lose
			for card in cur_win_suit:
				comparison = self.tools.det_winner(
					[cur_winner, card], trump_suit, lead_suit
				)
				if comparison != cur_winner:
					winning_plays.append(card)
				else:
					losing_plays.append(card)

			# add unallocated cards to respective win/lose lists
			if cur_win_suit  != trumps:
				winning_plays += trumps
			else:
				losing_plays += leads
		else: # leader

			winning_plays = cards_duplicate


		return winning_plays, losing_plays


if __name__ == "__main__":
	# Perform Tests
	hand = ('AH', '2D', '3D')
	prev_tricks = (('QD', '9D', '3S', '0D'), ('KH', '8S', 'AS', 'JS'))
	score = (2, 0, 0, 0)
	deck_top = '2H'
	phase_bids = (2, 2, 0, 0)
	seat = 1
	curr_trick = ('AD',)

	NPC_1 = NPC(1)
	NPC_1.update_hand(hand)

	print(NPC_1.get_name())
	print(NPC_1.get_player_no())
	print(NPC_1.init_bid(hand, 3))
	print(NPC_1.make_play(curr_trick, score, deck_top, seat))
	