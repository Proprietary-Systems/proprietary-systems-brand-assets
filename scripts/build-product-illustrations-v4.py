#!/usr/bin/env python3
"""Build the V4 flat-object Proprietary Systems product icon system."""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "svg" / "product-illustrations-v4"
MASTERS = V4 / "masters"
LIGHT = V4 / "light"
DARK = V4 / "dark"
PREVIEW = ROOT / "preview" / "product-illustrations-v4"
ECOSYSTEM_REGISTRY = ROOT / "ecosystem" / "registry.json"
COMPONENTS = ROOT / "components"

PALETTES = {
    "light": {
        "ink": "#0A2030",
        "surface": "#FFFFFF",
        "support": "#E6F2F2",
        "support2": "#D4E9E8",
        "teal": "#0097A7",
        "mint": "#00E5C2",
        "white": "#FFFFFF",
        "shadow": "#0A2030",
        "shadow_opacity": ".12",
    },
    "dark": {
        "ink": "#DDF4F1",
        "surface": "#103744",
        "support": "#193F4B",
        "support2": "#245461",
        "teal": "#00AFC0",
        "mint": "#00E5C2",
        "white": "#F6FBFB",
        "shadow": "#000A10",
        "shadow_opacity": ".28",
    },
}

def load_ecosystem() -> dict:
    return json.loads(ECOSYSTEM_REGISTRY.read_text())


ECOSYSTEM = load_ecosystem()


def load_products() -> list[dict]:
    products: list[dict] = []
    product_by_id = {product["id"]: product for product in ECOSYSTEM["products"]}
    ordered_ids = [
        product_id
        for group in ECOSYSTEM["navigation"]
        for product_id in group["products"]
    ]
    for product_id in ordered_ids:
        product = product_by_id[product_id]
        visual = product["visual"]
        products.append({
            "id": product["id"],
            "label": product["label"],
            "productClass": product["productClass"],
            "category": product["category"],
            "technicalBoundary": product["technicalBoundary"],
            "defaultRoute": product["defaultRoute"],
            "marketingPath": product["marketingPath"],
            "definition": product["definition"],
            "metaphor": visual["metaphor"],
            "excludes": visual["excludes"],
        })
    return products


PRODUCTS = load_products()

