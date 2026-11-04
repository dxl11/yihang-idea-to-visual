#!/usr/bin/env python3
"""One-off generator for original demo reference PNGs (not third-party works)."""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / ".agents/skills/yihang-idea-to-visual/assets/visual-reference-library"

SAMPLES = {
    "editorial/demo-editorial-grid.png": ((1080, 1350), "#F4F1EA", "#1F4B99", "grid"),
    "minimalism/demo-minimal-balance.png": ((1080, 1350), "#FFFFFF", "#222222", "minimal"),
    "technology/demo-tech-nodes.png": ((1080, 1350), "#0B1C2C", "#3DE0FF", "tech"),
    "artistic/demo-artistic-wash.png": ((1080, 1350), "#F7EDE3", "#C45C26", "artistic"),
    "infographic/demo-info-blocks.png": ((1080, 1350), "#F5F7FA", "#2F6FED", "info"),
    "photography/demo-photo-blocks.png": ((1080, 1080), "#D9D2C5", "#5A4634", "photo"),
    "typography/demo-big-type-blocks.png": ((1080, 1350), "#111111", "#F2F2F2", "type"),
    "miscellaneous/demo-misc-shapes.png": ((1080, 1350), "#EEF2F5", "#6B7C93", "misc"),
}


def main() -> None:
    for rel, (size, bg, fg, kind) in SAMPLES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", size, bg)
        d = ImageDraw.Draw(img)
        w, h = size
        if kind == "grid":
            for i in range(1, 4):
                y = int(h * i / 4)
                d.line([(80, y), (w - 80, y)], fill=fg, width=3)
            d.rectangle([80, 80, w - 80, 160], outline=fg, width=4)
        elif kind == "minimal":
            d.rectangle([w // 2 - 2, 120, w // 2 + 2, h - 120], fill=fg)
            d.ellipse([w // 2 - 60, 160, w // 2 + 60, 280], outline=fg, width=4)
        elif kind == "tech":
            for i in range(6):
                x = 120 + i * 140
                d.ellipse([x, h // 2 - 20, x + 40, h // 2 + 20], outline=fg, width=3)
                if i < 5:
                    d.line([x + 40, h // 2, x + 140, h // 2], fill=fg, width=2)
            d.rectangle([80, 80, 220, 120], fill=fg)
        elif kind == "artistic":
            d.ellipse([120, 200, 520, 600], fill=fg)
            d.ellipse([400, 450, 900, 1000], outline=fg, width=8)
        elif kind == "info":
            y = 160
            for i in range(4):
                d.rectangle([120, y, 120 + (i + 1) * 160, y + 80], fill=fg)
                y += 140
        elif kind == "photo":
            d.rectangle([80, 80, w - 80, h - 80], outline=fg, width=6)
            d.rectangle([140, 140, w - 140, h // 2], fill=fg)
        elif kind == "type":
            d.rectangle([80, 200, w - 80, 360], fill=fg)
            d.rectangle([80, 420, int(w * 0.55), 500], fill=fg)
            d.rectangle([80, 560, int(w * 0.35), 620], fill=fg)
        else:
            d.polygon([(200, 200), (500, 180), (650, 450), (300, 600)], fill=fg)
            d.rectangle([700, 700, 980, 980], outline=fg, width=5)
        img.save(path)
        print("wrote", path)

    svg = ROOT / "editorial" / "demo-editorial-sketch.svg"
    svg.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#F4F1EA"/>
  <rect x="40" y="40" width="320" height="36" fill="none" stroke="#1F4B99" stroke-width="4"/>
  <line x1="40" y1="140" x2="360" y2="140" stroke="#1F4B99" stroke-width="3"/>
  <line x1="40" y1="220" x2="360" y2="220" stroke="#1F4B99" stroke-width="3"/>
  <text x="40" y="480" font-size="14" fill="#1F4B99">Original demo sketch — not a third-party work</text>
</svg>
""",
        encoding="utf-8",
    )
    print("wrote", svg)


if __name__ == "__main__":
    main()
