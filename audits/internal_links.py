from collections import Counter
from audits.issue import add_issue

def audit_internal_links(pages, links, issues):
    incoming = Counter([l["target"] for l in links])
    outgoing = Counter([l["source"] for l in links])
    results = {}

    for page in pages:
        url = page["url"]
        results[url] = {
            "incoming": incoming[url],
            "outgoing": outgoing[url],
            "depth": page["depth"]
        }

        if page["depth"] > 0 and incoming[url] < 2:
            add_issue(issues, "Low Internal Link Equity", url, f"{incoming[url]} incoming internal link(s)")

    return results
