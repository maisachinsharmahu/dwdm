# 📊 Data Warehousing & Data Mining (DWDM) Lab

Course code **CIE-425P**. Every experiment has the **theory, the code and its real output**, plus viva questions with answers, so it can be revised quickly before the exam.

## 📂 **Index – Click to Open Any File**

### 🏭 **Data Warehousing / ETL**
- [Experiment 1: Study of ETL process and its tools](Exp01-ETL-Process.md)
- [Experiment 2: Data cleansing: inconsistent names](Exp02-Data-Cleansing-Names.md)
- [Experiment 3: Data cleansing: remove redundancy](Exp03-Data-Cleansing-Redundancy.md)

### 🧰 **WEKA Tool**
- [Experiment 4: Introduction to WEKA tool](Exp04-Intro-to-WEKA.md)
- [Experiment 5: Classification on ARFF files using WEKA](Exp05-Classification-WEKA.md)
- [Experiment 6: Clustering on ARFF files using WEKA](Exp06-Clustering-WEKA.md)
- [Experiment 7: Association rules on ARFF files using WEKA](Exp07-Association-Rules-WEKA.md)
- [Experiment 8: Visualization on ARFF files using WEKA](Exp08-Visualization-WEKA.md)

### 🐍 **Algorithms in Python**
- [Experiment 9: Data similarity measures](Exp09-Similarity-Measures.md)
- [Experiment 10: Apriori algorithm for frequent itemsets](Exp10-Apriori-Algorithm.md)
- [Experiment 11: Clustering algorithms](Exp11-Clustering-Algorithms.md)
- [Experiment 12: Validity measures for clustering](Exp12-Clustering-Validity.md)

### 📁 **Code and datasets**
- [`code/`](code) has every program as a separate runnable file
- [`data/iris.arff`](data/iris.arff) and [`data/weather.nominal.arff`](data/weather.nominal.arff) (used by the WEKA experiments). The Java programs read `data/iris.arff`, so run them from the repo root.

## ▶️ How to run

```bash
pip install numpy pandas matplotlib scipy scikit-learn
cd code
python3 exp9.py        # Python experiments (1, 2, 3, 9, 10, 11, 12)
cd ..
# WEKA experiments (4 to 8) need weka.jar and JDK 17
javac -cp weka.jar code/IntroWeka.java && java -cp code:weka.jar IntroWeka
```
