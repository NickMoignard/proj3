class Trick(OhHellModeloh):
	_player_order = itertools.cycle([0, 1, 2, 3])


	#Store Players Object in an iterable?

	# deal cards to iterable call Next() *4
	# get winners index and call next() that number of times to ensure player order

	def is_valid_play(play, curr_trick, hand, self):

	def start_trick(self):
		""" generate plays for bots and get user input """
	def get_play(self):
		""" get users input """
	def display_cur_trick(self):
	
	def __init__(self):

		# Init Seating Order =================================================
		self._seat = cycle([0, 1, 2, 3])
		self._first_player_of_trick = int(_first_player_of_trick)

		for i in range(self._first_player_of_trick):
			self._leading_player = next(self._seat)
