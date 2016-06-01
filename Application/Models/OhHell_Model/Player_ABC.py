from abc import ABCMeta, abstractmethod

class Player_ABC(metaclass=ABCMeta):
	_hand = []
	_name = ''
	_player_no = int()

	@abstractmethod
	def make_play():
		""" name:
			synopsis:
			input(s):
			output(s):
		"""

	def remove_card_from_hand(self, card):
		""" name: remove_card_from_hand()
			synopsis: remove a card from players hand
			input(s): card, string representation of a card
			output(s): card, string representation of a card
		"""
		if card in self._hand:
			self._hand.remove(card)
			return card
		else:
			raise NameError('{} is not players hand'.format(card))


	# Setter Methods
	def update_hand(self, cards ,new_hand=True):
		""" name: update_hand()
			synopsis: update a players hand with new cards
			input(s):
				cards, a list of strings to be added to hand
				new_hand, an optional arg that determines if cards are added
				to an existing handor the old hand is cleared before new
				cards are added
			output(s):
				None
		"""
		# _hand must be <type=list>
		if not isinstance(cards, list):
			cards = list(cards)

		if new_hand:
			self._hand = cards
		elif isinstance(cards, str):
			self._hand.append(cards)
		else:
			self._hand += cards

	def set_player_name(self, player_name):
		""" name: set_player_name()
			synopsis: update players name
			input(s): player_name, a string
			output(s): None
		"""
		self._name = player_name

	# Getter Methods
	def get_name(self):
		""" name: get_name()
			synopsis: retrieve players name
			input(s):  None
			output(s): players_name, string
		"""	
		return self._name	

	def get_player_no(self):
		""" name: get_player_no()
			synopsis: retrive player number from data members
			input(s): None
			output(s): player_no, an integer
		"""	
		return self._player_no	

	def get_hand(self):
		""" name: get_hand()
			synopsis: retrive players current hand from data members
			input(s): None
			output(s): hand, a list of cards
		"""	
		return self._hand



if __name__ == "__main__":
	class MyClass(Player_ABC):
		def __init__(self, hand, name, player_no):
			self._hand = hand
			self._player_no =player_no
			self._name = name

		def make_play(self):
			pass
			
	# Perfrom Tests
	passed = 0

	player = MyClass(['AS', 'AH', 'AC', '2D'], "NICKO", 1)
	# Test: Get hand
	hand = player.get_hand()
	if hand == ['AS', 'AH', 'AC', '2D']:
		passed += 1



	# Test: Remove card from hand
	player.remove_card_from_hand('2D')
	hand = player.get_hand()
	if hand == ['AS', 'AH', 'AC']:
		passed += 1
	
	# Test: Add a card to hand
	player.update_hand('2C', new_hand=False)
	hand = player.get_hand()
	if hand == ['AS', 'AH', 'AC', '2C']:
		passed += 1

	# Test Set a new hand
	player.update_hand(['0D', '9S'])
	hand = player.get_hand()
	if hand == ['0D', '9S']:
		passed += 1

	# Test: Get Player Name
	name = player.get_name()
	if name == "NICKO":
		passed += 1

	# Test: Set name
	player.set_player_name('ayyy lmao')
	name = player.get_name()
	if name == 'ayyy lmao':
		passed += 1

	# Test: Get player number
	player_num = player.get_player_no()
	if player_num == 1:
		passed += 1


	print('Player_ABC: {} out of {} tests passed'.format(passed, 7))
