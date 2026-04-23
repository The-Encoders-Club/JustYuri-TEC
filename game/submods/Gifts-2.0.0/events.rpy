init python:
    """
    Events
    GiftEvent: Runs whenever a gift related event is ran
    GiftDetectEvent: Runs whenever a gift is detected
    GiftGiveEvent: Runs whenever a gift is given to Yuri
    GiftEquipEvent: Runs whenever a gift is put into the idle scene
    GiftUnequipEvent: Runs whenever a gift is taken out of the idle scene
    GiftActivateEvent: Runs whenever a gift that can be turned on is activated
    GiftDeactivateEvent: Runs whenever a gift that can be turned on is de-activated
    """

    class GiftEvent(Event):
        def __init__(self, gift):
            self.gift = gift

    class GiftDetectEvent(Event):
        def __init__(self, gift, file_location, given):
            super().__init__(self, gift)
            self.file_location = file_location
            self.given = given

    class GiftGiveEvent(Event):
        pass

    class GiftEquipEvent(Event):
        def __init__(self, gift, last_state):
            super().__init__(self, gift)
            self.last_state = last_state

    class GiftUnequipEvent(Event):
        def __init__(self, gift, last_state):
            super().__init__(self, gift)
            self.last_state = last_state

    class GiftActivateEvent(Event):
        def __init__(self, gift, last_state):
            super().__init__(self, gift)
            self.last_state = last_state

    class GiftDeactivateEvent(Event):
        def __init__(self, gift, last_state):
            super().__init__(self, gift)
            self.last_state = last_state