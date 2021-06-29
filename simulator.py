import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics as stat
from scipy.stats import norm
import math


numDays = 200
numProjections = 5
showAverageProjection = True

closingPrice = []
date = []
with open('SPY.csv', newline="\n") as f:
    reader = csv.reader(f)
    for row in reader:
        closingPrice.append(row[5])
        date.append(row[0])

closingPrice = closingPrice[1:]
closingPrice = list(map(float, closingPrice))
date = date[1:]
date2 = np.arange(0, len(date), 1)
# print(date)
# print(closingPrice)

# fig, ax = plt.subplots()
plt.figure(figsize=(10, 7))
plt.ylabel("Value (US Dollars)")
plt.xlabel("Days since " + date[1])
plt.title("Monte Carlo Simulation of SPDR S&P 500 ETF over a %d day period using %d projections" % (
    numDays, numProjections))
plt.minorticks_on()

# fig.autofmt_xdate()
# fmt_half_year = mdates.MonthLocator(interval=1)
# fmt_month = mdates.WeekdayLocator()
# ax.xaxis.set_minor_locator(fmt_month)
# ax.xaxis.set_major_locator(fmt_half_year)


def monteCarlo(values, numDays):
    newValues = []
    dayPrice = closingPrice.copy()
    for i in range(numDays+1):
        averageApproxValues = []

        div = []
        for j in range(1, len(dayPrice)):
            div.append(dayPrice[j]/dayPrice[j-1])

        # dayPrice.insert(0, 0)
        # div = [i / j for i, j in zip(dayPrice, closingPrice)]
        # div = div[1:-1]
        periodicDailyReturn = np.log(div)
        drift = np.average(periodicDailyReturn) - \
            (stat.variance(periodicDailyReturn)/2)
        randomVal = stat.stdev(periodicDailyReturn) * \
            norm.ppf(np.random.rand())
        if i == 0:
            nextPrice = values[-1]
        else:
            nextPrice = newValues[-1]
        nextPrice *= math.exp(drift + randomVal)
        newValues.append(nextPrice)
        dayPrice.append(nextPrice)

    return newValues


approxDates = np.arange(date2[-1], date2[-1]+numDays + 1, 1)

for i in range(numProjections):
    approxValue = monteCarlo(closingPrice.copy(), numDays)
    if showAverageProjection:
        if i == 0:
            averageApproxValues = approxValue
        else:
            for i in range(len(averageApproxValues)):
                averageApproxValues[i] += approxValue[i]
    else:
        plt.plot(approxDates, approxValue)

if showAverageProjection:
    plt.plot(approxDates, [x/numProjections for x in averageApproxValues])

givenData, = plt.plot(date2, closingPrice)
plt.legend([givenData], ["Closing value from " + date[1] + " to " + date[-1]])

plt.show()
