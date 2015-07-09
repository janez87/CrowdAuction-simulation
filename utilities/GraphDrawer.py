import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def drawBarChart(data, configuration):

    plt.xlabel(configuration["xlabel"])
    plt.title(configuration["title"])

    ax = plt.subplot(111)
    bars = []
    for d in data:
        ax2 = ax.twinx()
        ax2.set_ylabel(configuration["bars"]["ylabel"])
        bar = ax.bar(numpy.arange(len(d["data"])), d["data"],  0.4, color='r', yerr=d[
                     "error"], align='center', error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))
        bars.append(bar)

      ax.legend((costBar[0], qualityBar[0]), ('Cost', 'Quality'))
    locs, ls = plt.xticks(numpy.arange(len(data)) + 0.4 / 2.,
                          map(lambda x: x["id"], data))
    plt.setp(ls, rotation=90)
    plt.savefig("results/AverageQualityAndCost.pdf")
    plt.close()


def drawScatterPlot(data, configuration):
    plt.scatter(range(0, len(timed)), timed)

    if(configuration["regressionLine"]):
        z = numpy.polyfit(range(0, len(timed)), timed, 1)
        p = numpy.poly1d(z)
        plt.plot(xrange(0, len(timed)), p(xrange(0, len(timed))), "-r")

    plt.ylabel(configuration["ylabel"])
    plt.xlabel(configuration["xlabel"])
    plt.title(configuration["title"])
    plt.savefig("results/" + configuration["name"])
    plt.close()
