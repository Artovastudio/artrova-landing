from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SITEMAP_FILE = PROJECT_ROOT / "sitemap.xml"

# عدّل هذا العنوان الأساسي لو تغيّر الدومين
BASE_URL = "https://artrovastudio.com"


URLS = [
    "",
    "#home",
    "#about",
    "#services",
    "#portfolio",
    "#future",
    "#contact",
]


def build_sitemap() -> str:
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">",
    ]
    for path in URLS:
        loc = BASE_URL.rstrip("/") + "/" + path.lstrip("#") if path else BASE_URL.rstrip("/") + "/"
        lines.extend(
            [
                "  <url>",
                f"    <loc>{loc}</loc>",
                f"    <lastmod>{now}</lastmod>",
                "    <changefreq>weekly</changefreq>",
                "    <priority>0.8</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> None:
    content = build_sitemap()
    SITEMAP_FILE.write_text(content, encoding="utf-8")
    print(f"تم إنشاء {SITEMAP_FILE} بنجاح. تأكد من إضافة رابطه في Google Search Console.")


if __name__ == "__main__":
    main()
