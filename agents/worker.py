import numpy
import math
from scipy import spatial
from numpy.linalg import norm

from objects.bid import Bid
from objects.answer import Answer


class Worker:

    """docstring for Worker"""

    def __init__(self, name, mean, variance, slope, maxTasks, skills):

        # Worker features
        self.name = name
        self.maxTasks = maxTasks
        self.skills = skills

        # Evaluation error
        self.mean = mean
        self.variance = variance

        # Bid to effort function
        self.slope = slope

        # Worker current status
        self.currentBid = None
        self.currentTask = None

        # Worker status
        self.taskPerformed = 0
        self.taskBidded = 0
        self.bids = []
        self.profitDone = 0
        self.isBusy = False

    def estimateProfit(self, task):
        error = numpy.random.normal(self.mean, self.variance)
        estimatedProfit = task.baseProfit + error

        return estimatedProfit

    def bidTask(self, task):
        amount = self.estimateProfit(task)

        if amount < 0:
            amount = 1

        amount = 0.01 + 0.99 * amount

        bid = Bid(self, task, amount)
        self.taskBidded += 1
        self.bids.append(bid)
        self.currentBid = bid
        self.currentTask = task
        return bid

    def getEffort(self):
        return self.currentBid.amount * self.slope

    def performTask(self, task):
        self.isBusy = True
        workerSkills = self.skills

        dot = numpy.dot(workerSkills, task.skills)
        delta = abs(task.baseProfit - self.currentBid.amount)
        quality = (self.getEffort() * (dot)) / \
            (task.baseProfit + delta)
        #quality = (self.getEffort()) / task.baseProfit + dot / task.baseProfit

        answer = Answer(self, task, quality)
        task.execute(answer)
        self.taskPerformed += 1
        self.profitDone += self.currentBid.amount
        return answer
