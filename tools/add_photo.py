"""Add a photo to the photo album (photo.html).

Usage:
    python tools/add_photo.py path/to/image.jpg
    python tools/add_photo.py path/to/image.jpg --at 5      # insert as slide 5 (default: end)
    python tools/add_photo.py path/to/image.jpg --no-resize # keep original resolution

What it does:
    1. Copies the image into imgs/photo/ (resized to max 2400px, quality 85, unless --no-resize)
    2. Generates a 500x500 centre-cropped thumbnail in imgs/photo/thumbnails/
    3. Prompts for caption / location / year and appends the entry to jsons/photos.js

The website renders the album from jsons/photos.js, so no HTML editing is needed.
To reorder or edit captions later, edit jsons/photos.js directly.
"""
import argparse
import json
import os
import re
import shutil
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS_JS = os.path.join(ROOT, "jsons", "photos.js")
PHOTO_DIR = os.path.join(ROOT, "imgs", "photo")
THUMB_DIR = os.path.join(PHOTO_DIR, "thumbnails")

MAX_DIM = 2400
JPEG_QUALITY = 85
THUMB_SIZE = 500

HEADER = (
    "// Photo album data — one entry per photo, in display order.\n"
    "// img: file in imgs/photo/   thumb: file in imgs/photo/thumbnails/\n"
    "// caption: HTML allowed (<br>)   long: true = smaller caption font (long text)\n"
)


def load_photos():
    text = open(PHOTOS_JS, encoding="utf-8").read()
    m = re.search(r"window\.PHOTOS\s*=\s*(\[.*\]);", text, re.S)
    if not m:
        sys.exit(f"could not parse {PHOTOS_JS}")
    return json.loads(m.group(1))


def save_photos(photos):
    payload = json.dumps(photos, indent=2, ensure_ascii=False)
    with open(PHOTOS_JS, "w", encoding="utf-8") as f:
        f.write(HEADER + "window.PHOTOS = " + payload + ";\n")


def unique_name(directory, name):
    base, ext = os.path.splitext(name)
    candidate, i = name, 1
    while os.path.exists(os.path.join(directory, candidate)):
        candidate = f"{base}-{i}{ext}"
        i += 1
    return candidate


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("image", help="path to the photo to add")
    ap.add_argument("--at", type=int, default=None,
                    help="insert as slide number N (1-based); default appends at the end")
    ap.add_argument("--no-resize", action="store_true",
                    help="copy the image as-is instead of resizing to max %dpx" % MAX_DIM)
    args = ap.parse_args()

    if not os.path.exists(args.image):
        sys.exit(f"file not found: {args.image}")

    photos = load_photos()

    # --- main image ---
    img_name = unique_name(PHOTO_DIR, os.path.basename(args.image))
    dest = os.path.join(PHOTO_DIR, img_name)
    im = ImageOps.exif_transpose(Image.open(args.image))
    if args.no_resize:
        shutil.copy2(args.image, dest)
    else:
        im_copy = im.copy()
        im_copy.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
        im_copy.convert("RGB").save(dest, "JPEG", quality=JPEG_QUALITY,
                                    progressive=True, optimize=True)
    print(f"image     -> imgs/photo/{img_name} ({os.path.getsize(dest) // 1024} KB)")

    # --- thumbnail (500x500 centre crop) ---
    default_thumb = os.path.splitext(img_name)[0].lower() + "_thumb.jpg"
    thumb_name = input(f"thumbnail file name [{default_thumb}]: ").strip() or default_thumb
    if not thumb_name.lower().endswith(".jpg"):
        thumb_name += ".jpg"
    thumb_name = unique_name(THUMB_DIR, thumb_name)
    thumb = ImageOps.fit(im, (THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
    thumb.convert("RGB").save(os.path.join(THUMB_DIR, thumb_name), "JPEG",
                              quality=JPEG_QUALITY, optimize=True)
    print(f"thumbnail -> imgs/photo/thumbnails/{thumb_name}")

    # --- metadata ---
    caption = input("caption (HTML <br> allowed): ").strip()
    location = input("location (e.g. 'Zermatt, Switzerland'): ").strip()
    year = input("year: ").strip()
    long_flag = len(re.sub(r"<[^>]+>", "", caption)) > 110
    if long_flag:
        print("(caption is long — using the smaller 'long_desc' font)")

    entry = {
        "img": img_name,
        "caption": caption,
        "credit": f"{location} · {year}",
        "long": long_flag,
        "thumb": thumb_name,
    }

    pos = len(photos) if args.at is None else max(0, min(args.at - 1, len(photos)))
    photos.insert(pos, entry)
    save_photos(photos)
    print(f"added as slide {pos + 1} of {len(photos)} -> jsons/photos.js")


if __name__ == "__main__":
    main()
