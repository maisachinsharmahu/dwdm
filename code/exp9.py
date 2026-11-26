import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

def euclidean(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def manhattan(a, b):
    return np.sum(np.abs(a - b))

def minkowski(a, b, p):
    return np.sum(np.abs(a - b) ** p) ** (1 / p)

names = ["P1", "P2", "P3", "P4", "P5"]
X = np.array([[2, 10], [2, 5], [8, 4], [5, 8], [7, 5]], dtype=float)

a, b = X[0], X[2]
print("Two points      : P1 =", a, " P3 =", b)
print(f"Euclidean       : {euclidean(a, b):.4f}")
print(f"Manhattan       : {manhattan(a, b):.4f}")
print(f"Minkowski (p=3) : {minkowski(a, b, 3):.4f}")
print(f"Chebyshev       : {np.max(np.abs(a - b)):.4f}")
print(f"Check with scipy: {distance.euclidean(a, b):.4f}, "
      f"{distance.cityblock(a, b):.4f}")

n = len(X)
E_mat = np.array([[euclidean(X[i], X[j]) for j in range(n)]
                  for i in range(n)])
M_mat = np.array([[manhattan(X[i], X[j]) for j in range(n)]
                  for i in range(n)])
print("\nEuclidean distance matrix")
print(np.round(E_mat, 2))
print("\nManhattan distance matrix")
print(M_mat.astype(int))
i, j = np.unravel_index(np.argmin(E_mat + np.eye(n) * 99), E_mat.shape)
print(f"\nMost similar pair (Euclidean): {names[i]} and {names[j]} "
      f"(distance {E_mat[i, j]:.2f})")

fig, ax = plt.subplots(1, 3, figsize=(13, 4))
pairs = [(E_mat, "Euclidean"), (M_mat, "Manhattan")]
for k, (mat, title) in enumerate(pairs):
    im = ax[k].imshow(mat, cmap="YlOrRd")
    ax[k].set_xticks(range(n)); ax[k].set_xticklabels(names)
    ax[k].set_yticks(range(n)); ax[k].set_yticklabels(names)
    ax[k].set_title(f"{title} distance matrix")
    for r in range(n):
        for c in range(n):
            ax[k].text(c, r, f"{mat[r, c]:.1f}", ha="center",
                       va="center", fontsize=8)
    plt.colorbar(im, ax=ax[k], fraction=0.046)
t = np.linspace(0, 2 * np.pi, 200)
ax[2].plot(np.cos(t), np.sin(t), label="Euclidean = 1")
ax[2].plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], label="Manhattan = 1")
ax[2].plot([1, 1, -1, -1, 1], [1, -1, -1, 1, 1], label="Chebyshev = 1")
ax[2].set_aspect("equal"); ax[2].legend(loc="upper right", fontsize=8)
ax[2].set_title("Points at distance 1 from origin")
plt.tight_layout()
plt.show()
