from urllib.parse import urljoin, urlparse, urldefrag
import re

def normalize_url(url):
    url = urldefrag((url or "").strip())[0]
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/")

def domain_from_url(url):
    host = urlparse(normalize_url(url)).netloc.lower()
    return host.replace("www.", "")

def same_domain(url, root_domain):
    host = domain_from_url(url)
    return host == root_domain or host.endswith("." + root_domain)

def absolute_url(base, href):
    return normalize_url(urljoin(base, href))

def clean_text(text):
    return " ".join((text or "").split())

def count_words(text):
    return len(re.findall(r"\b\w+\b", text or ""))
