import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = PROJECT_ROOT / "index.html"

GA_PLACEHOLDER = "G-XXXXXXXXXX"  # استبدله بمعرف GA4 الحقيقي عند التشغيل


def inject_search_console_meta(html: str, verification_code: str) -> str:
    """أضف وسم التحقق من Google Search Console داخل <head> إن لم يكن موجوداً."""
    if not verification_code:
        return html

    meta_tag = f'    <meta name="google-site-verification" content="{verification_code}">\n'

    if "google-site-verification" in html:
        # موجود مسبقًا، لا نضيف شيئًا
        return html

    # نحاول الإدراج بعد وسم <meta name="viewport"> إن وجد، وإلا في بداية <head>
    viewport_str = '<meta name="viewport"'
    idx = html.find(viewport_str)
    if idx != -1:
        end = html.find('\n', idx)
        if end != -1:
            return html[: end + 1] + meta_tag + html[end + 1 :]

    head_str = "<head>"
    idx = html.find(head_str)
    if idx != -1:
        insert_pos = idx + len(head_str)
        return html[: insert_pos] + "\n" + meta_tag + html[insert_pos:]

    return html


def inject_ga4_snippet(html: str, measurement_id: str) -> str:
    """أضف كود GA4 قبل </head> إن لم يكن موجوداً."""
    if not measurement_id:
        return html

    if "gtag/js?id=" in html or "Google Analytics" in html:
        # يوجد كود أناليتكس مسبقاً
        return html

    snippet = f"""    <!-- Google Analytics 4 -->
    <script async src=\"https://www.googletagmanager.com/gtag/js?id={measurement_id}\"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{measurement_id}');
    </script>
"""

    closing_head = "</head>"
    idx = html.lower().find(closing_head)
    if idx != -1:
        return html[:idx] + snippet + html[idx:]

    return html


def run_generate_sitemap() -> None:
    script = PROJECT_ROOT / "tools" / "generate_sitemap.py"
    if not script.exists():
        print("[INFO] generate_sitemap.py غير موجود، لن يتم إنشاء sitemap.xml تلقائياً.")
        return
    try:
        subprocess.run(["python", str(script)], check=True)
    except Exception as e:  # pragma: no cover
        print(f"[WARN] تعذر تشغيل generate_sitemap.py: {e}")


def main() -> None:
    if not INDEX_HTML.exists():
        print(f"[ERROR] لم يتم العثور على index.html في {PROJECT_ROOT}")
        return

    print("هذا السكربت يساعدك في حقن وسم التحقق من Google Search Console وكود Google Analytics 4 في index.html.")
    print("يمكنك تشغيله أكثر من مرة، ولن يكرر الأكواد إن كانت موجودة بالفعل.\n")

    site_url = input("أدخل رابط موقعك (GitHub Pages أو غيره)، مثال: https://artrovastudio.github.io/artrova-landing/\n> ").strip()
    if site_url:
        print(f"سيتم استخدام هذا الرابط في sitemap.xml (عبر generate_sitemap.py) إن قمت بتشغيله.")

    verification_code = input("\nأدخل قيمة google-site-verification من Google Search Console (أو اتركه فارغاً لتخطي الخطوة):\n> ").strip()
    measurement_id = input("\nأدخل Google Analytics 4 Measurement ID (مثل G-XXXXXXXXXX) أو اتركه فارغاً لتخطي الخطوة:\n> ").strip()

    html = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")

    if verification_code:
        html = inject_search_console_meta(html, verification_code)
        print("- تم تجهيز وسم التحقق من Search Console (إن لم يكن موجوداً).")

    if measurement_id:
        html = inject_ga4_snippet(html, measurement_id)
        print("- تم تجهيز كود Google Analytics 4 (إن لم يكن موجوداً).")

    INDEX_HTML.write_text(html, encoding="utf-8")
    print("\n✅ تم تحديث index.html بنجاح.")

    use_sitemap = input("\nهل تريد توليد sitemap.xml الآن باستخدام generate_sitemap.py؟ (y/n): ").strip().lower()
    if use_sitemap == "y":
        run_generate_sitemap()

    print("\nانتهى السكربت. يمكنك الآن رفع التعديلات إلى GitHub.")


if __name__ == "__main__":
    main()
