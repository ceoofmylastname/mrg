# scripts/

Local utility scripts for the MRG Accounting Service website.

## `generate-images.py`

Batch-generates all editorial WebP images defined in `image-prompts.json` using KIE.ai's Nano Banana 2 model. Downloads each result, converts to WebP, and saves into `../assets/` with the exact filenames the website expects.

### One-time setup

1. **Install Pillow** (for WebP conversion):
   ```bash
   pip3 install Pillow
   ```

2. **Set your KIE.ai API key as an environment variable.** You can either export it inline for one session, or add it to your shell profile (`~/.zshrc`):

   ```bash
   export KIE_API_KEY="your-kie-ai-api-key-here"
   ```

### Generate all 13 images

From the `mrg-website/` directory:

```bash
python3 scripts/generate-images.py
```

Takes ~5 minutes total. Each image takes 20–45 seconds to generate.

### Optional flags

```bash
# Skip images that already exist in assets/ (resume mode)
python3 scripts/generate-images.py --skip-existing

# Generate only one specific image
python3 scripts/generate-images.py --only home-atmosphere.webp

# Change WebP compression quality (default 80, valid 1-100)
python3 scripts/generate-images.py --quality 85
```

### Editing prompts

Prompts live in `image-prompts.json`. Edit any prompt or filename and re-run the script (use `--only` to regenerate just that one). The website HTML references filenames directly, so as long as the filename stays the same, the page picks up the new image automatically on the next refresh.

### Cost

Approximately $0.10–$0.30 per image at KIE.ai's Nano Banana 2 rate. Full batch (13 images) runs about $2–$4.

### After generation

```bash
cd ..
git add assets/
git commit -m "Add editorial imagery"
git push
```

Live site updates within seconds on Netlify/Vercel.
