init python:
    """
    Events
    DateEvent: Runs anytime a date related event is ran
    DateStartEvent: Runs when the player starts a date with Yuri
    DateEndEvent: Runs when the player completes or ends a date with Yuri
    DreamEvent: Runs anytime a dream related event is ran
    DreamStartEvent: Runs when the player starts a dream
    DreamEndEvent: Runs when the player completes or ends a dream
    """

    class DateEvent(Event):
        def __init__(self, label):
            self.label = str(label)
            self.original_label = str(label)

    class DateStartEvent(DateEvent):
        pass

    class DateEndEvent(DateEvent):
        def __init__(self, label, completed):
            super().__init__(self, label)
            self.completed = True

    class DreamEvent(Event):
        def __init__(self, label):
            self.label = str(label)
            self.original_label = str(label)

    class DreamStartEvent(DreamEvent):
        pass

    class DreamEndEvent(DreamEvent):
        def __init__(self, label, completed):
            super().__init__(self, label)
            self.completed = True