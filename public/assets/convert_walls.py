import json
import os

# Load original format
with open("walls.json") as f:
    raw_data = json.load(f)

# Convert format
converted_data = [
    {
        "x1": wall["start"][0],
        "y1": wall["start"][1],
        "x2": wall["end"][0],
        "y2": wall["end"][1]
    }
    for wall in raw_data
]

# Save to public folder
os.makedirs("public", exist_ok=True)
with open("public/walls.json", "w") as f:
    json.dump(converted_data, f, indent=2)

print("✅ Converted walls.json saved to public/walls.json")