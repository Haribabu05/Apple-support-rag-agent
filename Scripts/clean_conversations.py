import json
import re
import pandas as pd

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"

URL = re.compile(r"https?://\S+")
MENTION = re.compile(r"@\w+")
THANKS = re.compile(r"thank|thx|awesome|perfect|worked|fixed|appreciate", re.I)
DM = re.compile(r"\bDMs?\b|direct message", re.I)

def clean(t):
    t = URL.sub("", t)
    t = MENTION.sub("", t)
    return re.sub(r"\s+", " ", t).strip()

rows = []
with open(BASE + r"\data\apple_conversations.jsonl", encoding="utf-8") as f:
    for line in f:
        conv = json.loads(line)
        turns = conv["turns"]
        root_author = turns[0]["author"]
        apple_texts = [clean(t["text"]) for t in turns if t["author"] == "AppleSupport"]
        first_reply = apple_texts[0]
        last = turns[-1]
        customer_last = last["author"] == root_author

        rows.append({
            "conversation_id": conv["conversation_id"],
            "n_turns": len(turns),
            "customer_msg": clean(turns[0]["text"]),
            "first_reply": first_reply,
            "reply_words": len(first_reply.split()),
            "mentions_dm": bool(DM.search(" ".join(apple_texts))),
            "customer_thanks_last": customer_last and bool(THANKS.search(last["text"])),
            "other_brand_in_thread": any(
                t["author"] not in ("AppleSupport", root_author) for t in turns
            ),
        })

df = pd.DataFrame(rows)

print("Total:", len(df))
print("Apple mentions DM:", round(df["mentions_dm"].mean(), 3))
print("Short reply (<20 words) AND mentions DM:",
      round(((df["reply_words"] < 20) & df["mentions_dm"]).mean(), 3))
print("Customer thanks at end:", round(df["customer_thanks_last"].mean(), 3))
print("Other brand in thread:", round(df["other_brand_in_thread"].mean(), 3))
print("\nReply length (words):")
print(df["reply_words"].describe())

df.to_csv(BASE + r"\data\apple_conversations_flags.csv", index=False)
print("\nSaved flags file.")