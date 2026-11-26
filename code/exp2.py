import re

MISSPELLINGS = {"jhon": "John", "micheal": "Michael", "saraah": "Sarah",
                "rahull": "Rahul", "preya": "Priya"}

def clean_name(raw):
    name = raw.strip()
    name = re.sub(r"[^A-Za-z ,.'-]", "", name)
    name = re.sub(r"\s+", " ", name)
    if "," in name:
        last, first = [p.strip() for p in name.split(",", 1)]
        name = f"{first} {last}"
    words = []
    for w in name.split(" "):
        w = w.capitalize()
        words.append(MISSPELLINGS.get(w.lower(), w))
    return " ".join(words)

print("Data-warehouse name cleansing")
count = 0
while True:
    raw = input("Enter a name (or 'exit' to stop): ")
    if raw.strip().lower() == "exit":
        break
    count += 1
    print(f"   Raw name     : {raw!r}")
    print(f"   Cleaned name : {clean_name(raw)}")
print(f"Total names cleaned: {count}")
