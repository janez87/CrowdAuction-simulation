import numpy as np
import random
import math

from objects.task import Task
from strategies.pickingStrategy import PickingStrategy


class Requester:

    """docstring for Requester"""

    def spawnTask(self, baseProfit, numberOfWorker, taskSkills):
        task = Task(baseProfit, numberOfWorker, taskSkills)
        self.tasks.append(task)
        return task

    def selectWinners(self, task, strategy):
        bids = task.bids

        pickingStrategy = PickingStrategy.strategies[int(strategy)]
        workers = pickingStrategy(self, bids, task)

        return workers

    def updateWorkerFunction(self, task):
        answers = task.answers

        #avgQuality = sum(a.quality for a in answers)
        #avgQuality = avgQuality / len(answers)

        maxQuality = 0
        observedQualities = []

        if(len(task.answers) == 1):
            comparableTasks = filter(
                lambda x: x.baseProfit == task.baseProfit, self.tasks)
            pastAnswers = [item for sublist in map(
                lambda x:x.answers, comparableTasks) for item in sublist]
            maxQuality = np.amax(map(lambda x: x.quality, pastAnswers))
        else:
            maxQuality = np.amax(map(lambda x: x.quality, answers))

        for a in answers:
            if self.workersTable.has_key(a.worker.name):
                self.workersTable[a.worker.name].append(
                    {"bid": a.worker.currentBid.amount, "quality": a.quality / maxQuality})
            else:
                self.workersTable[a.worker.name] = [
                    {"bid": a.worker.currentBid.amount, "quality": a.quality / maxQuality}]
            observedQualities.append(a.quality / maxQuality)

        task.observedQualities = observedQualities
        # print self.workersTable

    def __init__(self, budget):
        self.budget = budget
        self.workersTable = {}
        self.tasks = []
