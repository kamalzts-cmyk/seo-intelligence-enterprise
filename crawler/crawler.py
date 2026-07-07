from collections import deque
from bs4 import BeautifulSoup
import requests, time
from config import USER_AGENT, REQUEST_TIMEOUT
from crawler.utils import normalize_url, domain_from_url, same_domain, absolute_url, clean_text

def fetch(url):
    started = time.time()
    try:
        res = requests.get(
            url,
            timeout=8,
            allow_redirects=True,
            headers={"User-Agent": USER_AGENT}
        )
        return res, round(time.time() - started, 2), None
    except Exception as e:
        return None, round(time.time() - started, 2), str(e)

def parse_html_page(url, response, elapsed, depth):
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    visible = BeautifulSoup(html, "lxml")
    for tag in visible(["script", "style", "noscript"]):
        tag.decompose()
    text = clean_text(visible.get_text(" "))

    links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        links.append(absolute_url(response.url, href))

    return {
        "url": url,
        "final_url": normalize_url(response.url),
        "status": response.status_code,
        "response_time": elapsed,
        "depth": depth,
        "html": html,
        "text": text,
        "links": links,
        "content_type": response.headers.get("content-type", "")
    }

def crawl_site(start_url, max_pages):
    start_url = normalize_url(start_url)
    root = domain_from_url(start_url)
    queue = deque([(start_url, 0)])
    seen = set()
    pages = []
    errors = []
    internal_links = []

    while queue and len(seen) < max_pages:
        url, depth = queue.popleft()
        if url in seen or not same_domain(url, root):
            continue

        seen.add(url)
        res, elapsed, error = fetch(url)

        if error or not res:
            errors.append({"url": url, "status": 0, "error": error or "Request failed", "depth": depth})
            continue

        if res.status_code >= 400:
            errors.append({"url": url, "status": res.status_code, "error": f"HTTP {res.status_code}", "depth": depth})
            continue

        if "text/html" not in res.headers.get("content-type", ""):
            continue

        page = parse_html_page(url, res, elapsed, depth)
        pages.append(page)

        for link in page["links"]:
            if same_domain(link, root):
                internal_links.append({"source": url, "target": link})
                if link not in seen and len(queue) < max_pages * 5:
                    queue.append((link, depth + 1))

    return {
        "start_url": start_url,
        "root_domain": root,
        "pages": pages,
        "errors": errors,
        "internal_links": internal_links
    }
