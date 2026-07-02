import requests
from config import DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD

BASE = "https://api.dataforseo.com/v3"

def connected():
    return bool(DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD)

def post(endpoint, payload):
    url = BASE + endpoint
    response = requests.post(
        url,
        auth=(DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD),
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()

def get_backlink_summary(domain):
    if not connected():
        return {"connected": False}

    payload = [{
        "target": domain,
        "internal_list_limit": 10,
        "include_subdomains": True
    }]

    data = post("/backlinks/summary/live", payload)
    task = data.get("tasks", [{}])[0]
    result = (task.get("result") or [{}])[0]

    return {
        "connected": True,
        "target": domain,
        "backlinks": result.get("backlinks"),
        "referring_domains": result.get("referring_domains"),
        "referring_pages": result.get("referring_pages"),
        "dofollow": result.get("dofollow"),
        "nofollow": result.get("nofollow"),
        "rank": result.get("rank"),
        "spam_score": result.get("spam_score"),
        "raw": result
    }

def get_anchor_texts(domain):
    if not connected():
        return []

    payload = [{
        "target": domain,
        "limit": 25,
        "include_subdomains": True
    }]

    data = post("/backlinks/anchors/live", payload)
    task = data.get("tasks", [{}])[0]
    result = task.get("result") or []
    anchors = []

    for block in result:
        for item in block.get("items", [])[:25]:
            anchors.append({
                "anchor": item.get("anchor"),
                "backlinks": item.get("backlinks"),
                "referring_domains": item.get("referring_domains")
            })

    return anchors