BODIES = {
    "peter-ai": '''
<rect x="63" y="57" width="130" height="143" rx="42" fill="{support}"/>
<path d="M128 57V31" stroke="{ink}" stroke-width="8" stroke-linecap="round"/><circle cx="128" cy="25" r="10" fill="{teal}"/>
<rect x="46" y="94" width="24" height="58" rx="10" fill="{ink}"/><rect x="186" y="94" width="24" height="58" rx="10" fill="{ink}"/>
<rect x="78" y="79" width="100" height="91" rx="29" fill="{ink}"/>
<circle cx="107" cy="118" r="10" fill="{mint}"/><circle cx="149" cy="118" r="10" fill="{mint}"/>
<path d="M109 145c12 10 26 10 38 0" fill="none" stroke="{mint}" stroke-width="8" stroke-linecap="round"/>
<path d="M96 200h64v17c0 8-6 14-14 14h-36c-8 0-14-6-14-14Z" fill="{teal}"/>''',
    "ps-crm": '''
<rect x="76" y="55" width="126" height="151" rx="12" fill="{support}"/>
<rect x="54" y="37" width="126" height="151" rx="12" fill="{teal}"/>
<circle cx="117" cy="84" r="22" fill="{white}"/><path d="M82 133c5-24 18-36 35-36s30 12 35 36Z" fill="{white}"/>
<path d="M83 151h68M83 169h51" stroke="{white}" stroke-width="8" stroke-linecap="round"/>''',
    "ps-prospect": '''
<rect x="101" y="92" width="102" height="101" rx="11" fill="{support}"/>
<circle cx="111" cy="105" r="58" fill="{surface}" stroke="{ink}" stroke-width="14"/>
<circle cx="111" cy="88" r="18" fill="{mint}"/><path d="M75 139c5-25 18-38 36-38s31 13 36 38Z" fill="{mint}"/>
<path d="m153 148 47 47" stroke="{ink}" stroke-width="18" stroke-linecap="round"/>''',
    "ps-outreach": '''
<rect x="125" y="96" width="103" height="81" rx="12" fill="{support}"/><path d="M154 126h47M154 149h34" stroke="{white}" stroke-width="8" stroke-linecap="round"/>
<path d="M31 88 218 34l-66 183-36-75-48 39 16-61Z" fill="{teal}"/>
<path d="m84 120 134-86-102 108" fill="none" stroke="{mint}" stroke-width="5" stroke-linejoin="round"/>''',
    "ps-dialer": '''
<rect x="119" y="85" width="105" height="116" rx="14" fill="{support}"/>
<g fill="{teal}"><circle cx="153" cy="119" r="7"/><circle cx="177" cy="119" r="7"/><circle cx="201" cy="119" r="7"/><circle cx="153" cy="145" r="7"/><circle cx="177" cy="145" r="7"/><circle cx="201" cy="145" r="7"/><circle cx="153" cy="171" r="7"/><circle cx="177" cy="171" r="7"/><circle cx="201" cy="171" r="7"/></g>
<path d="M65 31c-13 5-25 12-34 21-5 5-7 13-5 20 20 76 79 135 155 155 7 2 15 0 20-5 9-9 16-21 21-34l-47-37-25 24c-31-15-54-38-69-69l24-25Z" fill="{ink}"/>''',
    "ps-contracts": '''
<path d="M48 29h103l43 43v142H48Z" fill="{surface}" stroke="{ink}" stroke-width="5" stroke-linejoin="round"/><path d="M151 29v43h43" fill="{support}" stroke="{ink}" stroke-width="5" stroke-linejoin="round"/>
<path d="M73 91h61M73 116h79M73 141h56" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>
<path d="M157 119 222 138v38c0 38-27 61-65 72-38-11-65-34-65-72v-38Z" fill="{ink}"/>
<path d="m130 179 18 18 37-44" fill="none" stroke="{mint}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>''',
    "ps-email-signatures": '''
<rect x="31" y="43" width="194" height="170" rx="18" fill="{support}" stroke="{ink}" stroke-width="5"/>
<path d="M31 78h194" stroke="{ink}" stroke-width="10"/><circle cx="53" cy="60" r="5" fill="{mint}"/><circle cx="71" cy="60" r="5" fill="{teal}"/>
<path d="M57 101h103M57 122h78" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>
<rect x="55" y="143" width="146" height="48" rx="10" fill="{teal}"/>
<circle cx="80" cy="167" r="15" fill="{white}"/><path d="M106 158h66M106 176h45" stroke="{white}" stroke-width="7" stroke-linecap="round"/>
<path d="m184 151 7 8 10-13" fill="none" stroke="{mint}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>''',
    "ps-finance": '''
<rect x="45" y="155" width="28" height="62" rx="5" fill="{ink}"/><rect x="91" y="130" width="28" height="87" rx="5" fill="{ink}"/><rect x="137" y="104" width="28" height="113" rx="5" fill="{ink}"/><rect x="183" y="71" width="28" height="146" rx="5" fill="{ink}"/>
<path d="m49 131 50-43 42 23 68-66" fill="none" stroke="{mint}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><circle cx="49" cy="131" r="9" fill="{teal}"/><circle cx="99" cy="88" r="9" fill="{teal}"/><circle cx="141" cy="111" r="9" fill="{teal}"/><circle cx="209" cy="45" r="9" fill="{teal}"/>''',
    "ps-insights": '''
<rect x="35" y="40" width="186" height="176" rx="18" fill="{support}" stroke="{ink}" stroke-width="5"/>
<path d="M35 76h186" stroke="{ink}" stroke-width="9"/><circle cx="56" cy="58" r="5" fill="{mint}"/><circle cx="74" cy="58" r="5" fill="{teal}"/>
<rect x="57" y="139" width="24" height="48" rx="5" fill="{ink}"/><rect x="94" y="119" width="24" height="68" rx="5" fill="{teal}"/><rect x="131" y="96" width="24" height="91" rx="5" fill="{ink}"/>
<path d="m58 124 41-25 37 12 60-39" fill="none" stroke="{mint}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="196" cy="72" r="8" fill="{mint}"/>''',
    "ps-strategy": '''
<circle cx="128" cy="128" r="91" fill="{support}" stroke="{ink}" stroke-width="7"/>
<circle cx="128" cy="128" r="59" fill="{surface}" stroke="{teal}" stroke-width="6"/>
<path d="m155 91-15 50-50 15 15-50Z" fill="{teal}"/><path d="m105 106 35 35-50 15Z" fill="{ink}"/>
<circle cx="128" cy="128" r="8" fill="{mint}"/><path d="M128 26v18M128 212v18M26 128h18M212 128h18" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>''',
    "ps-people": '''
<rect x="69" y="25" width="118" height="69" rx="11" fill="{teal}"/>
<circle cx="102" cy="53" r="13" fill="{white}"/><path d="M84 82c3-15 9-23 18-23s15 8 18 23Z" fill="{white}"/><path d="M132 50h33M132 70h25" stroke="{white}" stroke-width="7" stroke-linecap="round"/>
<path d="M128 94v46M52 140h152M52 140v31M128 140v31M204 140v31" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>
<circle cx="52" cy="195" r="22" fill="{mint}"/><circle cx="128" cy="195" r="22" fill="{ink}"/><circle cx="204" cy="195" r="22" fill="{teal}"/><g fill="{white}"><circle cx="52" cy="189" r="7"/><circle cx="128" cy="189" r="7"/><circle cx="204" cy="189" r="7"/></g>''',
    "ps-docs": '''
<rect x="75" y="42" width="126" height="168" rx="8" fill="{support}"/>
<path d="M55 24h112l35 35v161H55Z" fill="{surface}" stroke="{ink}" stroke-width="5" stroke-linejoin="round"/><path d="M167 24v35h35" fill="{teal}"/>
<path d="M82 91h71M82 119h89M82 147h76M82 175h55" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>''',
    "ps-sheets": '''
<rect x="41" y="34" width="174" height="188" rx="14" fill="{support}" stroke="{ink}" stroke-width="5"/>
<path d="M41 79h174M89 79v143M151 79v143M41 126h174M41 173h174" stroke="{ink}" stroke-width="5"/>
<path d="M41 48c0-8 6-14 14-14h146c8 0 14 6 14 14v31H41Z" fill="{teal}"/>
<rect x="94" y="132" width="52" height="35" rx="5" fill="{mint}"/><path d="M103 150h34" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>''',
    "ps-calendar": '''
<rect x="39" y="53" width="178" height="168" rx="18" fill="{support}" stroke="{ink}" stroke-width="5"/>
<path d="M39 91h178" stroke="{ink}" stroke-width="10"/><path d="M82 31v42M174 31v42" stroke="{teal}" stroke-width="12" stroke-linecap="round"/>
<g fill="{ink}"><rect x="65" y="116" width="28" height="25" rx="5"/><rect x="106" y="116" width="28" height="25" rx="5"/><rect x="147" y="116" width="28" height="25" rx="5"/></g>
<rect x="65" y="158" width="69" height="31" rx="7" fill="{mint}"/><path d="m77 174 10 10 23-25" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>''',
    "ps-messages": '''
<path d="M42 46h132c13 0 23 10 23 23v72c0 13-10 23-23 23h-67l-39 30 8-30H42c-13 0-23-10-23-23V69c0-13 10-23 23-23Z" fill="{support}" stroke="{ink}" stroke-width="5"/>
<path d="M99 104h112c14 0 26 12 26 26v54c0 14-12 26-26 26h-28l8 26-36-26H99c-14 0-26-12-26-26v-54c0-14 12-26 26-26Z" fill="{teal}"/>
<path d="M105 139h98M105 164h72" stroke="{white}" stroke-width="8" stroke-linecap="round"/><circle cx="62" cy="91" r="9" fill="{mint}"/><circle cx="91" cy="91" r="9" fill="{teal}"/><circle cx="120" cy="91" r="9" fill="{ink}"/>''',
    "ps-automate": '''
<path d="M53 81v-19c0-15 12-27 27-27h27M203 175v19c0 15-12 27-27 27h-27" fill="none" stroke="{mint}" stroke-width="8" stroke-linecap="round"/>
<circle cx="51" cy="108" r="17" fill="{surface}" stroke="{teal}" stroke-width="8"/><circle cx="205" cy="148" r="17" fill="{surface}" stroke="{teal}" stroke-width="8"/>
<path d="m137 27-53 101h45l-15 101 62-119h-48Z" fill="{ink}"/>''',
    "ps-creatives": '''
<rect x="38" y="38" width="180" height="180" rx="20" fill="{support}" stroke="{ink}" stroke-width="5"/>
<path d="M38 77h180" stroke="{ink}" stroke-width="9"/><circle cx="58" cy="58" r="5" fill="{mint}"/><circle cx="76" cy="58" r="5" fill="{teal}"/>
<path d="m85 181 63-82 24 20-63 82-34 8Z" fill="{teal}"/><path d="m148 99 12-15c5-6 14-7 20-2l8 7c6 5 7 14 2 20l-13 16Z" fill="{ink}"/>
<path d="m75 209 34-8-24-20Z" fill="{ink}"/><path d="M78 111h15M86 103v16M176 165h20M186 155v20" stroke="{mint}" stroke-width="7" stroke-linecap="round"/>''',
    "ps-sites": '''
<rect x="37" y="45" width="182" height="169" rx="14" fill="{support}" stroke="{ink}" stroke-width="5"/>
<path d="M37 74h182" stroke="{ink}" stroke-width="12"/><circle cx="57" cy="59" r="5" fill="{mint}"/><circle cx="75" cy="59" r="5" fill="{teal}"/><circle cx="93" cy="59" r="5" fill="{white}"/>
<circle cx="128" cy="141" r="47" fill="{teal}"/><circle cx="128" cy="141" r="39" fill="none" stroke="{white}" stroke-width="6"/><path d="M89 141h78M128 102v78M103 110c22 20 22 43 0 62M153 110c-22 20-22 43 0 62" fill="none" stroke="{white}" stroke-width="5"/>''',
    "ps-projects": '''
<path d="M48 26h132l29 29v177H48Z" fill="{support}"/><path d="M180 26v29h29" fill="{teal}"/>
<path d="m72 80 11 11 19-23m-30 59 11 11 19-23m-30 59 11 11 19-23" fill="none" stroke="{mint}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M119 82h60M119 129h60M119 176h43" stroke="{ink}" stroke-width="8" stroke-linecap="round"/>''',
    "ps-client-portal": '''
<rect x="33" y="44" width="190" height="167" rx="18" fill="{support}" stroke="{ink}" stroke-width="5"/>
<path d="M33 79h190" stroke="{ink}" stroke-width="10"/><circle cx="55" cy="61" r="5" fill="{mint}"/><circle cx="73" cy="61" r="5" fill="{teal}"/>
<circle cx="104" cy="125" r="24" fill="{teal}"/><path d="M66 183c5-30 18-45 38-45s33 15 38 45Z" fill="{teal}"/>
<path d="M165 112h31M165 139h31M165 166h22" stroke="{ink}" stroke-width="8" stroke-linecap="round"/>''',
    "ps-home": '''
<path d="M38 47 104 69v69l-66-9Z" fill="{ink}"/><path d="M38 145 104 137v69l-66 22Z" fill="{ink}"/>
<path d="m218 47-66 22v69l66-9Z" fill="{teal}"/><path d="m218 145-66-8v69l66 22Z" fill="{teal}"/>
<path d="M116 77h24v121h-24Z" fill="{support}"/>''',
    "ps-territory": '''
<path d="m28 61 63-26 74 27 63-27v160l-63 26-74-27-63 27Z" fill="{support}" stroke="{ink}" stroke-width="5" stroke-linejoin="round"/>
<path d="M91 35v159M165 62v159" stroke="{white}" stroke-width="6"/>
<path d="M53 174c39-47 60-15 87-52 25-34 38-17 60-51" fill="none" stroke="{ink}" stroke-width="7" stroke-dasharray="11 13" stroke-linecap="round"/>
<circle cx="53" cy="174" r="12" fill="{ink}"/><circle cx="200" cy="71" r="13" fill="{surface}" stroke="{teal}" stroke-width="7"/>''',
    "ps-places": '''
<path d="M35 75h111v146H35Z" fill="{teal}"/><path d="M58 48h65v27H58Z" fill="{teal}"/>
<g fill="{white}"><rect x="57" y="98" width="17" height="17" rx="3"/><rect x="88" y="98" width="17" height="17" rx="3"/><rect x="57" y="132" width="17" height="17" rx="3"/><rect x="88" y="132" width="17" height="17" rx="3"/><rect x="73" y="178" width="35" height="43" rx="4"/></g>
<path d="M184 59c-30 0-54 24-54 54 0 45 54 100 54 100s54-55 54-100c0-30-24-54-54-54Z" fill="{mint}"/><circle cx="184" cy="113" r="22" fill="{white}"/>''',
}


