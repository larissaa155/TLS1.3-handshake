import matplotlib.pyplot as plt
import csv

labels = []
times = []

with open('tls_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Time (s)'] != 'None':
            labels.append(row['Algorithm'])
            times.append(float(row['Time (s)']))

plt.figure()
plt.bar(labels, times)

plt.xticks(rotation=45)
plt.ylabel("Handshake Time (seconds)")
plt.title("TLS 1.3 Handshake Performance Comparison")

plt.tight_layout()
plt.savefig("tls_performance_chart.png")
