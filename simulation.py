import random
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import math
import json
import numpy
import sys
import csv

from agents.requester import Requester
from agents.worker import Worker
from objects.task import Task
from strategies.strategy import Strategy

print "Loading the configuration"
configuration = json.load(open('configuration/configuration.json'))

runnedSimulations = []
csvList = []


taskSkills = []
while True:
    for x in xrange(1, configuration["numberOfSkills"]):
        coin = random.randint(1, 2)
        if(coin == 1):
            taskSkills.append(random.uniform(0, 1))
        else:
            taskSkills.append(0)
    if sum(taskSkills) > 0:
        break
    taskSkills = []

for s in configuration["simulations"]:

    simulationStats = {}
    simulationStats["id"] = s["id"]
    simulationStats["timedStats"] = []

    simulationStats["avgQuality"] = []
    simulationStats["stdQuality"] = []
    simulationStats["avgCost"] = []
    simulationStats["stdCost"] = []

    for i in range(1, configuration["numberOfRuns"] + 1):
        print "Simulation: " + s["id"] + " run: " + str(i)
        print "Creating workers"
        workers = []

        numberOfWorkers = configuration["workerConfiguration"]["number"]
        print "Creating " + str(numberOfWorkers) + " randomized workers"
        for i in xrange(0, numberOfWorkers):
            meanError = random.uniform(configuration["workerConfiguration"]["meanRange"][
                0], configuration["workerConfiguration"]["meanRange"][1])
            variance = random.uniform(configuration["workerConfiguration"]["varianceRange"][
                0], configuration["workerConfiguration"]["varianceRange"][1])
            slope = random.uniform(configuration["workerConfiguration"]["slopeRange"][
                0], configuration["workerConfiguration"]["slopeRange"][1])
            numberOfTask = random.randint(configuration["workerConfiguration"]["numberOfTasksRange"][
                0], configuration["workerConfiguration"]["numberOfTasksRange"][1])

            skills = []
            for x in xrange(1, configuration["numberOfSkills"]):
                skills.append(random.randint(0, 1))

            workers.append(
                Worker(str(i), meanError, variance, slope, numberOfTask, skills))

        print "Creating fixed " + str(len(configuration["workers"])) + " workers (if any)"

        for x in configuration["workers"]:
            workers.append(Worker(
                x["name"], x["mean"], x["variance"], x["slope"], x["numberOfTask"]))

        print "Creating the requester"
        req = Requester(s["requesterConfiguration"]["budget"])

        tasks = []
        print "Creating the fixed tasks (if any)"
        for x in s["tasks"]:
            tasks.append(Task(x["baseProfit"], x["numberOfWorkers"]))

        numberOfTasks = s["tasksConfiguration"]["number"]
        print "Creating " + str(numberOfTasks) + " randomized tasks"

        for x in xrange(0, numberOfTasks):

            baseProfit = random.randint(s["tasksConfiguration"][
                                        "baseProfitRange"][0], s["tasksConfiguration"]["baseProfitRange"][1])
            numberOfWorkers = random.randint(s["tasksConfiguration"][
                "numberOfWorkersRange"][0], s["tasksConfiguration"]["numberOfWorkersRange"][1])
            tasks.append(
                req.spawnTask(baseProfit, numberOfWorkers, taskSkills))

        for task in tasks:

            # print "Begin auction"
            notBusyWokers = filter(lambda x: not x.isBusy, workers)
            biddingWorkers = []
            for w in notBusyWokers:
                coin = random.randint(1, 2)
                if(coin == 1):
                    biddingWorkers.append(w)

            for w in workers:
                w.isBusy = False

            bids = []
            for x in xrange(0, len(biddingWorkers)):
                if(numpy.dot(biddingWorkers[x].skills, task.skills) > 0):
                    bid = biddingWorkers[x].bidTask(task)
                    if bid != None:
                        bids.append(bid.amount)

            winners = req.selectWinners(
                task, Strategy[s["requesterConfiguration"]["strategy"]])

            for w in winners:
                w.performTask(task)

            req.updateWorkerFunction(task)

        data = []

        k = 1
        for task in tasks:
            data.append(task.getQuality() / task.getMoneySpent())
            csvList.append([
                s["id"],
                i,
                k,
                task.getObservedQuality(),
                task.getQuality(),
                task.getMoneySpent(),
                task.getAverageMoneySpent()
            ])
            k = k + 1

        with open('./results/data.csv', 'a') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerows(csvList)

        csvList = []

        qualities = map(lambda x: x.getQuality(), tasks)
        costs = map(lambda x: x.getMoneySpent(), tasks)

        simulationStats["timedStats"].append(data)

        simulationStats["avgQuality"].append(numpy.mean(qualities))
        simulationStats["stdQuality"].append(numpy.std(qualities))

        simulationStats["avgCost"].append(numpy.mean(costs))
        simulationStats["stdCost"].append(numpy.std(costs))

