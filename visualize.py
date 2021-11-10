import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# median housing price in the US
housing = pd.read_csv("./data/housing-natl.csv",
                      parse_dates=["Date"], index_col="Date")
housing_plt = (housing/1000).plot(
    legend=True, title="Housing Prices in the US (Thousands $)")
housing_plt.get_figure().savefig("./plots/housing.png")
housing_plt.remove()

# spy vs median housing price
spy = pd.read_csv("./data/spy-hist.csv",
                  parse_dates=["Date"], index_col="Date")

spy_housing = spy.merge(housing, how="left", on="Date").dropna()
spy_housing = spy_housing.reindex(index=spy_housing.index[::-1])
equity_mkt = [1.0]
housing_mkt = [1.0]
for i in range(len(spy_housing) - 1):
    equity_mkt.append(spy_housing["Price"][i+1] /
                      spy_housing["Price"][i] * equity_mkt[-1])
    housing_mkt.append(
        spy_housing["Median"][i+1] / spy_housing["Median"][i] * housing_mkt[-1])

spy_vs_housing = pd.DataFrame(
    {"SPY": equity_mkt, "Median House Value": housing_mkt}, index=spy_housing.index)

spy_plot = spy_vs_housing.plot(
    legend=True, title="$1 (USD) invested in each market")
spy_plot.get_figure().savefig("./plots/spy_vs_housing.png")
spy_plot.remove()

# interest rate vs housing price
interest = pd.read_csv("./data/interest-hist.csv",
                       parse_dates=["Date"], index_col="Date")
interest_housing = interest.merge(housing, how="left", on="Date").dropna()

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

ax1 = (interest_housing["Adjusted-Median"]/1000).plot(color='blue',
                                                      label='Inflation-Adjusted Median Price (1000s of USD)')
ax2 = interest_housing["FedFundsRate"].plot(
    color='orange', secondary_y=True, label='Federal Funds Rate')

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()

plt.legend(h1+h2, l1+l2, loc=2)
plt.savefig("./plots/interest_vs_housing.png")
plt.close()

hpi = pd.read_csv("./data/HPI_master.csv")
regions = hpi[(hpi["frequency"] == "monthly") &
              (hpi["place_name"] != "United States")].copy()
regions["Date"] = pd.to_datetime(
    regions["yr"].astype(str) + "-" + regions["period"].astype(str) + "-1")
fig, ax = plt.subplots(figsize=(8, 6))
for i, g in regions.groupby('place_name'):
    g.plot(x='Date', y='index_nsa', ax=ax, label=str(i))
plt.title("Housing Price Index (Unadjusted) by Region")
plt.ylabel("Index")
plt.savefig("./plots/regions.png")
plt.close()
