#!/usr/bin/env python3
"""
MRG Website — Batch Image Generator
Generates all 13 editorial images defined in image-prompts.json using KIE.ai
Nano Banana 2, converts them to WebP at quality 80, and saves them to ../assets/

Usage:
  cd mrg-website
  export KIE_API_KEY="your-kie-ai-api-key"
  python3 scripts/generate-images.py

  # Optional flags:
  python3 scripts/generate-images.py --only home-atmosphere.webp     # generate one
  python3 scripts/generate-images.py --skip-existing                  # skip files already in assets/
  python3 scripts/generate-images.py --quality 85                     # webp quality (default 80)
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("ERROR: Pillow not installed. Run: pip3 install Pillow\n")
    sys.exit(1)

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
ASSETS_DIR = PROJECT_DIR / "assets"
PROMPTS_FILE = SCRIPT_DIR / "image-prompts.json"

CREATE_URL = "https://api.kie.ai/api/v1/flux/generate"
POLL_URL = "https://api.kie.ai/api/v1/jobs/{task_id}"
POLL_INTERVAL = 5
TIMEOUT = 180


def get_api_key():
    key = os.environ.get("KIE_API_KEY", "").strip()
    if not key:
        sys.stderr.write(
            "ERROR: KIE_API_KEY environment variable not set.\n"
            "Set it before running:\n"
            "  export KIE_API_KEY=\"your-api-key-here\"\n"
            "  python3 scripts/generate-images.py\n"
        )
        sys.exit(1)
    return key


def http_post(url, payload, api_key):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def http_get(url, api_key):
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def extract_task_id(response):
    return (
        response.get("taskId")
        or response.get("task_id")
        or response.get("id")
        or (response.get("data") or {}).get("taskId")
    )


def extract_image_url(response):
    url = (
        response.get("imageUrl")
        or response.get("image_url")
        or response.get("output")
        or (response.get("data") or {}).get("imageUrl")
        or (response.get("data") or {}).get("image_url")
        or (response.get("data") or {}).get("output")
    )
    if isinstance(url, list):
        return url[0] if url else None
    return url


def extract_status(response):
    return (
        response.get("status")
        or (response.get("data") or {}).get("status")
        or ""
    ).lower()


def generate_one(prompt, size, api_key):
    payload = {"model": "nano-banana-2", "prompt": prompt, "size": size, "n": 1}

    try:
        result = http_post(CREATE_URL, payload, api_key)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"HTTP {e.code} creating task: {body}")

    task_id = extract_task_id(result)
    if not task_id:
        raise RuntimeError(f"No task ID in response: {json.dumps(result)}")

    elapsed = 0
    while elapsed < TIMEOUT:
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

        try:
            status_resp = http_get(POLL_URL.format(task_id=task_id), api_key)
        except urllib.error.HTTPError as e:
            print(f"    Poll error (HTTP {e.code}), retrying...")
            continue

        status = extract_status(status_resp)

        if status in ("completed", "success", "succeeded", "finished"):
            image_url = extract_image_url(status_resp)
            if not image_url:
                raise RuntimeError(f"Completed but no image URL: {json.dumps(status_resp)}")
            return image_url

        if status in ("failed", "error", "cancelled"):
            raise RuntimeError(f"Task failed: {json.dumps(status_resp)}")

        print(f"    Status: {status} ({elapsed}s)")

    raise RuntimeError(f"Timed out after {TIMEOUT}s. Task ID: {task_id}")


def download_and_save_webp(image_url, output_path, quality):
    with urllib.request.urlopen(image_url, timeout=60) as resp:
        image_bytes = resp.read()

    img = Image.open(BytesIO(image_bytes))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format="WEBP", quality=quality, method=6)
    return output_path.stat().st_size


def main():
    parser = argparse.ArgumentParser(description="Batch-generate MRG website images via KIE.ai Nano Banana 2.")
    parser.add_argument("--only", help="Generate only the named file (e.g. home-atmosphere.webp)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip files already present in assets/")
    parser.add_argument("--quality", type=int, default=80, help="WebP quality 1-100 (default 80)")
    args = parser.parse_args()

    api_key = get_api_key()

    if not PROMPTS_FILE.exists():
        sys.stderr.write(f"ERROR: prompts file not found: {PROMPTS_FILE}\n")
        sys.exit(1)

    with open(PROMPTS_FILE) as f:
        config = json.load(f)

    images = config.get("images", [])
    if args.only:
        images = [i for i in images if i["filename"] == args.only]
        if not images:
            sys.stderr.write(f"ERROR: no image with filename '{args.only}' in {PROMPTS_FILE}\n")
            sys.exit(1)

    total = len(images)
    print(f"\nMRG Website — Batch Image Generator")
    print(f"  Source: {PROMPTS_FILE.name}")
    print(f"  Output: {ASSETS_DIR}")
    print(f"  Quality: WebP @ {args.quality}")
    print(f"  Images to generate: {total}\n")

    succeeded = []
    failed = []
    skipped = []

    for idx, entry in enumerate(images, 1):
        filename = entry["filename"]
        prompt = entry["prompt"]
        output_path = ASSETS_DIR / filename

        print(f"[{idx}/{total}] {filename}")

        if args.skip_existing and output_path.exists():
            print(f"    Skipped (already exists)\n")
            skipped.append(filename)
            continue

        print(f"    Submitting to KIE.ai...")
        try:
            image_url = generate_one(prompt, config.get("size", "2k"), api_key)
            print(f"    Generated, downloading...")
            size_bytes = download_and_save_webp(image_url, output_path, args.quality)
            print(f"    Saved: {filename} ({size_bytes // 1024} KB)\n")
            succeeded.append(filename)
        except Exception as e:
            print(f"    FAILED: {e}\n")
            failed.append((filename, str(e)))

    print("=" * 60)
    print(f"Summary")
    print(f"  Succeeded: {len(succeeded)}")
    if succeeded:
        for f in succeeded:
            print(f"    + {f}")
    if skipped:
        print(f"  Skipped: {len(skipped)}")
        for f in skipped:
            print(f"    - {f}")
    if failed:
        print(f"  Failed: {len(failed)}")
        for f, err in failed:
            print(f"    x {f}: {err}")
    print("=" * 60)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
