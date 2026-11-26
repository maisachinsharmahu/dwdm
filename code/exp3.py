import pandas as pd
import matplotlib.pyplot as plt

rows = [
    (101, "Rahul Sharma",  "rahul@mail.com",  "Delhi",  "2025-01-10"),
    (102, "Priya Verma",   "priya@mail.com",  "Mumbai", "2025-01-11"),
    (101, "Rahul Sharma",  "rahul@mail.com",  "Delhi",  "2025-01-10"),
    (103, "John Smith",    "john@mail.com",   "Pune",   "2025-01-12"),
    (104, " priya verma ", "PRIYA@mail.com",  "Mumbai", "2025-01-11"),
    (105, "Aman Gupta",    "aman@mail.com",   "Noida",  "2025-01-13"),
    (103, "John Smith",    "john@mail.com",   "Pune",   "2025-01-12"),
    (106, "Aman Gupta",    "aman@mail.com",   "Gurgaon","2025-01-20"),
]
df = pd.DataFrame(rows, columns=["id", "name", "email", "city", "updated"])
print("Original data :", len(df), "rows")
print(df.to_string(index=False))

print("\nExact duplicate rows found:", df.duplicated().sum())
step1 = df.drop_duplicates()
print("After removing exact duplicates:", len(step1), "rows")

step2 = step1.copy()
step2["name"] = step2["name"].str.strip().str.title()
step2["email"] = step2["email"].str.strip().str.lower()
step2 = step2.drop_duplicates(subset=["name", "email"])
print("After standardising text and removing duplicates:",
      len(step2), "rows")

step3 = step2.sort_values("updated").drop_duplicates("email", keep="last")
step3 = step3.sort_values("id")
print("After keeping latest record per email:", len(step3), "rows")
print("\nFinal clean table")
print(step3.to_string(index=False))

sizes = [len(df), len(step1), len(step2), len(step3)]
labels = ["Original", "Exact dup.\nremoved",
          "Text standardised\n+ dedup", "Latest per\nemail"]
plt.figure(figsize=(7, 3.6))
bars = plt.bar(labels, sizes,
               color=["#b0b0b0", "#4c72b0", "#55a868", "#dd8452"])
for b in bars:
    plt.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.1,
             int(b.get_height()), ha="center")
plt.ylabel("number of rows")
plt.title("Rows remaining after each cleansing step")
plt.tight_layout()
plt.show()
