# Experiment 2: Data cleansing: inconsistent names

> **File:** `exp2.py`  |  **Tools:** Python 3.13 (re module), MacOS

## 🎯 Aim

Write a data cleansing program that takes inconsistent names from the user and formats them in a standard way.

## 📘 Theory

Data cleansing removes errors and inconsistencies before data enters the warehouse. Names typed by different users are often written with extra spaces, wrong capital letters, wrong spellings, digits or symbols. If they are stored like this, the same person can appear as several different customers, which spoils every report built on top of the data.

- **Standardisation**: converting every name into one common format, such as Proper Case.
- **Trimming**: removing the leading, trailing and repeated spaces.
- **Noise removal**: deleting digits and special symbols that are not part of a name.
- **Spelling correction**: replacing common wrong spellings using a dictionary of known mistakes.
- **Order correction**: converting the form "Doe, John" into "John Doe".

## 🪜 Algorithm / Steps

1. Create a dictionary of common wrong spellings and their correct form.
2. Ask the user to enter a name inside a loop and stop when the user types exit.
3. Clean the name: trim it, remove symbols, reduce repeated spaces and fix the "last, first" order.
4. Convert each word to Proper Case and replace it if it is present in the dictionary.
5. Display the raw name and the cleaned name.

## 💻 Code

```python
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
```

> Run it and type the names shown in the output below (or `exit` to stop).

## 🖥️ Output

```text
Data-warehouse name cleansing
Enter a name (or 'exit' to stop):   jhon   doe  
   Raw name     : '  jhon   doe  '
   Cleaned name : John Doe
Enter a name (or 'exit' to stop): mIcHaEl jOrDaN
   Raw name     : 'mIcHaEl jOrDaN'
   Cleaned name : Michael Jordan
Enter a name (or 'exit' to stop): SARAAH    connor
   Raw name     : 'SARAAH    connor'
   Cleaned name : Sarah Connor
Enter a name (or 'exit' to stop): doe, rahull
   Raw name     : 'doe, rahull'
   Cleaned name : Rahul Doe
Enter a name (or 'exit' to stop): pri9ya   sh@arma
   Raw name     : 'pri9ya   sh@arma'
   Cleaned name : Priya Sharma
Enter a name (or 'exit' to stop): exit
Total names cleaned: 5
```

## ✅ Result

Five different inconsistent entries were cleaned correctly, for example "  jhon   doe  " became John Doe, "SARAAH    connor" became Sarah Connor, "doe, rahull" became Rahul Doe and "pri9ya   sh@arma" became Priya Sharma.

## 🎤 Viva Questions

**Q. Why are names cleansed before loading?**  
A. The same person written in different ways would be counted as different people.

**Q. What problems did the program fix?**  
A. Extra spaces, digits and symbols, wrong capitals, titles, surname-first order and spelling variants.

**Q. What is a lookup table?**  
A. A dictionary that maps known wrong forms to the correct form.

**Q. What is standardisation?**  
A. Writing values of one kind in one agreed format.

**Q. Which Python module was used for patterns?**  
A. re, the regular expression module.

---
[⬅ Back to index](README.md)
