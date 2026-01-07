from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = PROJECT_ROOT / "index.html"

IMG_SRC_PATTERN = re.compile(r'src="([^\"]+)"')
PROJECT_IMAGE_PATTERN = re.compile(r"image:\s*'([^']+)'")


def collect_paths_from_html(text: str) -> set[str]:
    paths: set[str] = set()
    for m in IMG_SRC_PATTERN.finditer(text):
        paths.add(m.group(1))
    for m in PROJECT_IMAGE_PATTERN.finditer(text):
        paths.add(m.group(1))
    cleaned: set[str] = set()
    for p in paths:
        # استبعاد الروابط المطلقة (http/https)
        if p.startswith("http://") or p.startswith("https://"):
            continue
        # استبعاد المصادر الديناميكية الخاصة بـ Alpine مثل project.image
        if p.startswith("project."):
            continue
        cleaned.add(p)

    return cleaned


def main() -> None:
    if not INDEX_HTML.exists():
        print(f"[ERROR] لم يتم العثور على index.html في {PROJECT_ROOT}")
        return

    text = INDEX_HTML.read_text(encoding="utf-8", errors="ignore")
    paths = sorted(collect_paths_from_html(text))

    print(f"تم العثور على {len(paths)} مسار صورة في index.html\n")

    missing = []
    for rel in paths:
        fs_path = PROJECT_ROOT / rel
        if not fs_path.exists():
            missing.append((rel, fs_path))

    if not missing:
        print("✅ لا توجد صور مفقودة بحسب المسارات في index.html")
    else:
        print("❌ الصور التالية مساراتها غير موجودة:")
        for rel, fs_path in missing:
            print(f" - {rel}  ->  {fs_path}")


if __name__ == "__main__":
    main()
