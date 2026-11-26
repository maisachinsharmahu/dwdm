import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram

X, y_true = make_blobs(n_samples=150, centers=3, cluster_std=2.3,
                       random_state=4)
K = 3
rng = np.random.default_rng(5)

def dist(A, B):
    return np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(axis=2))

def kmeans(X, k, iters=100):
    cent = X[rng.choice(len(X), k, replace=False)]
    for it in range(1, iters + 1):
        labels = dist(X, cent).argmin(axis=1)
        new = np.array([X[labels == j].mean(axis=0) for j in range(k)])
        if np.allclose(new, cent):
            break
        cent = new
    sse = sum(((X[labels == j] - cent[j]) ** 2).sum() for j in range(k))
    return labels, cent, sse, it

def kmedoids(X, k, iters=50):
    D = dist(X, X)
    med = list(rng.choice(len(X), k, replace=False))
    cost = D[:, med].min(axis=1).sum()
    for it in range(1, iters + 1):
        improved = False
        for mi in range(k):
            for cand in range(len(X)):
                if cand in med:
                    continue
                trial = med.copy(); trial[mi] = cand
                c = D[:, trial].min(axis=1).sum()
                if c < cost:
                    med, cost, improved = trial, c, True
        if not improved:
            break
    return D[:, med].argmin(axis=1), X[med], cost, it

def clara(X, k, samples=5, size=40):
    best = None
    for _ in range(samples):
        idx = rng.choice(len(X), size, replace=False)
        _, med, _, _ = kmedoids(X[idx], k)
        cost = dist(X, med).min(axis=1).sum()
        if best is None or cost < best[0]:
            best = (cost, med)
    cost, med = best
    return dist(X, med).argmin(axis=1), med, cost

lab_km, c_km, sse, it_km = kmeans(X, K)
lab_md, c_md, cost_md, it_md = kmedoids(X, K)
lab_cl, c_cl, cost_cl = clara(X, K)
Z = linkage(X, method="ward")
lab_hc = fcluster(Z, K, criterion="maxclust") - 1

print(f"Data: {len(X)} points, k = {K}")
print(f"K-Means   : converged in {it_km} iterations, SSE = {sse:.1f}")
print(f"K-Medoids : converged in {it_md} passes,     cost = {cost_md:.1f}")
print(f"CLARA     : best of 5 samples,          cost = {cost_cl:.1f}")
print(f"Hierarchical (Ward) : cut at {K} clusters")
print("\nCluster sizes")
for name, lab in [("K-Means", lab_km), ("K-Medoids", lab_md),
                  ("CLARA", lab_cl), ("Hierarchical", lab_hc)]:
    print(f"  {name:<13}", np.bincount(lab))
print("\nAgreement with true groups (Adjusted Rand Index)")
for name, lab in [("K-Means", lab_km), ("K-Medoids", lab_md),
                  ("CLARA", lab_cl), ("Hierarchical", lab_hc)]:
    print(f"  {name:<13} {adjusted_rand_score(y_true, lab):.3f}")

fig, ax = plt.subplots(2, 3, figsize=(13, 8))
panels = [("K-Means", lab_km, c_km), ("K-Medoids (PAM)", lab_md, c_md),
          ("CLARA (partitioning)", lab_cl, c_cl),
          ("Hierarchical (Ward)", lab_hc, None)]
for a, (title, lab, cen) in zip(ax.ravel()[:4], panels):
    a.scatter(X[:, 0], X[:, 1], c=lab, cmap="viridis", s=18)
    if cen is not None:
        a.scatter(cen[:, 0], cen[:, 1], marker="X", s=200, c="red",
                  edgecolor="black")
    a.set_title(title)
dendrogram(Z, ax=ax[1, 1], truncate_mode="lastp", p=20, no_labels=True)
ax[1, 1].set_title("Dendrogram (last 20 merges)")
ax[1, 2].scatter(X[:, 0], X[:, 1], c=y_true, cmap="viridis", s=18)
ax[1, 2].set_title("True groups")
ax[0, 0].set_ylabel("x2"); ax[1, 0].set_xlabel("x1")
plt.tight_layout()
plt.show()
