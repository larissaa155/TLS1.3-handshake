import subprocess
import time
import csv
import random

def test_handshake(cipher_suite, key_exchange, runs=3):
    times = []
    for _ in range(runs):
        start = time.time()
        try:
            result = subprocess.run(
                [
                    'openssl', 's_time',
                    '-connect', 'google.com:443',
                    '-tls1_3',
                    '-ciphersuites', cipher_suite,
                    '-curves', key_exchange,
                    '-time', '2'
                ],
                capture_output=True,
                text=True
            )
            end = time.time()
            if result.returncode == 0:
                times.append(end - start)
        except Exception as e:
            print("Error:", e)

    if times:
        return round(sum(times) / len(times), 4)
    return None


def simulate_pq_algorithm(name):
    base = random.uniform(0.01, 0.05)
    if "512" in name:
        return base + 0.02
    elif "768" in name:
        return base + 0.05
    elif "1024" in name:
        return base + 0.08
    elif "HQC" in name:
        return base + 0.06
    elif "BIKE" in name:
        return base + 0.07
    return base


def simulate_signature(name):
    base = random.uniform(0.01, 0.03)
    if name == "RSA-PSS":
        return base + 0.06
    elif name == "ECDSA":
        return base + 0.03
    elif name == "Dilithium":
        return base + 0.05
    return base


def hybrid_performance(classical, pq):
    return round(classical + pq, 4)


def main():
    classical_kex = ['X25519', 'P-256', 'P-384']
    cipher_suites = [
        'TLS_AES_128_GCM_SHA256',
        'TLS_CHACHA20_POLY1305_SHA256'
    ]

    pq_algorithms = [
        'ML-KEM-512', 'ML-KEM-768', 'ML-KEM-1024',
        'HQC-128', 'HQC-192', 'HQC-256',
        'BIKE'
    ]

    signatures = ['RSA-PSS', 'ECDSA', 'Dilithium']

    results = []

    print("Running TLS 1.3 Tests...\n")

    #Classical
    for kex in classical_kex:
        for suite in cipher_suites:
            t = test_handshake(suite, kex)
            results.append(["Classical", kex, suite, t])

    #Post-Quantum 
    for pq in pq_algorithms:
        t = simulate_pq_algorithm(pq)
        results.append(["Post-Quantum", pq, "N/A", round(t, 4)])

    #Hybrid
    for kex in classical_kex:
        base = test_handshake('TLS_AES_128_GCM_SHA256', kex)
        pq = simulate_pq_algorithm('ML-KEM-768')
        results.append([
            "Hybrid",
            f"{kex} + ML-KEM-768",
            "TLS_AES_128_GCM_SHA256",
            hybrid_performance(base, pq)
        ])

    #Signatures
    for sig in signatures:
        t = simulate_signature(sig)
        results.append(["Signature", sig, "N/A", round(t, 4)])

    #Save CSV
    with open('tls_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Algorithm", "Cipher Suite", "Time (s)"])
        writer.writerows(results)

    print("Results saved to tls_results.csv")


if __name__ == "__main__":
    main()
