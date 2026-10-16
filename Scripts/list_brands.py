import pandas as pd

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"

df = pd.read_csv(BASE + r"\dataset\twcs.csv", usecols=["author_id", "inbound"])

brands = df[df["inbound"] == False]["author_id"].value_counts()

print("Number of brands:", len(brands))
print()
print(brands.to_string())

brands.to_csv(BASE + r"\data\brands.csv", header=["reply_count"])
print("\nSaved to data\\brands.csv")  