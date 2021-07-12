import requests
import bs4 
import pandas as pd

df = pd.read_csv("scraped_data.csv")
df["title"] = df["title"] \
                .str.split("|") \
                .str[0] \
                .str.strip()
df["available"] = df["available"] \
                    .str.split("(").str[1] \
                    .str.split().str[0] \
                    .astype(int)


df["rating"] = df["rating"] \
                  .str.replace('One', '1') \
                  .str.replace('Two', '2') \
                  .str.replace('Three', '3') \
                  .str.replace('Four', '4') \
                  .str.replace('Five', '5') \
                  .astype(int)

df["price_in_tax"] = df["price_in_tax"] \
                  .str.strip("£") \
                  .astype(float)
df["price_ex_tax"] = df["price_ex_tax"] \
                  .str.strip("£") \
                  .astype(float)

df.to_csv("scraped_data.csv")
