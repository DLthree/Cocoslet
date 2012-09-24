import greenlet
import cocos
import traceback

VERBOSE = False

# @TODO implement something like sleep_until(event/animation is done)!
class Cocoslet(cocos.cocosnode.CocosNode):
    def __init__(self, owner, interval=None):
        super(Cocoslet, self).__init__()
        self.owner = owner
        self.interval = interval

    def sleep(self, seconds):
        if VERBOSE: print "sleep", seconds
        assert seconds > 0
        self.unschedule(self.tick)
        self.schedule_interval(self.tick, seconds, reset=True)
        self.g.parent.switch()

    def start(self):
        # we start new Greenlets through the cocos scheduler,
        # so that they all (hopefully) have the same parent Greenlet
        self.owner.add(self)
        self.schedule_once(self.delayed_start)

    def reset_timer(self):
        if VERBOSE: print "resetting timer"
        self.unschedule(self.tick)
        if self.interval:
            self.schedule_interval(self.tick, self.interval)
        else:
            self.schedule(self.tick)

    def delayed_start(self, dt):
        self.reset_timer()
        self.g = greenlet.greenlet(self.run)

    def finish(self):
        if VERBOSE: print "finish"
        self.owner.remove(self)
        self.g = None
        self.unschedule(self.tick)

    def tick(self, dt, reset=False):
        if VERBOSE: print "tick"
        if reset:
            self.reset_timer()
        try:
            self.g.switch()
        except:
            traceback.print_exc()
            self.finish()
            return
        if self.g.dead:
            self.finish()
                

