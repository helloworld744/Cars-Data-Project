import pandas as pd

df = pd.read_csv("carsdata.csv")

df['price'] = df['price'].replace({'\$': '', ',': '', '"': ''}, regex=True).astype(int)

df['mileage'] = df['mileage'].replace({'mi.': '', ',': ''}, regex=True).astype(int)

df['mpg'] = df['mpg'].str.replace('–', ',')

df['price drop'] = df['price drop'].replace({',': '', '\$': '', '"': '', ' price drop': ''}, regex=True)

df.to_csv("carsdata.csv", index=False)
