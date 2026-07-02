from collections import Counter
from statistics import mean

PENALTY = {
    "Critical": 10,
    "High": 6,
    "Medium": 3,
    "Low": 1
}

def score_issues(issues, categories=None):
    relevant = [i for i in issues if categories is None or i["category"] in categories]
    penalty = sum(PENALTY.get(i["severity"], 1) for i in relevant)
    return max(0, round(100 - penalty))

def avg(items, key):
    values = [v.get(key, 100) for v in items.values()]
    return round(mean(values)) if values else 100

def build_scores(issues, content_results):
    severity = Counter([i["severity"] for i in issues])
    category = Counter([i["category"] for i in issues])

    scores = {
        "SEO Health": score_issues(issues),
        "Technical": score_issues(issues, ["Crawlability", "Indexability", "On-Page SEO"]),
        "Content": min(score_issues(issues, ["Content"]), avg(content_results, "content_score")),
        "Schema": score_issues(issues, ["Schema & AI Search"]),
        "AEO": min(score_issues(issues, ["AEO"]), avg(content_results, "aeo_score")),
        "GEO": min(score_issues(issues, ["GEO"]), avg(content_results, "geo_score")),
        "AI Visibility": score_issues(issues, ["AEO", "GEO", "Schema & AI Search", "E-E-A-T"]),
        "E-E-A-T": min(score_issues(issues, ["E-E-A-T"]), avg(content_results, "eeat_score")),
        "Performance": score_issues(issues, ["Performance"]),
        "Internal Links": score_issues(issues, ["Internal Linking"]),
        "Backlinks": score_issues(issues, ["Backlinks"])
    }

    return scores, dict(severity), dict(category)
