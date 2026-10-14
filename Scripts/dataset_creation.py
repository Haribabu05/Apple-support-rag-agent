import pandas as pd

df = pd.read_csv(
    r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot\dataset\twcs.csv"
)

print("Full dataset:", df.shape)

apple = df[df["author_id"] == "AppleSupport"]

print("AppleSupport tweets:", apple.shape)

apple.to_csv(
    r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot\data\apple_tweets.csv",
    index=False
)

print("Apple data saved successfully.")