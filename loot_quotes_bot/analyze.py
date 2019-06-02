#!/usr/bin/env python
# coding: utf-8

# ## Load modules

# In[ ]:


import sqlite3, os

import pandas as pd


# ## Initialize database

# In[ ]:


conn = sqlite3.connect("./loot.db")
c = conn.cursor()


# In[ ]:


c.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER, item_id INTEGER, price INTEGER, dt text)''')


# ## Cleaning transactions

# In[ ]:


transactions = pd.read_sql_query("SELECT * FROM transactions LIMIT 50000", conn)

transactions = transactions.merge(items[["estimate", "rarity", "value"]], left_on="item_id", right_index=True, how="left")
# Remove items sold at the base price except for C type items
transactions = transactions.query("(rarity == 'C' | price != value) & (rarity == 'U' | price < estimate*5)")
# Drop estimate and values columns
transactions.drop(columns=["estimate", "rarity", "value"], inplace=True)

# Set datetime as index
transactions.dt = pd.to_datetime(transactions.dt, format="%Y-%m-%dT%H:%M:%S.%fZ")

transactions.head()


# In[ ]:


# Resample transactions
resampled_transactions = transactions.drop(columns="id").groupby(by=["item_id"])
resampled_transactions


# In[ ]:


numerosity = resampled_transactions.count()
numerosity.rename(columns={"price":"numerosity"}, inplace=True)

numerosity.head()


# In[ ]:


mean = resampled_transactions.mean()
mean.rename(columns={"price":"mean"}, inplace=True)

mean.head()


# In[ ]:


std = resampled_transactions.std()
std.rename(columns={"price":"std"}, inplace=True)

std.head()


# In[ ]:


median = resampled_transactions.median()
median.rename(columns={"price":"median"}, inplace=True)

median.head()


# In[ ]:


max_price = resampled_transactions.max()
max_price.rename(columns={"price":"max_price"}, inplace=True)

max_price.head()


# In[ ]:


min_price = resampled_transactions.min()
min_price.rename(columns={"price":"min_price"}, inplace=True)

min_price.head()


# In[ ]:


quantile_25 = resampled_transactions.agg(lambda x: x.quantile(0.25))
quantile_25.rename(columns={"price":"quantile_25"}, inplace=True)

quantile_25.head()


# In[ ]:


quantile_75 = resampled_transactions.agg(lambda x: x.quantile(0.75))
quantile_75.rename(columns={"price":"quantile_75"}, inplace=True)

quantile_75.head()


# In[ ]:


items = items.merge(pd.concat([numerosity.numerosity, mean["mean"], std["std"], median["median"], max_price.max_price, min_price.min_price, quantile_25.quantile_25, quantile_75.quantile_75], axis=1), left_index=True, right_index=True, how="left")

items.head()


# ## Saving market prices to file

# In[ ]:


items.to_json("./data/market_prices.json", orient="records")


# ## Save items statistics to file

# In[ ]:


def save_row_to_csv(row):
    if os.path.isfile(f"./items/{row.name}.csv"):
        data = pd.read_csv(f"./items/{row.name}.csv")
    else:
        data = pd.DataFrame()
    
    data = data.append(row)
    data.to_csv(f"./items/{row.name}.csv", index=False)


# In[ ]:


items.apply(save_row_to_csv, axis=1)


# In[ ]:


conn.close()


# In[ ]:




