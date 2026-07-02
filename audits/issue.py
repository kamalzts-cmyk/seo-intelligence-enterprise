GUIDES = {
    "HTTP Error": ("Critical","Crawlability"),
    "Missing Title": ("Critical","On-Page SEO"),
    "Title Too Short": ("Medium","On-Page SEO"),
    "Duplicate Title": ("High","On-Page SEO"),
    "Missing Meta Description": ("High","On-Page SEO"),
    "Missing H1": ("High","On-Page SEO"),
    "Multiple H1": ("Medium","On-Page SEO"),
    "Missing Canonical": ("Medium","Indexability"),
    "Noindex Found": ("Critical","Indexability"),
    "Low Word Count": ("Medium","Content"),
    "Weak Content Structure": ("Medium","Content"),
    "Images Missing ALT": ("Low","Image SEO"),
    "Missing Structured Data": ("High","Schema & AI Search"),
    "Incomplete Structured Data Implementation": ("Medium","Schema & AI Search"),
    "Schema Enhancement Recommended for AI Search": ("Low","Schema & AI Search"),
    "Missing AEO Signals": ("High","AEO"),
    "Weak AEO Answer Structure": ("Medium","AEO"),
    "Missing GEO Signals": ("High","GEO"),
    "Missing E-E-A-T Signals": ("High","E-E-A-T"),
    "Slow Response": ("High","Performance"),
    "Low Internal Link Equity": ("Medium","Internal Linking"),
    "Backlink Data Not Connected": ("High","Backlinks"),
    "Low Referring Domains": ("High","Backlinks"),
    "Weak Anchor Text Diversity": ("Medium","Backlinks"),
}

WHY = {
    "Backlink Data Not Connected": "Backlinks are an external authority signal and cannot be measured accurately without access to a backlink index.",
    "Low Referring Domains": "A low referring domain profile limits authority, trust and competitive ranking power.",
    "Weak Anchor Text Diversity": "Over-reliance on repetitive anchors can create risk and weak topical authority signals."
}

def add_issue(issues, name, url, detail="", evidence=""):
    severity, category = GUIDES.get(name, ("Medium", "General"))
    issues.append({
        "issue": name,
        "severity": severity,
        "category": category,
        "url": url,
        "detail": detail,
        "evidence": evidence,
        "why": WHY.get(name, "This issue affects search visibility, crawlability, AI understanding, user experience or conversion efficiency."),
        "root": "Detected through automated crawl and page-level intelligence checks.",
        "fix": "Prioritize this based on severity, affected URL value and business impact.",
        "developer": "Update CMS templates, page content, structured data or technical configuration as required.",
        "ai": "Improve clarity, entity relationships, answer extraction and citation readiness.",
        "best": "Follow Google Search guidance, Schema.org standards and evidence-led content practices.",
        "reference": "https://developers.google.com/search/docs"
    })
