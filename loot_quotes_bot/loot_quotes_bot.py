# ## Load modules
import os, requests, json, ftplib
import pandas as pd


# ## Load private settings
from private_settings import *

# ## Define working directory
os.chdir(PATH)


# ## Define constants
NO_TRANSACTIONS = 1000


# # Request items
url = "http://fenixweb.net:3300/api/v2/"+API_TOKEN+"/items"
response = json.loads(requests.get(url).text)

assert response["code"] == 200, "Connection error."

# Load json into dataframe
items = pd.DataFrame(response["res"])

# Set id as index
items.set_index("id", inplace=True)

items["datetime"] = pd.to_datetime("now")
items["interval"] = 2


# ## Save items to file
items.to_csv("data/items.csv")


# # Request market transactions

url = "http://fenixweb.net:3300/api/v2/"+API_TOKEN+"/history/market_direct?limit="+str(NO_TRANSACTIONS)
response = json.loads(requests.get(url).text)

assert response["code"] == 200, "Connection error."

transactions = pd.DataFrame(response["res"])
transactions.drop(columns=["buyer", "from_nick", "id", "name", "to_nick", "type"], inplace=True)


# # Cleaning transactions
#TODO: Develop cleaning process
# Remove items sold at the base price except for C type items & remove items with price over 5 times the estimate except for U type
transactions = transactions.merge(items[["estimate", "rarity", "value"]], left_on="item_id", right_index=True, how="left")
transactions = transactions.query("rarity != 'C' | price != value")
transactions = transactions.query("rarity != 'U' | price < estimate*5")

# Drop estimate and values columns
transactions.drop(columns=["estimate", "rarity", "value"], inplace=True)

# Set datetime as index
transactions.time = pd.to_datetime(transactions.time, format="%Y-%m-%dT%H:%M:%S.%fZ")
transactions.set_index("time", inplace=True)


# Resample transactions
resampled_transactions = transactions.groupby(by=["item_id"]).resample("2D")
#resampled_transactions.drop(columns="item_id", inplace=True)


# TODO: optimize
numerosity = resampled_transactions.count()
numerosity.rename(columns={"price":"numerosity"}, inplace=True)
numerosity.drop(columns="item_id", inplace=True)
numerosity = numerosity.groupby(level=0).tail(1)
numerosity.index = numerosity.index.droplevel("time")


mean = resampled_transactions.mean()
mean.rename(columns={"price":"mean"}, inplace=True)
mean.drop(columns="item_id", inplace=True)
mean = mean.groupby(level=0).tail(1)
mean.index = mean.index.droplevel("time")
mean = mean.groupby(level=0).tail(1)


std = resampled_transactions.std()
std.rename(columns={"price":"std"}, inplace=True)
std.drop(columns="item_id", inplace=True)
std = std.groupby(level=0).tail(1)
std.index = std.index.droplevel("time")
std = std.groupby(level=0).tail(1)


median = resampled_transactions.median()
median.rename(columns={"price":"median"}, inplace=True)
median.drop(columns="item_id", inplace=True)
median = median.groupby(level=0).tail(1)
median.index = median.index.droplevel("time")
median = median.groupby(level=0).tail(1)


max_price = resampled_transactions.max()
max_price.rename(columns={"price":"max"}, inplace=True)
max_price.drop(columns="item_id", inplace=True)
max_price = max_price.groupby(level=0).tail(1)
max_price.index = max_price.index.droplevel("time")
max_price = max_price.groupby(level=0).tail(1)


min_price = resampled_transactions.min()
min_price.rename(columns={"price":"min"}, inplace=True)
min_price.drop(columns="item_id", inplace=True)
min_price = min_price.groupby(level=0).tail(1)
min_price.index = min_price.index.droplevel("time")
min_price = min_price.groupby(level=0).tail(1)


quantile_25 = resampled_transactions.agg(lambda x: x.quantile(0.25))
quantile_25.rename(columns={"price":"quantile_25"}, inplace=True)
quantile_25.drop(columns="item_id", inplace=True)
quantile_25 = quantile_25.groupby(level=0).tail(1)
quantile_25.index = quantile_25.index.droplevel("time")
quantile_25 = quantile_25.groupby(level=0).tail(1)


quantile_75 = resampled_transactions.agg(lambda x: x.quantile(0.75))
quantile_75.rename(columns={"price":"quantile_75"}, inplace=True)
quantile_75.drop(columns="item_id", inplace=True)
quantile_75 = quantile_75.groupby(level=0).tail(1)
quantile_75.index = quantile_75.index.droplevel("time")
quantile_75 = quantile_75.groupby(level=0).tail(1)


items = items.merge(pd.concat([numerosity, mean, std, median, max_price, min_price, quantile_25, quantile_75], axis=1), left_index=True, right_index=True, how="left")
items.reset_index(inplace=True)

# ## Saving market prices to file
items.to_json("data/market_prices.json", orient="records")


# ## Save items statistics to file
def save_row_to_csv(row):
    if os.path.isfile("items/"+str(row.name)+".csv"):
        data = pd.read_csv("items/"+str(row.name)+".csv")
    else:
        data = pd.DataFrame()
    
    data = data.append(row)
    data.to_csv("items/"+str(row.name)+".csv", index=False)


items.apply(save_row_to_csv, axis=1)
