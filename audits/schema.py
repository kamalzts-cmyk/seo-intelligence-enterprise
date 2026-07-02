from bs4 import BeautifulSoup
import json, re
from audits.issue import add_issue

def collect_types(obj, found):
    if isinstance(obj, dict):
        t = obj.get("@type")
        if isinstance(t, str):
            found.append(t)
        elif isinstance(t, list):
            found.extend([x for x in t if isinstance(x, str)])
        for value in obj.values():
            collect_types(value, found)
    elif isinstance(obj, list):
        for item in obj:
            collect_types(item, found)

def extract_schema(html):
    soup = BeautifulSoup(html, "lxml")
    types = []
    invalid = 0
    blocks = 0

    for script in soup.find_all("script", attrs={"type": re.compile("ld\+json", re.I)}):
        raw = script.string or script.get_text() or ""
        if raw.strip():
            blocks += 1
            try:
                collect_types(json.loads(raw), types)
            except Exception:
                invalid += 1

    for node in soup.find_all(attrs={"itemscope": True}):
        itemtype = node.get("itemtype", "")
        if itemtype:
            types.append(itemtype.rstrip("/").split("/")[-1])

    return {"types": sorted(set(types)), "blocks": blocks, "invalid": invalid}

def detect_page_type(page):
    url = page["url"].lower()
    text = page["text"].lower()
    if any(x in text for x in ["add to cart", "sku", "in stock", "out of stock"]) or any(x in url for x in ["/product", "/shop"]):
        return "product"
    if "faq" in url or "frequently asked" in text:
        return "faq"
    if any(x in url for x in ["/blog", "/news", "/article"]):
        return "article"
    return "general"

def audit_schema(pages, issues):
    results = {}

    for page in pages:
        info = extract_schema(page["html"])
        url = page["url"]
        types = set(info["types"])
        ptype = detect_page_type(page)
        results[url] = info

        if info["blocks"] == 0 and not types:
            add_issue(issues, "Missing Structured Data", url, "No JSON-LD, Microdata or RDFa found")
            continue

        gaps = []
        if info["invalid"]:
            gaps.append(f"{info['invalid']} invalid schema block(s)")
        if page["depth"] == 0 and not ({"Organization", "LocalBusiness", "WebSite"} & types):
            gaps.append("Homepage lacks Organization/LocalBusiness/WebSite schema")
        if page["depth"] > 0 and "BreadcrumbList" not in types:
            gaps.append("BreadcrumbList schema missing")
        if ptype == "product" and "Product" not in types:
            gaps.append("Product schema missing on product/ecommerce page")
        if ptype == "faq" and "FAQPage" not in types:
            gaps.append("FAQPage schema missing")
        if ptype == "article" and not ({"Article", "BlogPosting"} & types):
            gaps.append("Article/BlogPosting schema missing")

        if gaps:
            add_issue(
                issues,
                "Incomplete Structured Data Implementation",
                url,
                "; ".join(gaps),
                "Detected Schema: " + (", ".join(info["types"]) or "None")
            )
        elif page["depth"] == 0 and "SearchAction" not in str(types):
            add_issue(
                issues,
                "Schema Enhancement Recommended for AI Search",
                url,
                "Consider WebSite SearchAction and richer entity linking",
                "Detected Schema: " + ", ".join(info["types"])
            )

    return results
