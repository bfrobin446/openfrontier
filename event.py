import openfrontier

class WorldEvent:
    '''
    Base class for all scheduled events

    Important data members:
    -----------------------
    runAt
      Game time at which this event should be run. Events run once at a set
      time (events scheduled in the past run once at the first opportunity),
      then are discarded if not rescheduled.
    action
      Callable to run when the scheduled time is reached. Called without
      arguments. Use ``openfrontier.activeWorld`` to access the calling world
      object.
    '''

    def run(self):
        '''
        Perform this event's action.

        This implementation merely calls ``self.action``. Subclasses that wish
        to reschedule the same action at a later time should do so in
        ``run()``.
        '''
        self.action()

    def __init__(self, when=0, action=lambda:None):
        self.runAt = when
        self.action = action

    def __lt__(self, other):
        return self.runAt < other.runAt

    @classmethod
    def fromDOMElement(cls, element):
        eventType = element.getAttribute('type')
        if eventType == "once":
            import domhelpers
            runAt = int(
                    getInnerText(
                        getFirstChildElementWithTagName(element, 'runAt')))
            action = getattr(ofcampaign,
                    getInnerText(
                        getFirstChildElementWithTagName(element, 'action')))
            return cls(runAt, action)
        else:
            return eventClassForType[eventType].fromDOMElement(element)


class RegularEvent(WorldEvent):
    '''
    Event that schedules itself at a fixed interval.

    New data member:
    ----------------
    interval
      Number of game ticks between activations
    '''

    def __init__(self, interval, start=0, action=lambda:None):
        WorldEvent.__init__(self, start, action)
        self.interval = interval

    def run(self):
        self.action()
        self.runAt += self.interval
        openfrontier.activeWorld.addEvent(self)


eventClassForType = {
        'once':     WorldEvent,
        'interval': RegularEvent
        }
