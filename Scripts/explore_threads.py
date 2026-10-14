import pandas as pd

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"

# Full dataset, because customer tweets live here
df = pd.read_csv(BASE + r"\dataset\twcs.csv")

# IDs have decimals (698.0) because of empty values. Make them clean integers.
df["tweet_id"] = df["tweet_id"].astype("Int64")
df["in_response_to_tweet_id"] = df["in_response_to_tweet_id"].astype("Int64")

# Lookup table: tweet_id -> row
lookup = df.set_index("tweet_id")

def get_thread(tweet_id):
    """Start at one tweet, walk upward to the first message."""
    chain = []
    current = tweet_id
    while pd.notna(current) and current in lookup.index:
        row = lookup.loc[current]
        chain.append((row["author_id"], row["text"]))
        current = row["in_response_to_tweet_id"]
    return list(reversed(chain))  # oldest message first

apple = df[df["author_id"] == "AppleSupport"]

# Look at 3 random Apple replies
for tid in apple["tweet_id"].sample(3, random_state=1):
    print("=" * 70)
    for author, text in get_thread(tid):
        print(f"[{author}] {text}\n")

#command
