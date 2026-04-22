init python:
    """
    Events
    gift: Runs whenever a gift is detected
    """
    # Fires anytime Yuri's sanity changes
    class GiftEvent(Event):
        def __init__(self, gift):
            self.gift = gift