init python:
    """
    Events
    game: Runs when the player starts a game with Yuri
    game_lost: Runs when the player loses a game against Yuri
    game_draw: Runs when the player draws a game against Yuri
    game_won: Runs when the player wins a game against Yuri
    """
    # Fires anytime Yuri's sanity changes
    class GiftEvent(Event):
        def __init__(self, gift):
            self.gift = gift