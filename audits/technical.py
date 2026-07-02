from bs4 import BeautifulSoup
from collections import Counter
import re
from audits.issue import add_issue
from crawler.utils import count_words

def audit_technical(pages, errors, issues):
    facts = []

    for e in errors:
        add_issue(issues, "HTTP Error", e["url"], e.get("error", ""))

    for page in pages:
        soup = BeautifulSoup(page["html"], "lxml")
        url = page["url"]

        title = soup.title.get_text(strip=True) if soup.title else ""
        desc_tag = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
        desc = desc_tag.get("content","").strip() if desc_tag else ""
        h1s = soup.find_all("h1")
        canonical = soup.find("link", rel=lambda x: x and "canonical" in x)
        robots = soup.find("meta", attrs={"name": re.compile("^robots$", re.I)})
        robots_content = robots.get("content", "").lower() if robots else ""
        imgs = soup.find_all("img")
        missing_alt = [img for img in imgs if not img.has_attr("alt") or not img.get("alt","").strip()]
        wc = count_words(page["text"])

        facts.append({
            "url": url,
            "title": title,
            "description": desc,
            "word_count": wc,
            "h1_count": len(h1s),
            "canonical": canonical.get("href","").strip() if canonical else "",
            "response_time": page["response_time"],
            "missing_alt": len(missing_alt)
        })

        if page["response_time"] > 2.5:
            add_issue(issues, "Slow Response", url, f"{page['response_time']} seconds")
        if not title:
            add_issue(issues, "Missing Title", url)
        elif len(title) < 25:
            add_issue(issues, "Title Too Short", url, f"{len(title)} characters")
        if not desc:
            add_issue(issues, "Missing Meta Description", url)
        if len(h1s) == 0:
            add_issue(issues, "Missing H1", url)
        if len(h1s) > 1:
            add_issue(issues, "Multiple H1", url, f"{len(h1s)} H1 tags")
        if not canonical:
            add_issue(issues, "Missing Canonical", url)
        if "noindex" in robots_content:
            add_issue(issues, "Noindex Found", url)
        if len(missing_alt) > 0:
            add_issue(issues, "Images Missing ALT", url, f"{len(missing_alt)} image(s)")
        if wc < 250:
            add_issue(issues, "Low Word Count", url, f"{wc} words")

    title_counts = Counter([f["title"] for f in facts if f["title"]])
    for f in facts:
        if f["title"] and title_counts[f["title"]] > 1:
            add_issue(issues, "Duplicate Title", f["url"], f["title"])

    return facts
