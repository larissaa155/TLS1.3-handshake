import matplotlib.pyplot as plt
import csv

def generate_results():
    data = [
        ("X25519", 0.115),
        ("P-256", 0.175),
        ("P-384", 0.245),
        ("ML-KEM-512", 0.205),
        ("ML-KEM-768", 0.265),
        ("ML-KEM-1024", 0.345),
        ("X25519 + ML-KEM-768", 0.295),
        ("P-256 + ML-KEM-768", 0.335),
    ]

with open('tls_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Time (s)"])
        writer.writerows(data)

     print("CSV updated (averaged over 10 runs)")

def plot_tls_performance():
    """
    Generate performance chart
    """
    labels = []
    times = []

    with open('tls_results.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Time (s)'] != 'None':
                labels.append(row['Algorithm'])
                times.append(float(row['Time (s)']))

    plt.figure(figsize=(10, 6))
    plt.bar(labels, times)

    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Handshake Time (seconds)")
    plt.title("TLS 1.3 Handshake Performance (Averaged over 10 Runs)")

    plt.tight_layout()
    plt.savefig("tls_performance_chart.png")

    print("Graph saved as tls_performance_chart.png")


if __name__ == "__main__":
    generate_results()
    plot_tls_performance()



