import heapq
import os.path

from pickle import Unpickler

import openfrontier

class OFWorld:
    '''
    OpenFrontier global data and galaxy-scale processing.

    Important data members
    ----------------------
    time
      Counter incremented at each time-step (``tick()``)
    activeFleets
      Iterable containing fleets that are not in a system, port, or
      encounter
    systems
      Dict of star systems making up the game world
    deepSpaceEncounters
      Iterable of encounters: short-lived containers for fleets that are
      interacting
    worldEvents
      Queue of events in order of scheduled activation time.
    '''
    def tick(self):
        '''
        Entry point for OpenFrontier world time-step.

        Operations performed:
        * Increment global time
        * Call ``tick()`` on each fleet and solar system
        * Run any world events scheduled at or before the current time
        '''
        self.time += 1
        for f in self.activeFleets:
            f.tick()
        for s in self.systems.values:
            s.tick()
        for e in self.deepSpaceEncounters:
            e.tick()
        while self.worldEvents[0].runAt <= self.time:
            evt = heappop(self.worldEvents)
            evt.run()


def fromFile(worldDir):
    '''Load a world object from a campaign bundle'''
    pickleFileName = os.path.join(worldDir, 'data.pickle')
    pickle = Unpickler(open(pickleFileName, 'rb'))
    fileVersion = pickle.load()
    if fileVersion != openfrontier.PICKLE_VERSION:
        raise TypeError(
                "Data version mismatch: expected {0}; got {1}.".format(
                    openfrontier.PICKLE_VERSION, fileVersion))
    world = pickle.load()
    if not isinstance(world, OFWorld):
        raise TypeError(
                "Expected OFWorld; got {0}".format(type(world).__name__))
    return world
