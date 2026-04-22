init python:
    """
    Event List
    karma: Runs whenever karma changes
    sanity: Runs whenever sanity changes
    idle: Runs when Yuri returns to her idle state
    talk_greeting: Runs when Yuri is about to greet the player
    talk_idle: Runs when Yuri is about to say an idle
    talk_topic: Runs when Yuri is about to talk to the player about a topic
    """
    # Fires anytime Yuri's karma changes
    class KarmaEvent(Event):
        def __init__(self, karma, resulting_karma, is_setting_karma):
            self.karma = karma
            self.resulting_karma = resulting_karma
            self.is_setting_karma = is_setting_karma

    # Fires anytime Yuri's sanity changes
    class SanityEvent(Event):
        def __init__(self, sanity, resulting_sanity, is_setting_sanity):
            self.sanity = sanity
            self.resulting_sanity = resulting_sanity
            self.is_setting_sanity = is_setting_sanity

    EventAPI.register(KarmaEvent)
    EventAPI.register(SanityEvent)