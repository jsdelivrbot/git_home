#!/usr/bin/python2.7

import pandas as pd

data = pd.read_csv("Auto.csv")

data["brand"] = data.name.map(lambda l: l.split()[0])

data.to_csv("Auto_transformed.csv")