def ensure_dirs() -> None:
    for path in (MASTERS, LIGHT, DARK, PREVIEW / "light", PREVIEW / "dark", COMPONENTS):
        path.mkdir(parents=True, exist_ok=True)


def svg_for(product: dict, theme: str) -> str:
    palette = PALETTES[theme]
    body = BODIES[product["id"]].format(**palette)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title desc" data-illustration-version="4" data-theme="{theme}" shape-rendering="geometricPrecision">
<title id="title">{product["label"]} flat-object product icon</title><desc id="desc">{product["definition"]}, represented by {product["metaphor"]}.</desc>
<defs><filter id="shadow" x="-25%" y="-25%" width="150%" height="165%"><feDropShadow dx="0" dy="7" stdDeviation="7" flood-color="{palette['shadow']}" flood-opacity="{palette['shadow_opacity']}"/></filter></defs>
<g filter="url(#shadow)">{body}</g>
</svg>\n'''


def validate_svg(path: Path) -> None:
    subprocess.run(["xmllint", "--noout", str(path)], check=True)
    inspected = path.read_text().replace('xmlns="http://www.w3.org/2000/svg"', "")
    for forbidden in ("<image", "data:image", "http://", "https://", "<text"):
        if forbidden in inspected:
            raise ValueError(f"Forbidden token {forbidden!r} in {path}")
    if 'viewBox="0 0 256 256"' not in inspected:
        raise ValueError(f"Unexpected viewBox in {path}")


def render_svg(source: Path, target: Path, size: int) -> None:
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), "-o", str(target), str(source)], check=True)


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = ["/System/Library/Fonts/SFNS.ttf", "/System/Library/Fonts/HelveticaNeue.ttc"]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size, index=1 if bold and path.suffix == ".ttc" else 0)
    return ImageFont.load_default(size=size)


def make_contact_sheet(theme: str) -> Path:
    bg = "#EEF5F4" if theme == "light" else "#06151E"
    card = "#FFFFFF" if theme == "light" else "#0B2430"
    outline = "#D5E5E3" if theme == "light" else "#23505C"
    primary = "#0A2030" if theme == "light" else "#E8FAF7"
    secondary = "#5F777D" if theme == "light" else "#91B8B6"
    width, cols, card_w, card_h, gap = 1800, 4, 400, 344, 28
    top = 160
    rows = math.ceil(len(PRODUCTS) / cols)
    height = top + rows * card_h + max(rows - 1, 0) * gap + 90
    canvas = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(canvas)
    draw.text((72, 48), f"Flat-object product icons · V4 {theme}", font=get_font(39, True), fill=primary)
    draw.text((72, 99), "One literal metaphor per product · native SVG · 256×256", font=get_font(19), fill=secondary)
    start_x = (width - (cols * card_w + (cols - 1) * gap)) // 2
    for index, product in enumerate(PRODUCTS):
        row, column = divmod(index, cols)
        x = start_x + column * (card_w + gap)
        y = top + row * (card_h + gap)
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=25, fill=card, outline=outline, width=2)
        art = Image.open(PREVIEW / theme / f"{product['id']}.png").convert("RGBA")
        art.thumbnail((258, 258), Image.Resampling.LANCZOS)
        canvas.paste(art, (x + (card_w - art.width) // 2, y + 6), art)
        draw.text((x + 24, y + 268), product["label"], font=get_font(22, True), fill=primary)
        draw.text((x + 24, y + 299), product["definition"], font=get_font(14), fill=secondary)
        if product["productClass"] == "external-surface":
            boundary_label = "EXTERNAL SURFACE"
        elif product["technicalBoundary"] in {"specialized-data-plane", "compatibility-web-runtime"}:
            boundary_label = "SUITE · BOUNDED RUNTIME"
        else:
            boundary_label = "SUITE"
        draw.text((x + 24, y + 324), boundary_label, font=get_font(11, True), fill="#00A9AA" if theme == "light" else "#00E5C2")
    target = ROOT / "preview" / f"product-illustrations-v4-{theme}-contact-sheet.png"
    canvas.save(target)
    return target


def make_legibility_sheet() -> Path:
    items = PRODUCTS
    width, row_h = 1200, 92
    height = 100 + len(items) * row_h + 48
    canvas = Image.new("RGB", (width, height), "#EAF2F1")
    draw = ImageDraw.Draw(canvas)
    draw.text((48, 30), "V4 actual-size legibility · 48px", font=get_font(30, True), fill="#0A2030")
    for index, product in enumerate(items):
        y = 92 + index * row_h
        fill = "#FFFFFF" if index % 2 == 0 else "#F5FAF9"
        draw.rounded_rectangle((38, y, width - 38, y + 78), radius=16, fill=fill)
        light = Image.open(PREVIEW / "light" / f"{product['id']}-48.png").convert("RGBA")
        dark = Image.open(PREVIEW / "dark" / f"{product['id']}-48.png").convert("RGBA")
        draw.rounded_rectangle((55, y + 7, 119, y + 71), radius=12, fill="#FFFFFF", outline="#D4E5E3")
        draw.rounded_rectangle((134, y + 7, 198, y + 71), radius=12, fill="#071923")
        canvas.paste(light, (63, y + 15), light)
        canvas.paste(dark, (142, y + 15), dark)
        draw.text((226, y + 17), product["label"], font=get_font(18, True), fill="#0A2030")
        draw.text((226, y + 44), product["definition"], font=get_font(14), fill="#61777D")
    target = ROOT / "preview" / "product-illustrations-v4-48px-legibility.png"
    canvas.save(target)
    return target


def write_manifest() -> None:
    def record(product: dict) -> dict:
        return {
            **product,
            "master": f"masters/{product['id']}.svg",
            "variants": {"light": f"light/{product['id']}.svg", "dark": f"dark/{product['id']}.svg"},
        }
    manifest = {
        "name": "Proprietary Systems Flat-Object Product Icons",
        "version": "4.2.0",
        "taxonomyVersion": "2.1.0",
        "ecosystemRegistry": "../../ecosystem/registry.json",
        "viewBox": "0 0 256 256",
        "preferred": True,
        "direction": "One literal flat-object metaphor per product",
        "semanticRules": [
            "Product meaning precedes decoration.",
            "One primary object and at most one semantic modifier.",
            "External relationships, internal people, and new-person discovery must remain distinct.",
            "Asynchronous outreach and live calling must remain distinct.",
            "Agreement execution and employee email-signature management must remain distinct.",
            "Document authoring and coordinated work must remain distinct.",
            "Internal application access and external client collaboration must remain distinct.",
            "Spreadsheet modeling, executive analytics, and financial planning must remain distinct.",
            "Operational territory and property intelligence must remain distinct.",
            "Creative production, website publishing, and generic document authoring must remain distinct.",
        ],
        "products": [record(product) for product in PRODUCTS],
        "aliases": ECOSYSTEM.get("aliases", {}),
    }
    (V4 / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def write_docs() -> None:
    (V4 / "ART_DIRECTION.md").write_text('''# V4 Flat-Object Product Icons

