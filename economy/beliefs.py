import random


from .offer import MIN_PRICE


class Beliefs(object):
    def __init__(self):
        self._beliefs = {}

    def choose_price(self, good):
        belief, confidence = self.get_belief(good)

        return round(belief + confidence * self.interval_factor())

    def get_belief(self, good):
        try:
            return self._beliefs[good]
        except KeyError:
            belief = random.randint(10, 20)
            confidence = random.randint(5, 10)

            self._beliefs[good] = [belief, confidence]

            return [belief, confidence]

    def update(self, good, clearing_price, successful=True):
        belief, confidence = self.get_belief(good)

        if successful:
            # A successful trade means we're more confident now in our beliefs
            confidence *= 0.9
        else:
            # Our price wasn't good enough; shift our belief
            belief = (belief + clearing_price)/2
            # Also, our confidence is shaken by our failure
            confidence /= 0.9

        # TODO: Ensure our beliefs won't result in negative prices... somehow

        self._beliefs[good] = [belief, confidence]

    def interval_factor(self):
        return random.random() * 2 - 1
