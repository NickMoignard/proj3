Due 25th of May 2016
an implementation of 'Oh Hell' a cardgame

There are four questions, details are found with project brief

FAQ

What are trumps?

Trumps are the suit of highest power, such that a trump card played in a given trick will beat any trump card. If no trumps are played, the suit of the leading card determines the winner. For example:

Deck top: '0S'; Trick: '5D', '8D', '5S', '0D' — as only Player 3 played a card which is a trump (a spade), he/she wins this trick.
Deck top: '0S'; Trick: '5D', '8D', 'QH', '0D' — no trumps (i.e. spades) played, so Player 4 is the winner, as he/she played the highest value card of the suit that was led (diamonds).
Can we assume that all card inputs will be valid?

Yes.

How do we submit our code?

We will set up a submission mechanism via Grok, but in the meantime, develop your code in IDLE (making sure to save/back it up suitably).

Is bonus_bid also subject to the forced bids of phases 4, 8, 10, 12, and 16?

Yes.

In the spec for score_phase you describe parameter "bids, a 4-tuple, containing the bids of the players, in order of player_no" but it is not clear what player_no is here. Do you simply mean in order 0, 1, 2, 3?

Yes, where 0 means the player who led the first trick for the phase.