V4 replaces multi-object dioramas with one immediately recognizable object metaphor per product. The system is designed to remain clear at 48 pixels and structurally intact at 24 pixels.

## Grammar

- 256 × 256 transparent canvas.
- Orthographic 2D geometry; no isometric stage or environmental scene.
- One primary object and at most one semantic modifier.
- Navy, teal, mint, white, and mist only.
- One soft shadow; no gradients or embedded raster imagery.
- Light and dark variants share geometry and re-author contrast.

## Taxonomy

The machine-readable taxonomy, definitions, metaphors, and collision exclusions live in `manifest.json`.
''')
    (V4 / "QA.md").write_text(f'''# V4 QA

- [x] {len(PRODUCTS)} products have paired light and dark SVG variants.
- [x] All assets use a 256 × 256 viewBox.
- [x] All assets pass XML validation.
- [x] No raster images, external URLs, fonts, or SVG text are embedded.
- [x] The manifest defines product meaning, primary metaphor, and collision exclusions.
- [x] Product metadata is generated from the canonical ecosystem registry.
- [x] A 48px light/dark legibility sheet is generated.
''')


def write_preview_html() -> None:
    cards = []
    for heading, products in (("Proprietary Systems products", PRODUCTS),):
        cards.append(f"<h2>{heading}</h2><section class=\"grid\">")
        for product in products:
            asset_id = product["id"]
            cards.append(f'''<article><div class="pair"><figure class="light"><img src="light/{asset_id}.svg" alt=""></figure><figure class="dark"><img src="dark/{asset_id}.svg" alt=""></figure></div><h3>{product["label"]}</h3><p>{product["definition"]}</p></article>''')
        cards.append("</section>")
    (V4 / "preview.html").write_text(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PS V4 Product Icons</title><style>*{{box-sizing:border-box}}body{{margin:0;padding:48px;background:#edf4f3;color:#0a2030;font:15px/1.45 Inter,system-ui}}header,h2,.grid{{max-width:1420px;margin-left:auto;margin-right:auto}}h1{{font-size:38px;margin:0}}h2{{margin-top:42px}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}article{{background:#fff;border:1px solid #d4e4e2;border-radius:22px;padding:16px}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}figure{{margin:0;display:grid;place-items:center;border-radius:14px;aspect-ratio:1}}figure.light{{background:#fff}}figure.dark{{background:#071923}}img{{width:82%;height:82%}}h3{{margin:14px 4px 2px;font-size:19px}}p{{margin:0 4px;color:#61777d}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><header><h1>Flat-object product icons · V4.1</h1><p>Paired light and dark native SVGs generated from the PS ecosystem registry.</p></header>{''.join(cards)}</body></html>''')


