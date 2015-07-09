from agents.worker import Worker


class PerfectGuesser(Worker):

    """docstring for PerfectGuesser"""

    def __init__(self, name, maxTasks):
        Worker.super(self, name, 0, 0, maxTasks)

    def estimateProfit(self, task):
        self.taskBidded += 1
        return task.baseProfit
