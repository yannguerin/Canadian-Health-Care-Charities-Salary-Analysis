# Standard Library
import time
import json

# Common 3rd Party
import requests
import pandas as pd
import numpy as np

# Specific Use Case 3rd Party
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pymongo

# Custom Module
from utils import parse_charity_details

# Initializing Connection to MongoDB Database
client = MongoClient()
db = client.canadian_charities
detailed_charity_info = db.detailed_charity_info
# 3443
for page_num in range(2000, 3443):
    base_search = f"https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dtldBscSrch?dsrdPg={page_num}&q.stts=0007&q.ordrClmn=NAME&q.ordrRnk=ASC"
    detailed = pd.read_html(base_search)
    detailed_charities = detailed[0]["Detailed list"]
    for detailed_text in detailed_charities:
        detailed_charity_info.insert_one(parse_charity_details(detailed_text))

print("Done")
