from itertools import combinations

transactions = [
    {"bread", "milk"},
    {"bread", "diaper", "beer", "eggs"},
    {"milk", "diaper", "beer", "cola"},
    {"bread", "milk", "diaper", "beer"},
    {"bread", "milk", "diaper", "cola"},
    {"bread", "milk", "diaper"},
    {"milk", "diaper", "beer"},
    {"bread", "milk", "eggs"},
]
N = len(transactions)
MIN_SUP, MIN_CONF = 0.375, 0.7

def count(itemset):
    return sum(1 for t in transactions if itemset <= t)

items = sorted({i for t in transactions for i in t})
level = [frozenset([i]) for i in items]
frequent, k = {}, 1
while level:
    survivors = {s: count(s) for s in level if count(s) / N >= MIN_SUP}
    if not survivors:
        break
    print(f"L{k}: {len(level)} candidates -> {len(survivors)} frequent")
    ordered = sorted(survivors.items(),
                     key=lambda x: (-x[1], sorted(x[0])))
    for s, c in ordered:
        print(f"     {sorted(s)}  count = {c}  support = {c / N:.3f}")
    frequent.update(survivors)
    k += 1
    keys = list(survivors)
    level = {a | b for a in keys for b in keys if len(a | b) == k}
    level = [c for c in level
             if all(frozenset(s) in survivors
                    for s in combinations(c, k - 1))]

print(f"\nRules with confidence >= {MIN_CONF:.0%}")
rules = []
for s, c in frequent.items():
    if len(s) < 2:
        continue
    for r in range(1, len(s)):
        for lhs in map(frozenset, combinations(s, r)):
            rhs = s - lhs
            conf = c / frequent[lhs]
            lift = conf / (frequent[rhs] / N)
            if conf >= MIN_CONF:
                rules.append((sorted(lhs), sorted(rhs), c / N, conf, lift))
for lhs, rhs, sup, conf, lift in sorted(rules, key=lambda r: -r[3]):
    print(f"  {str(lhs):<22} -> {str(rhs):<12} sup={sup:.3f} "
          f"conf={conf:.2f} lift={lift:.2f}")
print("\nTotal frequent itemsets:", len(frequent), " Rules:", len(rules))

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
big = sorted(((sorted(s), c / N) for s, c in frequent.items()
              if len(s) >= 2), key=lambda x: x[1])
ax[0].barh([" + ".join(s) for s, _ in big], [v for _, v in big],
           color="#4c72b0")
ax[0].axvline(MIN_SUP, color="red", ls="--", label="min support")
ax[0].set_xlabel("support"); ax[0].legend()
ax[0].set_title("Frequent itemsets (size 2 and more)")
ax[1].scatter([r[2] for r in rules], [r[3] for r in rules],
              s=[60 * r[4] for r in rules], alpha=0.6, color="#dd8452")
ax[1].set_xlabel("support"); ax[1].set_ylabel("confidence")
ax[1].set_title("Association rules (bubble size = lift)")
ax[1].grid(alpha=0.3)
plt.tight_layout()
plt.show()
