import numpy


class Task:

    """docstring for Task"""

    def __init__(self, baseProfit, numberOfWorkers, skills):

        # Task features
        self.baseProfit = baseProfit
        self.numberOfWorkers = numberOfWorkers
        self.skills = skills

        # Task status
        self.workers = 0
        self.numberOfBids = 0
        self.answers = []
        self.bids = []
        self.observedQualities = []

    def execute(self, answer):
        self.answers.append(answer)
        self.workers += 1

    def receiveBid(self, bid):
        self.numberOfBids += 1
        self.bids.append(bid)

    def getMoneySpent(self):
        cost = 0
        bidsReceived = self.bids
        selectedWorkerBids = filter(
            lambda x: x.worker in map(lambda y: y.worker, self.answers), bidsReceived)

        cost = sum(map(lambda x: x.amount, selectedWorkerBids))

        return cost

    def getAverageMoneySpent(self):
        cost = 0
        bidsReceived = self.bids
        selectedWorkerBids = filter(
            lambda x: x.worker in map(lambda y: y.worker, self.answers), bidsReceived)

        cost = sum(map(lambda x: x.amount, selectedWorkerBids)) / \
            len(selectedWorkerBids)

        return cost

    def getQuality(self):
        quality = sum(map(lambda x: x.quality, self.answers)) / \
            len(self.answers)

        return quality

    def getObservedQuality(self):
        quality = sum(self.observedQualities) / \
            len(self.observedQualities)

        return quality
