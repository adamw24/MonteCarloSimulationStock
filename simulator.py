import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics as stat
from scipy.stats import norm
import math

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

fig, ax = plt.subplots()

# fig.autofmt_xdate()
# fmt_half_year = mdates.MonthLocator(interval=1)
# fmt_month = mdates.WeekdayLocator()
# ax.xaxis.set_minor_locator(fmt_month)
# ax.xaxis.set_major_locator(fmt_half_year)


def monteCarlo(values, numDays):
    newValues = []
    for i in range(numDays+1):
        randomVal = stat.stdev(periodicDailyReturn) * \
            norm.ppf(np.random.rand())
        if i == 0:
            nextPrice = values[-1]
        else:
            nextPrice = newValues[-1]
        nextPrice *= math.exp(drift + randomVal)
        newValues.append(nextPrice)
    return newValues


numDays = 50
numSimulations = 50

showAveragePrediction = False

approxDates = np.arange(date2[-1], date2[-1]+numDays + 1, 1)
averageApproxValues = []

dayPrice = closingPrice.copy()
dayPrice.insert(0, 0)
div = [i / j for i, j in zip(dayPrice, closingPrice)]
div = div[1:]
periodicDailyReturn = np.log(div)
drift = np.average(periodicDailyReturn) - \
    (stat.variance(periodicDailyReturn)/2)

for i in range(numSimulations+1):
    approxValue = monteCarlo(closingPrice.copy(), numDays)
    if showAveragePrediction:
        if i == 0:
            averageApproxValues = approxValue
        else:
            averageApproxValues = [i + j for i,
                                   j in zip(averageApproxValues, approxValue)]
    else:
        plt.plot(approxDates, approxValue)

if showAveragePrediction:
    averageApproxValues = [x/(numSimulations+1) for x in averageApproxValues]
    plt.plot(approxDates, averageApproxValues)

plt.plot(date2, closingPrice)
plt.show()
