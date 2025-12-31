import requests
import re
from urllib.parse import urlparse

print("""
====================================
 DEV WEB SECURITY CHECKER (TERMUX)
====================================
⚠️ Gunakan hanya untuk website sendiri
""")

url = input("Masukkan URL (contoh: https://site.com/search?q=): ").strip()

if not url.startswith("http"):
    print("[ERROR] URL harus pakai http/https")
    exit()

payloads = {
    "SQL Injection": [
        "' OR '1'='1",
        "' AND 1=1--",
        "' UNION SELECT null--"
    ],
    "XSS": [
        "<script>alert(1)</script>",
        "\"><svg/onload=alert(1)>"
    ]
}

issues = []

def check_payload(payload, vuln_type):
    try:
        r = requests.get(url + payload, timeout=6)
        if payload.lower()[:10] in r.text.lower():
            issues.append((vuln_type, payload))
            print(f"[‼️] {vuln_type} TERDETEKSI → {payload}")
    except:
        print("[!] Target tidak merespon")

print("\n[🔍] Scan Input Vulnerability")
for vuln, tests in payloads.items():
    print(f"\n--- {vuln} ---")
    for p in tests:
        check_payload(p, vuln)

print("\n[🔍] Scan Security Headers")
try:
    res = requests.get(url.split("?")[0], timeout=6)
    headers = res.headers

    required_headers = {
        "Content-Security-Policy": "Tambahkan CSP untuk cegah XSS",
        "X-Frame-Options": "Tambahkan SAMEORIGIN / DENY",
        "X-Content-Type-Options": "Gunakan nosniff",
        "Referrer-Policy": "Batasi kebocoran referrer"
    }

    for h, fix in required_headers.items():
        if h not in headers:
            issues.append(("Missing Header", h))
            print(f"[⚠️] {h} TIDAK ADA → {fix}")
        else:
            print(f"[✅] {h} OK")

except:
    print("[!] Gagal cek header")

print("\n==============================")
if issues:
    print("🚨 HASIL: WEBSITE PERLU PERBAIKAN")
    print("📌 Rekomendasi Developer:")
    print("- Gunakan prepared statements (SQL)")
    print("- Escape output (htmlspecialchars / encode)")
    print("- Tambahkan security headers")
    print("- Validasi input server-side")
else:
    print("✅ HASIL: TIDAK ADA MASALAH SERIUS TERDETEKSI")
    print("👍 Aman untuk lanjut development")

print("==============================")