def write_react_catalog() -> None:
    id_union = "\n  | ".join(f'"{product["id"]}"' for product in PRODUCTS)
    records: list[str] = []
    for product in PRODUCTS:
        product_id = product["id"]
        records.append(
            f'''  "{product_id}": {{
    id: "{product_id}",
    label: {json.dumps(product["label"])},
    definition: {json.dumps(product["definition"])},
    productClass: {json.dumps(product["productClass"])},
    category: {json.dumps(product["category"])},
    technicalBoundary: {json.dumps(product["technicalBoundary"])},
    defaultRoute: {json.dumps(product["defaultRoute"])},
    marketingPath: {json.dumps(product["marketingPath"])},
    light: "brand-assets/svg/product-illustrations-v4/light/{product_id}.svg",
    dark: "brand-assets/svg/product-illustrations-v4/dark/{product_id}.svg",
  }}'''
        )
    aliases = ",\n".join(
        f'  "{alias}": "{canonical}"' for alias, canonical in ECOSYSTEM.get("aliases", {}).items()
    )
    navigation_groups = json.dumps(ECOSYSTEM.get("navigation", []), indent=2)
    featured_products = json.dumps(ECOSYSTEM.get("launcher", {}).get("featuredProducts", []), indent=2)
    record_block = ",\n".join(records)
    (COMPONENTS / "productIllustrationCatalog.ts").write_text(f'''// Generated by scripts/build-product-illustrations-v4.py. Do not hand-edit.
export type ProprietarySystemsProductId =
  | {id_union};

export type ProprietarySystemsProductIllustration = {{
  id: ProprietarySystemsProductId;
  label: string;
  definition: string;
  productClass: "suite-home" | "suite-module" | "external-surface";
  category: string;
  technicalBoundary: string;
  defaultRoute: string;
  marketingPath: string;
  light: string;
  dark: string;
}};

export type ProprietarySystemsNavigationGroup = {{
  id: string;
  label: string;
  products: ProprietarySystemsProductId[];
}};

export const PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS: Record<ProprietarySystemsProductId, ProprietarySystemsProductIllustration> = {{
{record_block}
}};

export const PROPRIETARY_SYSTEMS_PRODUCT_ALIASES = {{
{aliases}
}} as const;

export const PROPRIETARY_SYSTEMS_NAVIGATION_GROUPS = {navigation_groups} as ProprietarySystemsNavigationGroup[];

export const PROPRIETARY_SYSTEMS_FEATURED_PRODUCTS = {featured_products} as ProprietarySystemsProductId[];
''')


