from audits.issue import add_issue
from integrations.dataforseo_backlinks import connected, get_backlink_summary, get_anchor_texts

def audit_backlinks(root_domain, start_url, issues):
    if not connected():
        add_issue(
            issues,
            "Backlink Data Not Connected",
            start_url,
            "Add DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD in Render environment variables"
        )
        return {
            "connected": False,
            "provider": "DataForSEO",
            "domain": root_domain,
            "note": "Real backlink data requires DataForSEO credentials. No fake backlink metrics are shown."
        }

    try:
        summary = get_backlink_summary(root_domain)
        anchors = get_anchor_texts(root_domain)
        summary["anchors"] = anchors

        rd = summary.get("referring_domains") or 0
        if rd < 25:
            add_issue(issues, "Low Referring Domains", start_url, f"Only {rd} referring domains found via DataForSEO")

        anchor_names = [a.get("anchor") for a in anchors if a.get("anchor")]
        if len(set(anchor_names)) < 5 and len(anchor_names) > 0:
            add_issue(issues, "Weak Anchor Text Diversity", start_url, f"Only {len(set(anchor_names))} unique anchors in top sample")

        return summary

    except Exception as e:
        add_issue(issues, "Backlink Data Not Connected", start_url, f"DataForSEO request failed: {str(e)}")
        return {
            "connected": False,
            "provider": "DataForSEO",
            "domain": root_domain,
            "error": str(e)
        }
