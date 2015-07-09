import numpy as np
import random


class PickingStrategy(object):

    @classmethod
    def cheapestWorkers(cls, requester, bids, task):
        workers = []
        bids = sorted(
            bids, key=lambda x: (x.amount))
        totalCost = 0
        for b in bids:
            if len(workers) < task.numberOfWorkers and totalCost < requester.budget:
                workers.append(b.worker)
                totalCost = totalCost + b.amount
            else:
                break

        return workers

    @classmethod
    def mostExpensiveWorkers(cls, requester, bids, task):
        workers = []
        bids = sorted(
            bids, key=lambda x: (x.amount), reverse=True)
        totalCost = 0
        for b in bids:
            if len(workers) < task.numberOfWorkers and totalCost < requester.budget:
                workers.append(b.worker)
                totalCost = totalCost + b.amount
            else:
                break
        return workers

    @classmethod
    def randomWorkers(cls, requester, bids, task):
        workers = []
        random.shuffle(bids)
        totalCost = 0
        for b in bids:
            if len(workers) < task.numberOfWorkers and totalCost < requester.budget:
                workers.append(b.worker)
                totalCost = totalCost + b.amount
            else:
                break
        return workers

    @classmethod
    def bestWorkers(cls, requester, bids, task):
        candidates = []
        workers = []

        if(requester.workersTable == {}):
            workers = PickingStrategy.nearestAverage(
                requester, bids, task)
            return workers

        # Compute the slope
        for bid in bids:
            if(requester.workersTable.has_key(bid.worker.name)):
                oldWorker = requester.workersTable[bid.worker.name]
                slope, intercept = np.polyfit(
                    [0] + map(lambda x: x["bid"], oldWorker), [0] + map(lambda x: x["quality"], oldWorker), 1)

                pastQuality = sum(p["quality"]
                                  for p in oldWorker) / len(oldWorker)
                candidates.append({
                    "worker": bid.worker,
                    "slope": slope,
                    "intercept": intercept,
                    "pastQuality": pastQuality,
                    "expectedQuality": slope * bid.amount + intercept,
                    "amount": bid.amount
                })
            else:
                pass

        candidates = sorted(
            candidates, key=lambda x: (x["expectedQuality"]), reverse=True)

        totalCost = 0
        for x in xrange(0, task.numberOfWorkers):
            if x == len(candidates):
                break
            if candidates[x]["expectedQuality"] >= 0 and totalCost < requester.budget:
                workers.append(candidates[x]["worker"])
                totalCost = totalCost + candidates[x]["amount"]
            else:
                break

        # if len(workers) < task.numberOfWorkers:
        #     bids = sorted(
        #         bids, key=lambda x: (x.amount))
        #     for b in bids:
        #         if len(workers) == task.numberOfWorkers or totalCost >= requester.budget:
        #             break
        #         if b.worker not in workers:
        #             workers.append(b.worker)
        #             totalCost = totalCost + b.amount

        if len(workers) < task.numberOfWorkers:
            deltas = map(
                lambda x: {"delta": abs(task.baseProfit - x.amount), "worker": x.worker, "amount": x.amount}, bids)
            deltas = sorted(
                deltas, key=lambda x: x["delta"])
            for d in deltas:
                if len(workers) < task.numberOfWorkers and totalCost < requester.budget:
                    if d["worker"] not in workers:
                        workers.append(d["worker"])
                        totalCost = totalCost + d["amount"]
                else:
                    break
        return workers

    @classmethod
    def nearestCheapest(cls, requester, bids, task):
        workers = []
        filteredBids = filter(lambda x: x.amount <= task.baseProfit, bids)
        filteredBids = sorted(
            filteredBids, key=lambda x: (x.amount), reverse=True)
        totalCost = 0
        for b in filteredBids:
            if len(workers) < task.numberOfWorkers and totalCost < requester.budget:
                workers.append(b.worker)
                totalCost = totalCost + b.amount
            else:
                break

        if len(workers) < task.numberOfWorkers:
            bids = sorted(bids, key=lambda x: (x.amount))
            for b in bids:
                if len(workers) == task.numberOfWorkers or totalCost >= requester.budget:
                    break
                if b.worker not in workers:
                    workers.append(b.worker)
                    totalCost = totalCost + b.amount

        return workers

    @classmethod
    def nearestExpensive(cls, requester, bids, task):
        workers = []
        filteredBids = filter(lambda x: x.amount >= task.baseProfit, bids)
        filteredBids = sorted(
            filteredBids, key=lambda x: (x.amount))
        totalCost = 0
        for b in filteredBids:
            if len(workers) < task.numberOfWorkers and totalCost < requester.budget:
                workers.append(b.worker)
                totalCost = totalCost + b.amount
            else:
                break

        if len(workers) < task.numberOfWorkers:
            bids = sorted(
                bids, key=lambda x: (x.amount))

            for b in bids:
                if len(workers) == task.numberOfWorkers or totalCost >= requester.budget:
                    break
                if b.worker not in workers:
                    workers.append(b.worker)
                    totalCost = totalCost + b.amount

        return workers

    @classmethod
    def nearestAverage(cls, requester, bids, task):
        workers = []
        deltas = map(
            lambda x: {"delta": abs(task.baseProfit - x.amount), "worker": x.worker, "amount": x.amount}, bids)
        deltas = sorted(
            deltas, key=lambda x: x["delta"])
        totalCost = 0
        for d in deltas:
            if len(workers) < task.numberOfWorkers and totalCost < requester.budget:
                workers.append(d["worker"])
                totalCost = totalCost + d["amount"]
            else:
                break

        if len(workers) < task.numberOfWorkers:
            bids = sorted(
                bids, key=lambda x: (x.amount))
            for b in bids:
                if len(workers) == task.numberOfWorkers or totalCost >= requester.budget:
                    break
                if b.worker not in workers:
                    workers.append(b.worker)
                    totalCost = totalCost + b.amount

        return workers

PickingStrategy.strategies = {
    1: PickingStrategy.randomWorkers,
    2: PickingStrategy.mostExpensiveWorkers,
    3: PickingStrategy.cheapestWorkers,
    4: PickingStrategy.bestWorkers,
    5: PickingStrategy.nearestCheapest,
    6: PickingStrategy.nearestExpensive,
    7: PickingStrategy.nearestAverage
}
