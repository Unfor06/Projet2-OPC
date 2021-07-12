from requests import Session
import os
import pandas as pd

SESSION = Session()

df = pd.read_csv("scraped_data.csv")

for categorie, df_categorie in df.groupby("category"):
    df_categorie.to_csv(f"{categorie}.csv")
for _, row in df[["title", "image"]].iterrows():
    title = row['title'].replace("/", "_")
    img = row['image']
    
    with open(os.path.join("Books_img", f"{title}.jpg"), "wb") as f:
        image = SESSION.get(img)
        f.write(image.content)
        print('Téléchargement image de : ', title)

