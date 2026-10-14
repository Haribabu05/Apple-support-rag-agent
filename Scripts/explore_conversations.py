import json
import pandas as pd

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"

rows = []
with open(BASE + r"\data\apple_conversations.jsonl", encoding="utf-8") as f:
    for line in f:
        conv = json.loads(line)
        turns = conv["turns"]
        apple_turns = [t for t in turns if t["author"] == "AppleSupport"]
        rows.append({
            "conversation_id": conv["conversation_id"],
            "n_turns": len(turns),
            "n_apple": len(apple_turns),
            "last_author": turns[-1]["author"],
            "first_text": turns[0]["text"],
            "last_text": turns[-1]["text"],
        })

df = pd.DataFrame(rows)

print("Total conversations:", len(df))
print("\nTurns per conversation:")
print(df["n_turns"].describe())
print("\nShare by number of turns (top 8):")
print(df["n_turns"].value_counts(normalize=True).head(8).round(3))
print("\nWho speaks last?")
print(df["last_author"].value_counts(normalize=True).round(3))

# How many Apple conversations only say "DM" and nothing else?
dm_only = df["first_text"].str.len() > 0  # placeholder to keep df usable
print("\nSample of 5 random conversations' first message:")
for t in df["first_text"].sample(5, random_state=3):
    print("-", t[:150].replace("\n", " "))