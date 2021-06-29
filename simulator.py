# Monte Carlo simulation based on https://www.investopedia.com/terms/m/montecarlosimulation.asp

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics as stat
from scipy.stats import norm
import math

# number of days to predict
numDays = 50

# number of monte carlo simulations
numProjections = 50

# True: averages all the projections together
# False: shows all the projections
showAverageProjection = False

# Parse the Date and Closing price from the .csv file
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

# Days from the start date of the data
date2 = np.arange(0, len(date), 1)

# Figure title and axis labels
plt.figure(figsize=(12, 7))
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
    dayPrice = closingPrice.copy()
    for i in range(numDays+1):
        averageApproxValues = []
        # Calculated periodic daily return for each day including the new predicted days
        div = []
        for j in range(1, len(dayPrice)):
            div.append(dayPrice[j]/dayPrice[j-1])
        periodicDailyReturn = np.log(div)

        # Drift is based on average periodic daily return and its variance
        drift = np.average(periodicDailyReturn) - \
            (stat.variance(periodicDailyReturn)/2)

        # random factor invloved
        randomVal = stat.stdev(periodicDailyReturn) * \
            norm.ppf(np.random.rand())

        nextPrice = dayPrice[-1] * math.exp(drift + randomVal)

        # Calculate the next predicted value and add the value list
        dayPrice.append(nextPrice)

    # Only return the new predicted values
    return dayPrice[len(dayPrice)-numDays-1:]


# The future days used for the x axis of the projections
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
