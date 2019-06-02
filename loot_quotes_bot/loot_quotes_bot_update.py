#!/usr/bin/env python
# coding: utf-8

# ## Load modules

# In[ ]:


import sqlite3
import json

import requests
import pandas as pd


# ## Load API token

# In[ ]:


with open("./api.key", "r") as f:
    token = f.read().strip()


# ## Initialize database

# In[ ]:


conn = sqlite3.connect("./loot.db")
c = conn.cursor()


# In[ ]:


c.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER, item_id INTEGER, price INTEGER, dt text)''')


# In[ ]:


url = f"https://fenixweb.net:6600/api/v2/{token}/items"
r = requests.get(url)
assert r.status_code == 200, "Connection error."

j = json.loads(r.text)
assert j["code"] == 200, f"Errore {j['code']}: {j['error']}"

# Load json into dataframe
items = pd.DataFrame(j["res"])
items.set_index("id", inplace=True)

items.head()


# ## Save items to file

# In[ ]:


items.to_csv("./data/items.csv")


# ## Update transactions database

# In[ ]:


i = 0
while(i <= 10): # Maximum offset is 10000
    r = requests.get(f"https://fenixweb.net:6600/api/v2/{token}/history/market_direct?limit=1000&offset={i*1000}")
    assert r.status_code == 200, "Connection error."

    j = json.loads(r.text)
    assert j["code"] == 200, f"Errore {j['code']}: {j['error']}"

    transactions = pd.DataFrame(j["res"])
    transactions = transactions[transactions.type == 1]
    
    for row in transactions.iterrows():
        c.execute('SELECT * FROM transactions WHERE id=?', (row[1][2],))
        if c.fetchone():
            continue
        else:
            c.execute("INSERT INTO transactions VALUES (?,?,?,?)", (row[1][2], row[1][3], row[1][5], row[1][7]))
    i += 1


# In[ ]:


conn.commit()


# In[ ]:


conn.close()

