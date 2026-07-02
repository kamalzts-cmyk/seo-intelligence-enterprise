# SEO Intelligence Pro Enterprise V3

Render-ready SEO audit platform with:

- Technical SEO crawler
- On-page SEO checks
- Schema + AI Search structured data audit
- AEO scoring
- GEO scoring
- E-E-A-T scoring
- Content quality scoring
- Internal link intelligence
- Backlink intelligence via DataForSEO API
- CSV export
- Modular architecture

## Important Backlink Note

Real backlink data requires a backlink index. This version supports DataForSEO API.

Add these environment variables in Render:

DATAFORSEO_LOGIN
DATAFORSEO_PASSWORD

Without API credentials, the backlink module will clearly show that backlink data is not connected instead of inventing fake metrics.

## Render Deploy

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app
