import pandas as pd
import json

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"

df = pd.read_csv(BASE + r"\dataset\twcs.csv")

print("Total tweets:", len(df))
print("Columns:", df.columns.tolist())
print("AppleSupport tweets:", (df["author_id"] == "AppleSupport").sum())
print("Inbound values:", df["inbound"].value_counts(dropna=False))
print("Loading completed")

df["tweet_id"] = df["tweet_id"].astype("Int64")
df["in_response_to_tweet_id"] = df["in_response_to_tweet_id"].astype("Int64")
df["created_at"] = pd.to_datetime(df["created_at"], format="%a %b %d %H:%M:%S %z %Y")

# tweet_id -> its text/author/time
info = {
    t: (a, x, c)
    for t, a, x, c in zip(df["tweet_id"], df["author_id"], df["text"], df["created_at"])
}

# parent tweet_id -> list of tweets replying to it
replies = (
    df.dropna(subset=["in_response_to_tweet_id"])
      .groupby("in_response_to_tweet_id")["tweet_id"]
      .apply(list)
      .to_dict()
)

# Roots = customer's first tweet that Apple replied to
apple = df[df["author_id"] == "AppleSupport"]
apple_parents = set(apple["in_response_to_tweet_id"].dropna())

roots = df[
    (df["inbound"] == True)
    & (df["in_response_to_tweet_id"].isna())
    & (df["tweet_id"].isin(apple_parents))
]
print("Apple conversations found:", len(roots))

def collect(root_id):
    """Gather root + all descendants, sorted by time."""
    stack, found = [root_id], []
    while stack:
        t = stack.pop()
        found.append(t)
        stack.extend(replies.get(t, []))
    found.sort(key=lambda t: info[t][2])
    return found

out_path = BASE + r"\data\apple_conversations.jsonl"
with open(out_path, "w", encoding="utf-8") as f:
    for root_id in roots["tweet_id"]:
        ids = collect(root_id)
        turns = [{"tweet_id": int(t), "author": info[t][0], "text": info[t][1]} for t in ids]
        f.write(json.dumps({"conversation_id": int(root_id), "turns": turns}) + "\n")

print("Saved to", out_path)