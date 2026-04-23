init python:
    """
    Events
    game: Runs when the player starts a game with Yuri
    game_lost: Runs when the player loses a game against Yuri
    game_draw: Runs when the player draws a game against Yuri
    game_won: Runs when the player wins a game against Yuri
    """

    class GameEvent(Event):
        def __init__(self, game):
            self.game = game

    class GameStartEvent(GameEvent):
        pass

    class GameStopEvent(GameEvent):
        pass

    class GameWonEvent(GameEvent):
        pass

    class GameDrawEvent(GameEvent):
        pass

    class GameLostEvent(GameEvent):
        def __init__(self, game, forefit):
            super().__init__(self, game)
            self.forefit = forefit