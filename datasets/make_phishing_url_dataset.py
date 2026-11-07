"""
Generates a labeled dataset for Phishing URL Detection using hand-crafted URL features.
label = 1 -> phishing, label = 0 -> legitimate
Fully offline - synthetic URL generation based on well-known phishing heuristics.
"""
import csv
import random

random.seed(21)

legit_domains = [
    "google.com", "amazon.com", "wikipedia.org", "github.com", "microsoft.com",
    "apple.com", "netflix.com", "linkedin.com", "flipkart.com", "paytm.com",
    "icicibank.com", "hdfcbank.com", "sbi.co.in", "irctc.co.in", "nptel.ac.in",
    "yahoo.com", "spotify.com", "dropbox.com", "adobe.com", "salesforce.com",
]

phishing_brand_bases = [
    "paypal", "amazon", "google", "netflix", "icicibank", "hdfcbank", "sbi",
    "facebook", "instagram", "microsoft", "apple", "flipkart", "linkedin",
]

suspicious_words = ["secure", "verify", "update", "login", "account", "confirm",
                     "signin", "webscr", "banking", "alert", "suspend", "reward"]

tlds_legit = [".com", ".org", ".co.in", ".ac.in", ".net"]
tlds_suspicious = [".xyz", ".tk", ".ml", ".ga", ".cf", ".top", ".info", ".click"]


def make_legit_url():
    domain = random.choice(legit_domains)
    path_parts = random.choice(["", "/home", "/products", "/login", "/about",
                                 "/help", "/account/settings", "/search?q=item"])
    # legit sites are usually https, but occasionally plain http (e.g. old redirects)
    scheme = "https" if random.random() < 0.9 else "http"
    url = f"{scheme}://www.{domain}{path_parts}"
    return url


def make_phishing_url():
    brand = random.choice(phishing_brand_bases)
    style = random.choice(["hyphen", "subdomain", "ip", "typo", "longpath", "raw_tld"])
    # many modern phishing sites also use free HTTPS certificates (Let's Encrypt etc.)
    scheme = "https" if random.random() < 0.55 else "http"

    if style == "hyphen":
        word = random.choice(suspicious_words)
        tld = random.choice(tlds_suspicious)
        url = f"{scheme}://{brand}-{word}{tld}/index.php"
    elif style == "subdomain":
        word = random.choice(suspicious_words)
        fake_domain = f"{brand}.{word}-portal.com"
        url = f"{scheme}://{fake_domain}/"
    elif style == "ip":
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        url = f"{scheme}://{ip}/{brand}/{random.choice(suspicious_words)}.html"
    elif style == "typo":
        # simple char swap/typo on brand name
        b = list(brand)
        if len(b) > 3:
            i = random.randint(1, len(b) - 2)
            b[i], b[i + 1] = b[i + 1], b[i]
        typo_brand = "".join(b)
        url = f"{scheme}://{typo_brand}.com/{random.choice(suspicious_words)}"
    elif style == "longpath":
        word = random.choice(suspicious_words)
        tld = random.choice(tlds_suspicious)
        long_path = "/".join(random.choice(suspicious_words) for _ in range(4))
        url = f"{scheme}://{brand}{tld}/{long_path}/{word}.php?id=293847&session=abc123xyz"
    else:  # raw_tld
        word = random.choice(suspicious_words)
        tld = random.choice(tlds_suspicious)
        url = f"{scheme}://{brand}{word}{tld}"
    return url


def extract_features(url, label):
    length = len(url)
    num_dots = url.count(".")
    has_at = int("@" in url)
    has_https = int(url.startswith("https://"))
    has_ip = int(any(ch.isdigit() for ch in url.split("//")[-1].split("/")[0].split(".")[0]) and
                  all(part.isdigit() for part in url.split("//")[-1].split("/")[0].split(".") if part))
    num_hyphens = url.count("-")
    num_subdomains = url.split("//")[-1].split("/")[0].count(".")
    suspicious_word_count = sum(1 for w in suspicious_words if w in url.lower())
    has_suspicious_tld = int(any(url.lower().endswith(t) or f"{t}/" in url.lower() for t in tlds_suspicious))
    url_depth = url.count("/") - 2 if url.count("/") > 2 else 0
    has_query = int("?" in url)

    return {
        "url_length": length,
        "num_dots": num_dots,
        "has_at_symbol": has_at,
        "has_https": has_https,
        "has_ip_address": has_ip,
        "num_hyphens": num_hyphens,
        "num_subdomains": num_subdomains,
        "suspicious_word_count": suspicious_word_count,
        "has_suspicious_tld": has_suspicious_tld,
        "url_depth": url_depth,
        "has_query_params": has_query,
        "label": label,
    }


def build_dataset(n_each=400):
    rows = []
    for _ in range(n_each):
        rows.append(extract_features(make_legit_url(), 0))
    for _ in range(n_each):
        rows.append(extract_features(make_phishing_url(), 1))
    random.shuffle(rows)
    return rows


if __name__ == "__main__":
    rows = build_dataset(n_each=450)
    fieldnames = list(rows[0].keys())
    with open("phishing_url_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    n_phish = sum(1 for r in rows if r["label"] == 1)
    n_legit = sum(1 for r in rows if r["label"] == 0)
    print(f"Total rows: {len(rows)} | phishing: {n_phish} | legit: {n_legit}")
