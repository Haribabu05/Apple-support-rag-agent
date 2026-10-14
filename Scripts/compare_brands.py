import pandas as pd

BASE = r"C:\Users\Administrator\Desktop\YCDI\Apple Chatbot"
df = pd.read_csv(BASE + r"\dataset\twcs.csv", usecols=["author_id", "inbound", "text"])

top = [
    "AppleSupport", "SpotifyCares", "Delta", "AmericanAir", "SouthwestAir",
    "XboxSupport", "AskPlayStation", "Uber_Support", "Tesco", "hulu_support",
]
rows = []
for b in top:
    t = df[df["author_id"] == b]["text"].astype(str)
    rows.append({
        "brand": b,
        "replies": len(t),
        "mentions_dm_%": round(t.str.contains(r"\bDMs?\b", case=False).mean() * 100, 1),
        "has_link_%": round(t.str.contains("http").mean() * 100, 1),
        "median_words": int(t.str.split().str.len().median()),
    })

print(pd.DataFrame(rows).to_string(index=False))