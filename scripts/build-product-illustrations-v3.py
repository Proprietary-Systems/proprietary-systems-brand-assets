#!/usr/bin/env python3
"""Build the theme-aware V3 Proprietary Systems product illustration system.

V2 remains the editable composition source for the original products. This
builder adds the shared V3 atmosphere, performs attribute-aware color
adaptation for dark mode, adds the new Places master, renders QA previews, and
creates contact sheets. Generated SVGs remain native, editable vector markup.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "svg" / "product-illustrations-v2"
V3 = ROOT / "svg" / "product-illustrations-v3"
MASTERS = V3 / "masters"
LIGHT = V3 / "light"
DARK = V3 / "dark"
PREVIEW = ROOT / "preview" / "product-illustrations-v3"

PRODUCTS = [
    ("peter-ai", "Peter.ai", "platform"),
    ("ps-crm", "PS CRM", "platform"),
    ("ps-prospect", "PS Prospect", "platform"),
    ("ps-outreach", "PS Outreach", "platform"),
    ("ps-dialer", "PS Dialer", "standalone"),
    ("ps-contracts", "PS Contracts", "platform"),
    ("ps-signatures", "PS Signatures", "standalone"),
    ("ps-finance", "PS Finance", "platform"),
    ("ps-people", "PS People", "platform"),
    ("ps-docs", "PS Docs", "platform"),
    ("ps-automate", "PS Automate", "platform"),
    ("ps-sites", "PS Sites", "platform"),
    ("ps-projects", "PS Projects", "platform"),
    ("ps-portal", "PS Portal", "platform"),
    ("ps-territory", "PS Territory", "platform"),
    ("ps-places", "Proprietary Places", "standalone"),
]

ACCENTS = {
    "peter-ai": "#7C5CFC",
    "ps-crm": "#5B8DEF",
    "ps-prospect": "#5B8DEF",
    "ps-outreach": "#7C5CFC",
    "ps-dialer": "#F4B740",
    "ps-contracts": "#F4B740",
    "ps-signatures": "#7C5CFC",
    "ps-finance": "#00E5C2",
    "ps-people": "#FF7A66",
    "ps-docs": "#F4B740",
    "ps-automate": "#7C5CFC",
    "ps-sites": "#5B8DEF",
    "ps-projects": "#FF7A66",
    "ps-portal": "#7C5CFC",
    "ps-territory": "#5B8DEF",
    "ps-places": "#00E5C2",
}

DARK_FILL_MAP = {
    "#FFFFFF": "#163845",
    "#F6FBFB": "#12313D",
    "#E6F2F2": "#173B47",
    "#D9ECEB": "#1A414C",
    "#D4E9E8": "#1A414C",
    "#D3E6E6": "#1B424D",
    "#C8E7E5": "#28545D",
    "#B7DAD8": "#2A5961",
    "#A9CFCD": "#24505A",
    "#85BDBB": "#1F4B55",
    "#7FB7B7": "#1D4852",
    "#7EB6B5": "#1D4852",
    "#0A2030": "#103744",
    "#073947": "#0C2E3A",
    "#052F3B": "#092832",
}

DARK_ACCENT_MAP = {
    "#0097A7": "#00AFC0",
    "#00A9AA": "#00BFC0",
    "#5B8DEF": "#78A4FF",
    "#7C5CFC": "#9B84FF",
    "#FF7A66": "#FF927E",
    "#F4B740": "#FFCA5E",
    "#D89628": "#F0AA3E",
    "#B47B1F": "#D99A35",
}

DARK_STROKE_MAP = {
    "#0A2030": "#BFE9E5",
    "#073947": "#9ED6D1",
    "#052F3B": "#8FCBC6",
    "#FFFFFF": "#EAFBF8",
    "#F6FBFB": "#EAFBF8",
    "#B7DAD8": "#6EA8A6",
    "#A9CFCD": "#5C9695",
}

PLACES_MASTER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 240" role="img" aria-labelledby="t d">
<title id="t">Proprietary Places product diorama</title><desc id="d">A spatial intelligence map with property towers, a selected place, and an analytical property card.</desc>
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#00E5C2"/><stop offset="1" stop-color="#0097A7"/></linearGradient><filter id="s" x="-30%" y="-30%" width="160%" height="175%"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#0A2030" flood-opacity=".16"/></filter></defs>
<ellipse cx="158" cy="208" rx="122" ry="15" fill="#0A2030" opacity=".11"/>
<g filter="url(#s)">
  <path d="m40 165 111-64 130 38-112 66Z" fill="#F6FBFB" stroke="#0A2030" stroke-width="3" stroke-linejoin="round"/>
  <path d="M40 165v12l129 38v-10Z" fill="#A9CFCD"/><path d="m169 205 112-66v12l-112 64Z" fill="#7FB7B7"/>
  <path d="m64 161 88-51 103 31-88 51Z" fill="#D9ECEB"/>
  <path d="m71 158 96-2m-67 20 96-54m-62 66 92-53" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity=".9"/>
  <path d="M101 145v-38l22-13v38Z" fill="#FFFFFF" stroke="#0A2030" stroke-width="2.5" stroke-linejoin="round"/><path d="m123 94 18 10v38l-18-10Z" fill="#0097A7" stroke="#0A2030" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M145 132V77l26-15v55Z" fill="#FFFFFF" stroke="#0A2030" stroke-width="2.5" stroke-linejoin="round"/><path d="m171 62 22 12v55l-22-12Z" fill="url(#g)" stroke="#0A2030" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M205 142v-31l19-11v31Z" fill="#FFFFFF" stroke="#0A2030" stroke-width="2.5" stroke-linejoin="round"/><path d="m224 100 16 9v31l-16-9Z" fill="#5B8DEF" stroke="#0A2030" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M166 46c-15 0-27 12-27 27 0 23 27 48 27 48s27-25 27-48c0-15-12-27-27-27Z" fill="#FF7A66" stroke="#0A2030" stroke-width="3" stroke-linejoin="round"/><circle cx="166" cy="73" r="10" fill="#FFFFFF"/>
  <path d="M225 48 282 65v79l-57-17Z" fill="#FFFFFF" stroke="#0A2030" stroke-width="3" stroke-linejoin="round"/><path d="m282 65 8-5v78l-8 6Z" fill="#7FB7B7" stroke="#0A2030" stroke-width="3" stroke-linejoin="round"/>
  <circle cx="247" cy="81" r="9" fill="#00E5C2"/><path d="M262 81h10m-35 20h34m-34 12h24" stroke="#B7DAD8" stroke-width="5" stroke-linecap="round"/><path d="m239 126 9-8 8 5 13-16" fill="none" stroke="#0097A7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</g></svg>'''


def ensure_dirs() -> None:
    for directory in (MASTERS, LIGHT, DARK, PREVIEW / "light", PREVIEW / "dark"):
        directory.mkdir(parents=True, exist_ok=True)


def add_v3_atmosphere(svg: str, asset_id: str, theme: str) -> str:
    accent = ACCENTS[asset_id]
    if theme == "light":
        atmosphere = f'''<g aria-hidden="true" class="v3-atmosphere">
  <ellipse cx="160" cy="205" rx="128" ry="18" fill="#0A2030" opacity=".035"/>
  <circle cx="247" cy="69" r="47" fill="{accent}" opacity=".055"/>
  <path d="M54 193 160 132l106 31M76 205l105-61 83 24" fill="none" stroke="#0097A7" stroke-width="1.5" opacity=".09" stroke-linecap="round"/>
</g>'''
    else:
        atmosphere = f'''<g aria-hidden="true" class="v3-atmosphere">
  <ellipse cx="160" cy="205" rx="130" ry="19" fill="#00E5C2" opacity=".075"/>
  <circle cx="247" cy="69" r="50" fill="{DARK_ACCENT_MAP.get(accent, accent)}" opacity=".105"/>
  <path d="M54 193 160 132l106 31M76 205l105-61 83 24" fill="none" stroke="#69D9CC" stroke-width="1.5" opacity=".16" stroke-linecap="round"/>
</g>'''
    return svg.replace("</defs>", f"</defs>\n{atmosphere}", 1)


def replace_attribute_colors(svg: str, attribute: str, mapping: dict[str, str]) -> str:
    pattern = re.compile(rf'({attribute}=")(?P<color>#[0-9A-Fa-f]{{6}})(")')

    def replacement(match: re.Match[str]) -> str:
        color = match.group("color").upper()
        return f'{match.group(1)}{mapping.get(color, color)}{match.group(3)}'

    return pattern.sub(replacement, svg)


def theme_svg(master: str, asset_id: str, label: str, theme: str) -> str:
    svg = master.replace(
        '<svg xmlns="http://www.w3.org/2000/svg"',
        f'<svg xmlns="http://www.w3.org/2000/svg" data-illustration-version="3" data-theme="{theme}" shape-rendering="geometricPrecision"',
        1,
    )
    svg = add_v3_atmosphere(svg, asset_id, theme)
    if theme == "dark":
        svg = replace_attribute_colors(svg, "fill", DARK_FILL_MAP)
        svg = replace_attribute_colors(svg, "stroke", DARK_STROKE_MAP)
        svg = replace_attribute_colors(svg, "stop-color", DARK_ACCENT_MAP)
        svg = replace_attribute_colors(svg, "fill", DARK_ACCENT_MAP)
        svg = replace_attribute_colors(svg, "stroke", DARK_ACCENT_MAP)
        svg = replace_attribute_colors(svg, "flood-color", {"#0A2030": "#000A10"})
        svg = svg.replace("flood-opacity=\".16\"", "flood-opacity=\".34\"")
        svg = svg.replace("flood-opacity=\".15\"", "flood-opacity=\".32\"")
    svg = svg.replace(
        "</svg>",
        f'<!-- {html.escape(label)} · V3 {theme} · native vector -->\n</svg>',
    )
    return svg


def copy_masters() -> None:
    for asset_id, _, _ in PRODUCTS:
        target = MASTERS / f"{asset_id}.svg"
        if asset_id == "ps-places":
            target.write_text(PLACES_MASTER + "\n")
        else:
            source = V2 / f"{asset_id}.svg"
            target.write_text(source.read_text())


def build_svgs() -> None:
    for asset_id, label, _ in PRODUCTS:
        master = (MASTERS / f"{asset_id}.svg").read_text()
        for theme, directory in (("light", LIGHT), ("dark", DARK)):
            output = theme_svg(master, asset_id, label, theme)
            (directory / f"{asset_id}.svg").write_text(output)


def validate_svg(path: Path) -> None:
    subprocess.run(["xmllint", "--noout", str(path)], check=True)
    content = path.read_text()
    inspected = content.replace('xmlns="http://www.w3.org/2000/svg"', "")
    forbidden = ("<image", "data:image", "http://", "https://", "<text")
    for token in forbidden:
        if token in inspected:
            raise ValueError(f"Forbidden token {token!r} in {path}")
    if 'viewBox="0 0 320 240"' not in content:
        raise ValueError(f"Unexpected viewBox in {path}")


def render_svg(source: Path, target: Path, width: int = 640, height: int = 480) -> None:
    subprocess.run(
        ["rsvg-convert", "-w", str(width), "-h", str(height), "-o", str(target), str(source)],
        check=True,
    )


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size, index=1 if bold and candidate.endswith(".ttc") else 0)
    return ImageFont.load_default(size=size)


def rounded_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline: str) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def make_contact_sheet(theme: str) -> Path:
    bg = "#F1F7F7" if theme == "light" else "#06151E"
    card = "#FFFFFF" if theme == "light" else "#0B2430"
    outline = "#D8E8E7" if theme == "light" else "#204652"
    primary = "#0A2030" if theme == "light" else "#E8FAF7"
    secondary = "#527078" if theme == "light" else "#8EB8B6"
    width, cols, card_w, card_h, gap = 1800, 4, 400, 350, 28
    rows = 4
    height = 160 + rows * card_h + (rows - 1) * gap + 95
    canvas = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(canvas)
    draw.text((72, 52), f"Proprietary Systems product dioramas · V3 {theme}", font=get_font(38, True), fill=primary)
    draw.text((72, 102), "Native SVG · 320×240 · paired theme geometry", font=get_font(20), fill=secondary)
    start_x = (width - (cols * card_w + (cols - 1) * gap)) // 2
    for index, (asset_id, label, product_class) in enumerate(PRODUCTS):
        row, col = divmod(index, cols)
        x = start_x + col * (card_w + gap)
        y = 150 + row * (card_h + gap)
        rounded_card(draw, (x, y, x + card_w, y + card_h), 26, card, outline)
        art = Image.open(PREVIEW / theme / f"{asset_id}.png").convert("RGBA")
        art.thumbnail((360, 270), Image.Resampling.LANCZOS)
        canvas.paste(art, (x + (card_w - art.width) // 2, y + 12), art)
        draw.text((x + 24, y + 290), label, font=get_font(23, True), fill=primary)
        badge = "STANDALONE" if product_class == "standalone" else "PLATFORM"
        draw.text((x + 24, y + 323), badge, font=get_font(13, True), fill="#0097A7" if theme == "light" else "#00E5C2")
    target = ROOT / "preview" / f"product-illustrations-v3-{theme}-contact-sheet.png"
    canvas.save(target)
    return target


def make_comparison_sheet() -> Path:
    width, cols, pair_w, row_h, gap = 1920, 3, 590, 360, 28
    rows = 6
    height = 150 + rows * row_h + (rows - 1) * gap + 80
    canvas = Image.new("RGB", (width, height), "#DDE9E8")
    draw = ImageDraw.Draw(canvas)
    draw.text((72, 46), "V3 paired theme comparison", font=get_font(38, True), fill="#0A2030")
    draw.text((72, 96), "Same product silhouette; re-authored contrast and surfaces for each environment", font=get_font(20), fill="#527078")
    start_x = (width - (cols * pair_w + (cols - 1) * gap)) // 2
    for index, (asset_id, label, product_class) in enumerate(PRODUCTS):
        row, col = divmod(index, cols)
        x = start_x + col * (pair_w + gap)
        y = 140 + row * (row_h + gap)
        draw.rounded_rectangle((x, y, x + pair_w, y + row_h), radius=25, fill="#F8FCFC", outline="#C7DAD9", width=2)
        for theme_index, theme in enumerate(("light", "dark")):
            panel_x = x + 15 + theme_index * 280
            panel_fill = "#FFFFFF" if theme == "light" else "#071923"
            draw.rounded_rectangle((panel_x, y + 16, panel_x + 270, y + 284), radius=18, fill=panel_fill)
            art = Image.open(PREVIEW / theme / f"{asset_id}.png").convert("RGBA")
            art.thumbnail((260, 210), Image.Resampling.LANCZOS)
            canvas.paste(art, (panel_x + (270 - art.width) // 2, y + 42), art)
            draw.text((panel_x + 14, y + 254), theme.upper(), font=get_font(12, True), fill="#527078" if theme == "light" else "#8EB8B6")
        draw.text((x + 22, y + 303), label, font=get_font(22, True), fill="#0A2030")
        draw.text((x + 22, y + 334), product_class.upper(), font=get_font(12, True), fill="#0097A7")
    target = ROOT / "preview" / "product-illustrations-v3-theme-comparison.png"
    canvas.save(target)
    return target


def write_manifest() -> None:
    def record(item: tuple[str, str, str]) -> dict[str, str | dict[str, str]]:
        asset_id, label, product_class = item
        return {
            "id": asset_id,
            "label": label,
            "productClass": product_class,
            "master": f"masters/{asset_id}.svg",
            "variants": {"light": f"light/{asset_id}.svg", "dark": f"dark/{asset_id}.svg"},
        }

    manifest = {
        "name": "Proprietary Systems Product Dioramas",
        "version": "3.0.0",
        "viewBox": "0 0 320 240",
        "preferred": True,
        "direction": "Clean 2D isometric product dioramas with paired light and dark variants",
        "products": [record(item) for item in PRODUCTS],
    }
    (V3 / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def write_preview_html() -> None:
    cards = []
    for group, items in (("Proprietary Systems products", PRODUCTS),):
        cards.append(f"<h2>{html.escape(group)}</h2><section class=\"grid\">")
        for asset_id, label, product_class in items:
            cards.append(f'''<article class="card">
  <div class="pair"><figure class="light"><img src="light/{asset_id}.svg" alt=""><span>Light</span></figure><figure class="dark"><img src="dark/{asset_id}.svg" alt=""><span>Dark</span></figure></div>
  <h3>{html.escape(label)}</h3><p>{html.escape(product_class.replace('-', ' ').title())}</p>
</article>''')
        cards.append("</section>")
    document = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PS Product Dioramas V3</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#eaf2f1;color:#0a2030;font:15px/1.4 Inter,ui-sans-serif,system-ui;padding:48px}}header{{max-width:1440px;margin:auto auto 38px}}h1{{font-size:38px;margin:0 0 8px}}h2{{max-width:1440px;margin:42px auto 18px;font-size:22px}}.grid{{max-width:1440px;margin:auto;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}.card{{background:white;border:1px solid #d1e2e0;border-radius:24px;padding:16px;box-shadow:0 12px 32px #0a20300c}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}figure{{position:relative;margin:0;border-radius:17px;overflow:hidden;aspect-ratio:4/3;display:grid;place-items:center}}figure.light{{background:#f7fbfb}}figure.dark{{background:#071923}}img{{width:100%;height:100%;object-fit:contain}}span{{position:absolute;left:12px;bottom:10px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#547177}}.dark span{{color:#9cc3c0}}h3{{margin:14px 4px 2px;font-size:20px}}p{{margin:0 4px 3px;color:#688087}}@media(max-width:850px){{body{{padding:22px}}.grid{{grid-template-columns:1fr}}}}
</style></head><body><header><h1>Product dioramas · V3</h1><p>Paired native SVG illustrations for light and dark interfaces.</p></header>{''.join(cards)}</body></html>'''
    (V3 / "preview.html").write_text(document)


def write_docs() -> None:
    (V3 / "ART_DIRECTION.md").write_text('''# Product Dioramas V3

V3 advances the selected 2D-isometric direction with paired light and dark artwork. The silhouette and semantic metaphor remain stable between themes; surfaces, outlines, atmosphere, and shadow behavior are re-authored for their environment.

## Geometry

- 320 × 240 transparent canvas.
- Shallow axonometric projection with a consistent top-left light source.
- One hero object, one supporting product artifact, and one grounding plane.
- Silhouette must remain legible at 160 × 120.
- No automatic tracing, raster embedding, external URLs, fonts, or SVG text.

## Light mode

- White and mist surfaces.
- Navy structural outlines.
- Quiet atmospheric grid at 9% opacity.
- Soft navy ambient shadow.

## Dark mode

- Ink-blue surfaces rather than inverted white.
- Pale-mint structural outlines only where separation is required.
- Brighter product accents and a controlled luminous atmosphere.
- Near-black ambient shadow with greater density.

## Product architecture

- Proprietary Places is represented as a standalone PS product.
''')
    (V3 / "QA.md").write_text('''# V3 QA

- [x] Every asset has light and dark SVG variants.
- [x] All SVGs share the 320 × 240 viewBox.
- [x] All SVGs pass XML validation.
- [x] No raster images, external URLs, fonts, or SVG text are embedded.
- [x] Light and dark variants preserve matching product silhouettes.
- [x] Dark variants use attribute-aware surface and stroke colors rather than inversion.
- [x] Proprietary Places is classified as a standalone product.
''')


def main() -> None:
    ensure_dirs()
    copy_masters()
    build_svgs()
    for theme, directory in (("light", LIGHT), ("dark", DARK)):
        for asset_id, _, _ in PRODUCTS:
            svg = directory / f"{asset_id}.svg"
            validate_svg(svg)
            render_svg(svg, PREVIEW / theme / f"{asset_id}.png")
    write_manifest()
    write_preview_html()
    write_docs()
    make_contact_sheet("light")
    make_contact_sheet("dark")
    make_comparison_sheet()
    print(f"Built {len(PRODUCTS)} products × 2 themes in {V3}")


if __name__ == "__main__":
    main()
