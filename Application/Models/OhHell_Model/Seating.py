from itertools import cycle
class Seating():
	def __init__(self, seats, first_player=0):
		self._seat = cycle(range(seats))
		self._first_player = int(first_player)
		# Initialize seating
		for i in range(self._first_player + 1):
			self._leading_player = next(self._seat)
	def move_lead(self, new_lead):
		""" name: move_lead()
			synopsis: rotate lead seat to the new lead player
			input(s): new_lead, and integer between 0 - 3 inclusive
			output(s): None
		"""
		finshed = False
		while not finshed:
			self._leading_player = next(self._seat)
			if self._leading_player == new_lead:
				finshed = True


	def next_seat(self):
		""" name: next_player()
			synopsis: analogous to moving the deck of cards to the next player
				 to deal
			input(s): None
			output(s): None
		"""
		self._leading_player = next(self._seat)

if __name__ == "__main__":
	# perform tests
	passed = 0

	# Test: Initialization of data members
	table = Seating(4)
	if isinstance(table._seat, cycle):
		passed += 1
	if table._first_player == 0:
		passed += 1
	if table._leading_player == 0:
		passed += 1

	# Test: next_seat()
	table.next_seat()
	if table._leading_player == 1:
		passed += 1

	#Test: move_lead()
	table.move_lead(0)
	if table._leading_player == 0:
		passed += 1

	print('Seating: {} out of 5 tests passed'.format(passed))