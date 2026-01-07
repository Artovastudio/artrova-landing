import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


PROJECT_ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIRS = [
    PROJECT_ROOT / "images",
    PROJECT_ROOT / "assets" / "images",
]

OUTPUT_ROOT = PROJECT_ROOT / "optimized_images"


def iter_images():
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    for base in IMAGE_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.suffix.lower() in exts and path.is_file():
                rel = path.relative_to(PROJECT_ROOT)
                yield path, rel


def optimize_image(src: Path, dst: Path, quality: int = 80) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im_format = "WEBP" if im.format != "WEBP" else im.format
        # نحافظ على وضع الألوان
        save_kwargs = {
            "optimize": True,
            "quality": quality,
        }
        if im_format == "JPEG":
            save_kwargs["progressive"] = True
        im.convert("RGB").save(dst.with_suffix(".webp"), im_format, **save_kwargs)


def main():
    if Image is None:
        print("[ERROR] مكتبة Pillow غير مثبتة. ثبّتها أولاً:")
        print("       pip install pillow")
        sys.exit(1)

    quality = 80
    if len(sys.argv) > 1:
        try:
            quality = int(sys.argv[1])
        except ValueError:
            print("استخدم رقمًا للجودة بين 50 و 95، المثال: python optimize_images.py 80")
            sys.exit(1)

    print(f"جذر المشروع: {PROJECT_ROOT}")
    print(f"سيتم حفظ الصور المضغوطة في: {OUTPUT_ROOT}")
    print(f"جودة الضغط: {quality}")

    count = 0
    for src, rel in iter_images():
        dst = OUTPUT_ROOT / rel
        try:
            optimize_image(src, dst, quality=quality)
            count += 1
        except Exception as e:  # pragma: no cover
            print(f"[WARN] تعذر ضغط {src}: {e}")

    print(f"\nتم إنشاء {count} صورة مضغوطة في مجلد optimized_images دون تعديل الأصل.")


if __name__ == "__main__":
    main()
