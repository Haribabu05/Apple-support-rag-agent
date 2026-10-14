import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")  # so emojis don't crash the Windows console

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"
df = pd.read_csv(BASE + r"\data\apple_conversations_flags.csv")

df = df[~df["other_brand_in_thread"]]

buckets = {
    "A: no DM mentioned": df[~df["mentions_dm"]],
    "B: DM + short reply (<20 words)": df[df["mentions_dm"] & (df["reply_words"] < 20)],
    "C: DM + longer reply (20+ words)": df[df["mentions_dm"] & (df["reply_words"] >= 20)],
}

for name, b in buckets.items():
    print("=" * 70)
    print(f"{name}  ->  {len(b)} conversations")
    for _, r in b.sample(8, random_state=5).iterrows():
        print(f"\nCUSTOMER: {str(r['customer_msg'])[:200]}")
        print(f"APPLE:    {str(r['first_reply'])[:200]}")