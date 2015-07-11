import numpy
import math
import random


class Task:

    """docstring for Task"""

    def __init__(self, baseProfit, numberOfWorkers, skills):

        # Task features
        self.numberOfWorkers = numberOfWorkers
        self.skills = skills

        # Uber scenario
        self.startX = random.uniform(0, 1)
        self.startY = random.uniform(0, 1)

        self.endX = random.uniform(0, 1)
        self.endY = random.uniform(0, 1)

        self.baseProfit = dist = math.hypot(
            self.endX - self.startX, self.endY - self.startY)

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

        bestAnswer = filter(lambda x: x.worker.pickupQuality == max(
            map(lambda x: x.worker.pickupQuality, self.answers)), self.answers)

        cost = bestAnswer[0].worker.currentBid.amount + \
            sum(map(lambda x: x.worker.getPartialCost(), filter(
                lambda x: x.worker != bestAnswer[0].worker, selectedWorkerBids)))

        return cost

    def getAverageMoneySpent(self):
        cost = 0
        bidsReceived = self.bids
        selectedWorkerBids = filter(
            lambda x: x.worker in map(lambda y: y.worker, self.answers), bidsReceived)

        bestAnswer = filter(lambda x: x.quality == max(
            map(lambda x: x.quality, self.answers)), self.answers)

        cost = bestAnswer[0].worker.currentBid.amount + \
            sum(map(lambda x: x.worker.getPartialCost(), filter(
                lambda x: x.worker != bestAnswer[0].worker, selectedWorkerBids)))

        return cost

    def getQuality(self):
        bestAnswer = filter(lambda x: x.worker.pickupQuality == max(
            map(lambda x: x.worker.pickupQuality, self.answers)), self.answers)

        return bestAnswer[0].quality

    def getObservedQuality(self):
        quality = sum(self.observedQualities) / \
            len(self.observedQualities)

        return quality
