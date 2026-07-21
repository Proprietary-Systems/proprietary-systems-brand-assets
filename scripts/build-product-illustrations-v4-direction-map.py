#!/usr/bin/env python3
"""Build the labeled V4 direction map from the selected ImageGen concept.

This is an approval artifact, not the production icon export. The selected
contact-sheet cells are shown with their intended product labels so semantic
collisions can be reviewed before native SVG reconstruction begins.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "reference" / "product-illustration-v4" / "selected-flat-object-direction.png"
OUTPUT = ROOT / "preview" / "product-illustrations-v4-direction-map.png"

PRODUCTS = [
    ("Peter.ai", "AI assistant", "PLATFORM"),
    ("PS CRM", "contact records", "PLATFORM"),
    ("PS Prospect", "prospect search", "PLATFORM"),
    ("PS Outreach", "sequenced sending", "PLATFORM"),
    ("PS Dialer", "calling and keypad", "STANDALONE"),
    ("PS Contracts", "agreement approval", "PLATFORM"),
    ("PS Email Signatures", "employee email identity", "SUITE · BOUNDED RUNTIME"),
    ("PS Finance", "forecast and growth", "PLATFORM"),
    ("PS People", "organization and HCM", "PLATFORM"),
    ("PS Docs", "document creation", "PLATFORM"),
    ("PS Automate", "connected actions", "PLATFORM"),
    ("PS Sites", "web publishing", "PLATFORM"),
    ("PS Projects", "tasks and delivery", "PLATFORM"),
    ("PS Portal", "unified gateway", "PLATFORM"),
    ("PS Territory", "route and coverage", "PLATFORM"),
    ("PS Places", "property intelligence", "SUITE · BOUNDED RUNTIME"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size, index=1 if bold and path.suffix == ".ttc" else 0)
    return ImageFont.load_default(size=size)


def crop_grid(source: Image.Image) -> list[Image.Image]:
    # The generated reference has deliberately loose whitespace rather than a
    # hard mathematical grid. Crop around measured optical centers so nearby
    # objects never bleed into the next product cell.
    centers_x = (181, 531, 879, 1217)
    centers_y = (177, 430, 687, 918)
    crop_width, crop_height = 330, 250
    cells: list[Image.Image] = []
    for center_y in centers_y:
        for center_x in centers_x:
            left = center_x - crop_width // 2
            top = center_y - crop_height // 2
            right = left + crop_width
            bottom = top + crop_height
            cells.append(source.crop((left, top, right, bottom)).convert("RGBA"))
    return cells


def contain(image: Image.Image, width: int, height: int) -> Image.Image:
    copy = image.copy()
    copy.thumbnail((width, height), Image.Resampling.LANCZOS)
    return copy


def draw_card(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    image: Image.Image,
    x: int,
    y: int,
    title: str,
    meaning: str,
    classification: str,
    independent: bool = False,
) -> None:
    card_w, card_h = 400, 350
    fill = "#FFFFFF" if not independent else "#F8FBF7"
    outline = "#D6E6E5" if not independent else "#D9E5D6"
    draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=26, fill=fill, outline=outline, width=2)
    art = contain(image, 354, 242)
    canvas.paste(art, (x + (card_w - art.width) // 2, y + 10), art)
    draw.text((x + 24, y + 266), title, font=font(23, True), fill="#0A2030")
    draw.text((x + 24, y + 299), meaning, font=font(16), fill="#5F777D")
    badge_color = "#5B7A35" if independent else "#0097A7"
    draw.text((x + 24, y + 328), classification, font=font(12, True), fill=badge_color)


def main() -> None:
    selected = Image.open(REFERENCE).convert("RGB")
    cells = crop_grid(selected)
    width, cols, card_w, card_h, gap = 1800, 4, 400, 350, 28
    top = 212
    product_rows = 4
    height = top + product_rows * card_h + (product_rows - 1) * gap + 94
    canvas = Image.new("RGB", (width, height), "#EEF5F4")
    draw = ImageDraw.Draw(canvas)

    draw.text((72, 50), "Flat-object product system · V4 direction map", font=font(40, True), fill="#0A2030")
    draw.text((72, 105), "One literal metaphor per product · two-color geometry · recognition before decoration", font=font(20), fill="#557279")
    swatches = [("#0A2030", "navy"), ("#0097A7", "teal"), ("#00E5C2", "mint"), ("#E6F2F2", "mist")]
    swatch_x = 72
    for color, label in swatches:
        draw.rounded_rectangle((swatch_x, 151, swatch_x + 25, 176), radius=7, fill=color)
        draw.text((swatch_x + 35, 151), label, font=font(14), fill="#6B8186")
        swatch_x += 118

    start_x = (width - (cols * card_w + (cols - 1) * gap)) // 2
    for index, ((title, meaning, classification), image) in enumerate(zip(PRODUCTS, cells)):
        row, column = divmod(index, cols)
        x = start_x + column * (card_w + gap)
        y = top + row * (card_h + gap)
        draw_card(canvas, draw, image, x, y, title, meaning, classification)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