def write_legacy_aliases() -> None:
    product_by_id = {product["id"]: product for product in PRODUCTS}
    for alias, canonical in ECOSYSTEM.get("aliases", {}).items():
        product = product_by_id[canonical]
        alias_product = {**product, "label": f"{product['label']} (legacy {alias} alias)"}
        (MASTERS / f"{alias}.svg").write_text(
            svg_for(alias_product, "light").replace('data-theme="light"', 'data-theme="master"')
        )
        for theme, directory in (("light", LIGHT), ("dark", DARK)):
            path = directory / f"{alias}.svg"
            path.write_text(svg_for(alias_product, theme))
            validate_svg(path)


def main() -> None:
    ensure_dirs()
    for product in PRODUCTS:
        master = svg_for(product, "light").replace('data-theme="light"', 'data-theme="master"')
        (MASTERS / f"{product['id']}.svg").write_text(master)
        for theme, directory in (("light", LIGHT), ("dark", DARK)):
            path = directory / f"{product['id']}.svg"
            path.write_text(svg_for(product, theme))
            validate_svg(path)
            render_svg(path, PREVIEW / theme / f"{product['id']}.png", 512)
            render_svg(path, PREVIEW / theme / f"{product['id']}-48.png", 48)
    write_legacy_aliases()
    write_manifest()
    write_docs()
    write_preview_html()
    write_react_catalog()
    make_contact_sheet("light")
    make_contact_sheet("dark")
    make_legibility_sheet()
    print(f"Built {len(PRODUCTS)} V4 products × 2 themes")


if __name__ == "__main__":
    main()
