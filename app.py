from flask import Flask, render_template, request, send_file
from config import APP_NAME, DEFAULT_MAX_PAGES
from crawler.crawler import crawl_site
from audits.technical import audit_technical
from audits.schema import audit_schema
from audits.content_ai import audit_content_ai
from audits.internal_links import audit_internal_links
from audits.backlinks import audit_backlinks
from scoring.scorer import build_scores
from exports.csv_export import issues_csv

app = Flask(__name__)
LAST_REPORT = None

def run_audit(url, max_pages):
    crawl = crawl_site(url, max_pages)
    issues = []

    technical = audit_technical(crawl["pages"], crawl["errors"], issues)
    schema = audit_schema(crawl["pages"], issues)
    content_ai = audit_content_ai(crawl["pages"], issues)
    internal_links = audit_internal_links(crawl["pages"], crawl["internal_links"], issues)
    backlinks = audit_backlinks(crawl["root_domain"], crawl["start_url"], issues)

    scores, severity, category = build_scores(issues, content_ai)

    return {
        "start_url": crawl["start_url"],
        "root_domain": crawl["root_domain"],
        "summary": {
            "pages": len(crawl["pages"]),
            "issues": len(issues),
            "internal_links": len(crawl["internal_links"]),
            "errors": len(crawl["errors"])
        },
        "scores": scores,
        "severity": severity,
        "category": category,
        "issues": issues,
        "technical": technical,
        "schema": schema,
        "content_ai": content_ai,
        "internal_links": internal_links,
        "backlinks": backlinks
    }

@app.route("/", methods=["GET", "POST"])
def index():
    global LAST_REPORT
    report = None
    url = ""
    max_pages = DEFAULT_MAX_PAGES

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        max_pages = int(request.form.get("max_pages", DEFAULT_MAX_PAGES))
        report = run_audit(url, max_pages)
        LAST_REPORT = report

    return render_template("index.html", app_name=APP_NAME, report=report, url=url, max_pages=max_pages)

@app.route("/export-csv")
def export_csv():
    if not LAST_REPORT:
        return "No report available", 400
    mem = issues_csv(LAST_REPORT)
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="seo-intelligence-pro-enterprise-v3.csv")

if __name__ == "__main__":
    app.run(debug=True)