####### END OF THE RUNS OF SINGLE CONFIGURATION ##########################

    simulationStats["stdQuality"] = numpy.std(
        simulationStats[
            "avgQuality"])
    simulationStats["avgQuality"] = numpy.mean(simulationStats[
        "avgQuality"])

    simulationStats["stdCost"] = numpy.std(
        simulationStats["stdCost"])
    simulationStats["avgCost"] = numpy.mean(simulationStats[
        "avgCost"])

    runnedSimulations.append(simulationStats)

    timed = []

    for k in range(0, len(simulationStats["timedStats"][0])):
        istantData = 0
        for j in range(0, len(simulationStats["timedStats"])):
            d = simulationStats["timedStats"][j][k]
            istantData = istantData + d
        istantData = istantData / len(simulationStats["timedStats"])
        timed.append(istantData)

    # Data Analysis

    plt.scatter(range(0, len(timed)), timed)

    z = numpy.polyfit(range(0, len(timed)), timed, 1)
    p = numpy.poly1d(z)

    plt.ylabel('Quality / Cost')
    plt.xlabel('Tasks')
    plt.title(s["id"] + ' Quality / Cost by Task')
    plt.plot(xrange(0, len(timed)), p(xrange(0, len(timed))), "-r")
    plt.savefig("results/" + s["id"] + "_QualityOverCostByTime.pdf")
    plt.close()

##########################################################################

means = []
for i in xrange(0, len(runnedSimulations)):
    means.append(
        runnedSimulations[i]["avgQuality"] / runnedSimulations[i]["avgCost"])


ax = plt.subplot(111)
ax.bar(numpy.arange(len(runnedSimulations)), means,  0.5)
locs, labels = plt.xticks(numpy.arange(len(runnedSimulations)) + 0.5 / 2)
# plt.setp(labels, rotation=90, font=10)
ax.set_xticklabels(
    map(lambda x: x["id"], runnedSimulations), rotation="vertical", fontsize=10)
plt.ylabel('Quality / Cost')
plt.title('Average Quality / Cost')
plt.savefig("results/AverageQualityOverCost.pdf")
# plt.gca().tight_layout()
plt.close()

ax = plt.subplot(111)
x = map(lambda x: x["id"], runnedSimulations)
ax.set_ylabel('Average Cost')
plt.title('Average Cost and Quality')
ax2 = ax.twinx()
ax2.set_ylabel('Average Quality')
costBar = ax.bar(numpy.arange(len(x)) - 0.5, map(
    lambda x: x["avgCost"], runnedSimulations),  0.4, color='r', yerr=map(lambda x: x["stdCost"], runnedSimulations), align='center', error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))

qualityBar = ax2.bar(numpy.arange(len(x)), map(
    lambda x: x["avgQuality"], runnedSimulations),  0.4, color='b', yerr=map(lambda x: x["stdQuality"], runnedSimulations), align='center', error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))

locs, ls = plt.xticks(numpy.arange(len(runnedSimulations)) - 0.5 / 2)
# plt.setp(ls, rotation=90)
ax.set_xticklabels(
    map(lambda x: x["id"], runnedSimulations), rotation="vertical", fontsize=10)
ax.legend((costBar[0], qualityBar[0]), ('Cost', 'Quality'))
# plt.gca().tight_layout()
plt.savefig("results/AverageQualityAndCost.pdf")
plt.close()

sys.exit(0)
