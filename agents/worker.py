import numpy
import math
import random
import json
from scipy import spatial
from numpy.linalg import norm

from objects.bid import Bid
from objects.answer import Answer

configuration = json.load(open('configuration/configuration.json'))


class Worker:

    """docstring for Worker"""

    def __init__(self, name, mean, variance, slope, maxTasks, skills):

        # Worker features
        self.name = name
        self.maxTasks = maxTasks
        self.skills = skills

        # Uber Scenario
        self.x = random.uniform(0, 1)
        self.y = random.uniform(0, 1)
        self.efficiency = random.uniform(2, 5)
        self.currentDistance = 0

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
        error = math.hypot(task.startX - self.x, task.startY - self.y)

        estimatedProfit = (task.baseProfit + error) * self.efficiency
        self.currentDistance = error

        return estimatedProfit

    def bidTask(self, task):
        amount = self.estimateProfit(task)

        bid = Bid(self, task, amount)
        self.taskBidded += 1
        self.bids.append(bid)
        self.currentBid = bid
        self.currentTask = task
        return bid

    def getEffort(self):
        return self.slope

    def getPartialCost(self):
        return self.currentDistance * self.efficiency

    def performTask(self, task):
        self.isBusy = True
        workerSkills = self.skills

        dot = numpy.dot(workerSkills, task.skills)
        driveQuality = (self.getEffort() * (dot)) / \
            (task.baseProfit)

        pickupQuality = (self.getEffort() * (dot)) / \
            (self.currentDistance)

        quality = pickupQuality + driveQuality

        dice = random.random()
        if dice < configuration["incidents"]:
            quality = 0
            pickupQuality = 0
            driveQuality = 0

        self.pickupQuality = pickupQuality
        self.driveQuality = driveQuality

        answer = Answer(self, task, quality)
        task.execute(answer)
        self.taskPerformed += 1
        self.profitDone += self.currentBid.amount

        # Move the worker to the new location
        self.x = task.endX
        self.y = task.endY

        return answer
