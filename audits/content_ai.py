from bs4 import BeautifulSoup
from audits.issue import add_issue
from crawler.utils import count_words

QUESTION_STARTERS = ["what", "why", "how", "when", "where", "which", "can", "does", "is", "are", "cost", "best", "compare"]
TRUST_TERMS = ["about us", "contact", "privacy policy", "terms", "testimonial", "review", "case study", "certified", "award", "years of experience", "expert"]
PROOF_TERMS = ["according to", "source", "research", "study", "data", "report", "evidence", "case study", "results"]

def audit_content_ai(pages, issues):
    results = {}

    for page in pages:
        soup = BeautifulSoup(page["html"], "lxml")
        url = page["url"]
        text = page["text"]
        lower = text.lower()
        wc = count_words(text)

        headings = [h.get_text(" ", strip=True) for h in soup.find_all(["h1","h2","h3"])]
        q_headings = [h for h in headings if "?" in h or any(h.lower().startswith(q + " ") for q in QUESTION_STARTERS)]
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        answer_blocks = [p for p in paragraphs if 25 <= len(p.split()) <= 90]
        has_trust = any(t in lower for t in TRUST_TERMS)
        has_proof = any(t in lower for t in PROOF_TERMS)
        ext_links = [a.get("href","") for a in soup.find_all("a", href=True) if a.get("href","").startswith(("http://","https://")) and page["url"].split("/")[2] not in a.get("href","")]

        content_score = 100
        aeo_score = 100
        geo_score = 100
        eeat_score = 100

        if wc < 250:
            content_score -= 35
        elif wc < 500:
            content_score -= 15

        if len(headings) < 3 and wc > 300:
            add_issue(issues, "Weak Content Structure", url, f"Only {len(headings)} heading(s)")
            content_score -= 15

        if not q_headings:
            add_issue(issues, "Missing AEO Signals", url, "No question-led headings or FAQ-style sections found")
            aeo_score -= 45

        if q_headings and len(answer_blocks) < 2:
            add_issue(issues, "Weak AEO Answer Structure", url, "Question intent exists but concise extractable answers are limited")
            aeo_score -= 25

        if not has_trust:
            add_issue(issues, "Missing E-E-A-T Signals", url, "No strong trust, ownership or credibility signals detected")
            eeat_score -= 40

        if not has_proof and not ext_links:
            add_issue(issues, "Missing GEO Signals", url, "No evidence, citations, external references or source signals detected")
            geo_score -= 45

        results[url] = {
            "word_count": wc,
            "heading_count": len(headings),
            "question_heading_count": len(q_headings),
            "answer_block_count": len(answer_blocks),
            "external_link_count": len(ext_links),
            "content_score": max(0, content_score),
            "aeo_score": max(0, aeo_score),
            "geo_score": max(0, geo_score),
            "eeat_score": max(0, eeat_score)
        }

    return results
