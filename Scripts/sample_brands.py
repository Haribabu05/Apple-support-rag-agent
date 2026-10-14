import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"
BRAND = "SpotifyCares"  # change this to try other brands

df = pd.read_csv(BASE + r"\dataset\twcs.csv")
df["tweet_id"] = df["tweet_id"].astype("Int64")
df["in_response_to_tweet_id"] = df["in_response_to_tweet_id"].astype("Int64")
lookup = df.set_index("tweet_id")

replies = df[df["author_id"] == BRAND].sample(12, random_state=7)

for _, r in replies.iterrows():
    parent = r["in_response_to_tweet_id"]
    if pd.notna(parent) and parent in lookup.index:
        print(f"\nCUSTOMER: {str(lookup.loc[parent, 'text'])[:200]}")
        print(f"{BRAND}: {str(r['text'])[:200]}")