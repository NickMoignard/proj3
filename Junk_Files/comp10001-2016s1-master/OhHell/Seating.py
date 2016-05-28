class Seating():
	def move_lead(self, new_lead):
		""" name: move_lead()
			synopsis: rotate lead seat to the new lead player
			input(s): new_lead, and integer between 0 - 3 inclusive
			output(s): None
		"""
		finshed = False
		while not finshed:
			seat = next(self._seat)
			if seat == new_lead:
				finshed = True


	def rotate_dealer(self):
		""" name: rotate_dealer()
			synopsis: analogous to moving the deck of cards to the next player
				 to deal
			input(s): None
			output(s): None
		"""
		self._leading_player = next(self._seat)

	def __init__(self, first_player):
		self._seat = cycle([0, 1, 2, 3])
		self._first_player = int(first_player)

		for i in range(self._first_player):
			self._leading_player = next(self._seat)

