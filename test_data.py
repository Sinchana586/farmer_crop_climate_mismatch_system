import pandas as pd

crop = pd.read_csv("datasets/Crop_recommendation.csv")
rainfall = pd.read_csv("datasets/district wise rainfall normal.csv")

print("Crop Dataset Shape:")
print(crop.shape)

print("\nCrop Columns:")
print(list(crop.columns))

print("\nRainfall Dataset Shape:")
print(rainfall.shape)

print("\nRainfall Columns:")
print(list(rainfall.columns))