import pandas as pd

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"

# Conversations + flags file created by clean_conversations.py
df = pd.read_csv(BASE + r"\data\apple_conversations_flags.csv")

# Remove threads where another brand replied, and empty customer messages
df = df[~df["other_brand_in_thread"]]
df = df[df["customer_msg"].notna() & (df["customer_msg"].str.strip() != "")]

# Random sample of 250 (random_state makes it the same every time you run it)
sample = df.sample(250, random_state=42)[
    ["conversation_id", "customer_msg", "first_reply"]
].copy()

# Empty columns for you to fill in by hand
sample["intent"] = ""
sample["is_frustrated"] = ""
sample["should_escalate"] = ""
sample["notes"] = ""

# utf-8-sig so Excel shows apostrophes and emojis correctly
sample.to_csv(
    BASE + r"\data\golden_candidates.csv",
    index=False,
    encoding="utf-8-sig",
)
print("Saved", len(sample), "rows to data\\golden_candidates.csv")