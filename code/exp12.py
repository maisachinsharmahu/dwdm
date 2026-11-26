import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import (silhouette_score, silhouette_samples,
                             davies_bouldin_score, calinski_harabasz_score,
                             adjusted_rand_score,
                             normalized_mutual_info_score,
                             homogeneity_score, completeness_score)

X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=1.0,
                       random_state=21)

ks = range(2, 9)
sse, sil, dbi, chi = [], [], [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    sse.append(km.inertia_)
    sil.append(silhouette_score(X, km.labels_))
    dbi.append(davies_bouldin_score(X, km.labels_))
    chi.append(calinski_harabasz_score(X, km.labels_))

print(f"{'k':>2} | {'SSE':>9} | {'Silhouette':>10} | {'Davies-B':>8} | "
      f"{'Calinski-H':>10}")
print("-" * 52)
for k, a, b, c, d in zip(ks, sse, sil, dbi, chi):
    print(f"{k:>2} | {a:>9.1f} | {b:>10.3f} | {c:>8.3f} | {d:>10.1f}")
best = list(ks)[int(np.argmax(sil))]
print(f"\nBest k by silhouette  : {best}")
print("Best k by Davies-Bouldin (lowest) :", list(ks)[int(np.argmin(dbi))])
print("Best k by Calinski-Harabasz       :", list(ks)[int(np.argmax(chi))])

labels = KMeans(n_clusters=best, n_init=10, random_state=0).fit_predict(X)
print(f"\nExternal measures for k = {best}")
print(f"  Adjusted Rand Index : {adjusted_rand_score(y_true, labels):.3f}")
nmi = normalized_mutual_info_score(y_true, labels)
print(f"  Normalised Mutual Info : {nmi:.3f}")
print(f"  Homogeneity         : {homogeneity_score(y_true, labels):.3f}")
print(f"  Completeness        : {completeness_score(y_true, labels):.3f}")

fig, ax = plt.subplots(2, 3, figsize=(13, 7.5))
ax[0, 0].plot(list(ks), sse, "o-"); ax[0, 0].set_title("Elbow (SSE)")
ax[0, 1].plot(list(ks), sil, "o-", color="green")
ax[0, 1].set_title("Silhouette (higher is better)")
ax[0, 2].plot(list(ks), dbi, "o-", color="red")
ax[0, 2].set_title("Davies-Bouldin (lower is better)")
ax[1, 0].plot(list(ks), chi, "o-", color="purple")
ax[1, 0].set_title("Calinski-Harabasz (higher)")
for a in ax[0]:
    a.axvline(best, color="gray", ls="--")
    a.set_xlabel("number of clusters k")
ax[1, 0].set_xlabel("number of clusters k")
s = silhouette_samples(X, labels)
y0 = 0
for c in range(best):
    v = np.sort(s[labels == c])
    ax[1, 1].fill_betweenx(np.arange(y0, y0 + len(v)), 0, v, alpha=0.8)
    y0 += len(v) + 5
ax[1, 1].axvline(silhouette_score(X, labels), color="red", ls="--")
ax[1, 1].set_title(f"Silhouette plot, k = {best}")
ax[1, 1].set_xlabel("silhouette value")
ax[1, 2].scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", s=15)
ax[1, 2].set_title(f"K-Means result, k = {best}")
plt.tight_layout()
plt.show()
