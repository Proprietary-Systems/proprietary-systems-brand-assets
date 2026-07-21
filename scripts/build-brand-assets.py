#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent

DIRS = {
    "svg": ROOT / "svg",
    "png": ROOT / "png",
    "icons": ROOT / "icons",
    "preview": ROOT / "preview",
    "reference": ROOT / "reference",
}

REFERENCE_IMAGE = Path(
    "/Users/research/Library/Messages/Attachments/12/02/33DA14A1-5846-4A35-97D3-474C5B83DBA2/IMG_6039.JPG"
)

COLORS = {
    "mint": "#00E5C2",
    "teal": "#0097A7",
    "navy": "#0A2030",
    "off_white": "#F6FBFB",
    "mist": "#E6F2F2",
    "white": "#FFFFFF",
    "black": "#171717",
}

FONT_CANDIDATES = [
    "/System/Library/Fonts/Avenir Next.ttc",
    "/System/Library/Fonts/Avenir.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
]


def ensure_dirs() -> None:
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


def hex_to_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default(size=size)


class Canvas:
    def __init__(self, width: int, height: int, bg: str | None = None, scale: int = 3):
        self.width = width
        self.height = height
        self.scale = scale
        color = (0, 0, 0, 0) if bg is None else hex_to_rgba(bg)
        self.image = Image.new("RGBA", (width * scale, height * scale), color)
        self.draw = ImageDraw.Draw(self.image)

    def p(self, value: float) -> int:
        return int(round(value * self.scale))

    def xy(self, x: float, y: float) -> tuple[int, int]:
        return (self.p(x), self.p(y))

    def box(self, x0: float, y0: float, x1: float, y1: float) -> tuple[int, int, int, int]:
        return (self.p(x0), self.p(y0), self.p(x1), self.p(y1))

    def polygon(self, points: list[tuple[float, float]], fill: str) -> None:
        self.draw.polygon([(self.p(x), self.p(y)) for x, y in points], fill=hex_to_rgba(fill))

    def rounded(self, box: tuple[float, float, float, float], radius: float, fill: str) -> None:
        self.draw.rounded_rectangle(self.box(*box), radius=self.p(radius), fill=hex_to_rgba(fill))

    def rect(self, box: tuple[float, float, float, float], fill: str) -> None:
        self.draw.rectangle(self.box(*box), fill=hex_to_rgba(fill))

    def line(self, xy: tuple[float, float, float, float], fill: str, width: float = 1) -> None:
        self.draw.line(self.box(*xy), fill=hex_to_rgba(fill), width=self.p(width))

    def text(
        self,
        xy: tuple[float, float],
        text: str,
        size: int,
        fill: str,
        anchor: str = "la",
    ) -> None:
        self.draw.text(self.xy(*xy), text, font=font(size * self.scale), fill=hex_to_rgba(fill), anchor=anchor)

    def tracked_text_width(self, value: str, size: int, tracking: float) -> float:
        fnt = font(size * self.scale)
        width = 0.0
        for index, char in enumerate(value):
            bbox = self.draw.textbbox((0, 0), char, font=fnt)
            width += (bbox[2] - bbox[0]) / self.scale
            if index != len(value) - 1:
                width += tracking
        return width

    def tracked_text(
        self,
        xy: tuple[float, float],
        value: str,
        size: int,
        fill: str,
        tracking: float,
        anchor: str = "la",
    ) -> None:
        x, y = xy
        if anchor in {"ma", "mm"}:
            x -= self.tracked_text_width(value, size, tracking) / 2
            anchor = "la" if anchor == "ma" else "lm"

        fnt = font(size * self.scale)
        current_x = x
        for index, char in enumerate(value):
            self.draw.text(
                self.xy(current_x, y),
                char,
                font=fnt,
                fill=hex_to_rgba(fill),
                anchor=anchor,
            )
            bbox = self.draw.textbbox((0, 0), char, font=fnt)
            current_x += (bbox[2] - bbox[0]) / self.scale
            if index != len(value) - 1:
                current_x += tracking

    def save(self, path: Path) -> None:
        output = self.image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        output.save(path)


def mark_colors(scheme: str) -> tuple[str, str, str]:
    if scheme == "full-dark":
        return (COLORS["off_white"], COLORS["mint"], COLORS["teal"])
    if scheme == "full-light":
        return (COLORS["navy"], COLORS["mint"], COLORS["teal"])
    if scheme == "mono-white":
        return (COLORS["white"], COLORS["white"], COLORS["white"])
    if scheme == "mono-dark":
        return (COLORS["navy"], COLORS["navy"], COLORS["navy"])
    raise ValueError(f"Unknown mark scheme: {scheme}")


TRACED_MARK_VIEWBOX = "74 63 517 431"
TRACED_MARK_ASPECT = 431 / 517
TRACED_WHITE_PATH = """
M758 5359 c-17 -9 -18 -34 -18 -298 0 -226 3 -291 13 -299 9 -8 360
-12 1193 -14 1286 -4 1194 1 1332 -65 89 -42 184 -128 247 -224 l45
-69 295 0 c194 0 296 4 300 10 4 6 1 34 -5 63 -15 67 -89 255
-112 286 -10 13 -18 28 -18 32 0 28 -154 220 -230 287 -118 104
-309 213 -435 248 -183 51 -90 48 -1385 51 -819 2 -1211 -1
-1222 -8z
M757 4158 c-16 -12 -17 -112 -15 -1527 2 -1170 6 -1515 15 -1518
12 -4 186 157 501 464 l162 158 0 755 c0 648 2 764 15 815 28
104 87 180 179 228 l61 32 735 2 c404 1 1207 2 1783 2 1037 1
1049 1 1119 22 91 27 137 56 216 138 91 95 332 398 332 419 0
5 -34 12 -77 16 -42 3 -1186 6 -2543 6 -1957 0 -2470 -3 -2483
-12z
""".strip()

TRACED_TEAL_SHADOW_PATH = """
M3840 3584 c-34 -11 -71 -13 -152 -9 -70 4 -113 3 -127 -5 -42
-22 -20 -30 79 -30 55 0 100 -4 100 -9 0 -4 -41 -11 -92 -13
-82 -5 -94 -8 -108 -28 -30 -45 -77 -86 -135 -115 -76 -39 -95
-66 -102 -144 -3 -34 -10 -64 -14 -67 -17 -10 -10 -63 11 -74
10 -6 90 -11 177 -13 144 -2 163 0 218 21 102 38 232 165 302
292 20 36 49 86 64 112 l29 48 -23 14 c-27 18 -101 36 -147 35
-19 0 -55 -7 -80 -15z
""".strip()

TRACED_TEAL_MAIN_PATH = """
M2490 3471 c-44 -12 -52 -43 -47 -186 6 -163 32 -275 91 -394
91 -184 197 -313 318 -386 198 -119 351 -173 548 -193 53 -6
426 -10 848 -10 742 -1 753 -1 817 -22 78 -26 106 -47 138 -105
93 -165 30 -349 -148 -432 l-60 -28 -1005 -2 c-958 -2 -1009
-3 -1080 -22 -41 -10 -104 -36 -140 -57 -104 -62 -231 -201
-334 -366 -22 -35 -50 -79 -63 -99 -26 -39 -30 -71 -10 -87 6
-5 48 -12 92 -15 44 -3 658 -2 1365 2 l1285 8 85 26 c152 45
194 63 289 122 266 166 431 476 431 812 0 147 -39 301 -102
403 -15 25 -32 56 -38 69 -26 59 -154 199 -245 267 -129 96
-216 131 -395 159 -89 14 -212 16 -805 17 -385 0 -745 4 -800
8 -74 6 -115 15 -159 35 -78 35 -184 125 -221 188 -27 47 -30
62 -33 155 -4 88 -7 104 -23 113 -11 5 -113 12 -227 15 -114
2 -238 6 -277 8 -38 2 -81 0 -95 -3z
""".strip()


def draw_mark(c: Canvas, x: float, y: float, width: float, scheme: str = "full-dark") -> None:
    upper, lower, lower_shadow = mark_colors(scheme)
    scale = width / 240.0

    def px(value: float) -> float:
        return x + value * scale

    def py(value: float) -> float:
        return y + value * scale

    # Lower S shape, drawn first so the upper P can sit above it.
    c.rounded((px(84), py(78), px(204), py(110)), 15 * scale, lower_shadow)
    c.rect((px(84), py(94), px(112), py(133)), lower)
    c.rounded((px(94), py(124), px(206), py(156)), 16 * scale, lower)
    c.polygon(
        [
            (px(78), py(156)),
            (px(191), py(156)),
            (px(176), py(179)),
            (px(62), py(179)),
        ],
        lower,
    )

    # Upper P shape.
    c.rounded((px(32), py(26), px(142), py(51)), 10 * scale, upper)
    c.polygon([(px(126), py(26)), (px(158), py(26)), (px(173), py(51)), (px(137), py(51))], upper)
    c.polygon(
        [
            (px(32), py(67)),
            (px(220), py(67)),
            (px(201), py(94)),
            (px(58), py(94)),
            (px(58), py(148)),
            (px(32), py(176)),
        ],
        upper,
    )
    c.rounded((px(52), py(68), px(148), py(94)), 8 * scale, upper)


def draw_ps_ai(
    c: Canvas,
    x: float,
    y: float,
    size: int,
    base_fill: str,
    accent_fill: str,
    anchor: str = "lm",
) -> None:
    fnt = font(size * c.scale)
    parts = [("PS", base_fill), (".AI", accent_fill)]
    total = 0.0
    for value, _ in parts:
        bbox = c.draw.textbbox((0, 0), value, font=fnt)
        total += (bbox[2] - bbox[0]) / c.scale
    current_x = x - total / 2 if anchor.startswith("m") else x
    for value, fill in parts:
        c.draw.text(c.xy(current_x, y), value, font=fnt, fill=hex_to_rgba(fill), anchor="lm")
        bbox = c.draw.textbbox((0, 0), value, font=fnt)
        current_x += (bbox[2] - bbox[0]) / c.scale


def draw_horizontal(c: Canvas, variant: str, bg: str | None) -> None:
    is_secondary = variant == "secondary"
    if bg == COLORS["off_white"]:
        mark_scheme = "full-light"
        text_fill = COLORS["navy"]
        divider = COLORS["navy"]
    elif variant == "mono-white":
        mark_scheme = "mono-white"
        text_fill = COLORS["white"]
        divider = COLORS["white"]
    elif variant == "mono-dark":
        mark_scheme = "mono-dark"
        text_fill = COLORS["navy"]
        divider = COLORS["navy"]
    else:
        mark_scheme = "full-dark"
        text_fill = COLORS["white"]
        divider = COLORS["mint"]

    h = c.height
    w = c.width
    mark_w = h * (0.76 if is_secondary else 0.82)
    mark_h = mark_w * 180 / 240
    mark_x = h * 0.13
    mark_y = (h - mark_h) / 2
    draw_mark(c, mark_x, mark_y, mark_w, mark_scheme)

    div_h = h * 0.68
    div_y = (h - div_h) / 2
    div1_x = mark_x + mark_w + h * 0.33
    div2_x = w - h * 2.25
    c.line((div1_x, div_y, div1_x, div_y + div_h), divider, max(2, h * 0.01))
    c.line((div2_x, div_y, div2_x, div_y + div_h), divider, max(2, h * 0.01))

    text_x = div1_x + h * 0.36
    if is_secondary:
        c.tracked_text((text_x, h * 0.52), "PROPRIETARY SYSTEMS", int(h * 0.17), text_fill, h * 0.038, "lm")
    else:
        c.tracked_text((text_x, h * 0.40), "PROPRIETARY", int(h * 0.17), text_fill, h * 0.045, "lm")
        c.tracked_text((text_x, h * 0.64), "SYSTEMS", int(h * 0.17), text_fill, h * 0.067, "lm")

    accent = text_fill if variant in {"mono-white", "mono-dark"} else COLORS["mint"]
    draw_ps_ai(c, div2_x + h * 0.42, h * 0.52, int(h * 0.39), text_fill, accent, "lm")


def draw_stacked(c: Canvas, bg: str | None = COLORS["navy"]) -> None:
    mark_w = c.width * 0.29
    draw_mark(c, (c.width - mark_w) / 2, c.height * 0.12, mark_w, "full-dark")
    c.tracked_text((c.width / 2, c.height * 0.53), "PROPRIETARY", int(c.height * 0.056), COLORS["white"], c.height * 0.025, "ma")
    c.tracked_text((c.width / 2, c.height * 0.61), "SYSTEMS", int(c.height * 0.056), COLORS["white"], c.height * 0.038, "ma")
    c.line((c.width * 0.25, c.height * 0.69, c.width * 0.75, c.height * 0.69), COLORS["teal"], max(2, c.height * 0.004))
    draw_ps_ai(c, c.width / 2, c.height * 0.78, int(c.height * 0.085), COLORS["white"], COLORS["mint"], "mm")


def draw_wordmark(c: Canvas, bg: str | None, mono: str | None = None) -> None:
    if mono == "white":
        base = accent = COLORS["white"]
    elif mono == "dark":
        base = accent = COLORS["navy"]
    else:
        base = COLORS["white"] if bg == COLORS["navy"] else COLORS["navy"]
        accent = COLORS["mint"]
    draw_ps_ai(c, c.width / 2, c.height / 2, int(c.height * 0.46), base, accent, "mm")


def draw_app_icon(
    path: Path,
    size: int,
    shape: str = "rounded",
    bg: str = COLORS["navy"],
    mark_scheme: str = "full-dark",
    gradient: bool = False,
) -> Image.Image:
    scale = 3
    canvas = Canvas(size, size, None, scale)

    if gradient:
        for y in range(size * scale):
            ratio = y / max(1, size * scale - 1)
            start = hex_to_rgba(COLORS["mint"])
            end = hex_to_rgba(COLORS["teal"])
            color = tuple(int(start[i] * (1 - ratio) + end[i] * ratio) for i in range(3)) + (255,)
            canvas.draw.line((0, y, size * scale, y), fill=color)
        mask = Image.new("L", (size * scale, size * scale), 0)
        mask_draw = ImageDraw.Draw(mask)
        if shape == "circle":
            mask_draw.ellipse((0, 0, size * scale, size * scale), fill=255)
        else:
            mask_draw.rounded_rectangle((0, 0, size * scale, size * scale), radius=int(size * scale * 0.2), fill=255)
        canvas.image.putalpha(mask)
    elif shape == "circle":
        canvas.draw.ellipse(canvas.box(0, 0, size, size), fill=hex_to_rgba(bg))
    else:
        canvas.rounded((0, 0, size, size), size * 0.2, bg)

    mark_w = size * 0.62
    draw_mark(canvas, (size - mark_w) / 2, size * 0.275, mark_w, mark_scheme)
    output = canvas.image.resize((size, size), Image.Resampling.LANCZOS)
    output.save(path)
    return output


def svg_mark(scheme: str = "full-dark") -> str:
    upper, lower, lower_shadow = mark_colors(scheme)
    shadow_fill = lower if scheme in {"mono-white", "mono-dark"} else lower_shadow
    return f"""
  <g id="ps-mark" transform="translate(0 600) scale(0.1 -0.1)">
    <path d="{TRACED_TEAL_MAIN_PATH}" fill="{lower}"/>
    <path d="{TRACED_TEAL_SHADOW_PATH}" fill="{shadow_fill}"/>
    <path d="{TRACED_WHITE_PATH}" fill="{upper}"/>
  </g>""".strip()


def svg_shell(width: int, height: int, title: str, content: str, bg: str | None = None) -> str:
    bg_rect = "" if bg is None else f'  <rect width="{width}" height="{height}" fill="{bg}"/>\n'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">Proprietary Systems logo asset generated from the approved brand specification.</desc>
  <style>
    .ps-type {{ font-family: "Avenir Next", Avenir, Montserrat, "Century Gothic", Arial, sans-serif; font-weight: 600; }}
    .ps-wordmark {{ font-family: "Avenir Next", Avenir, Montserrat, "Century Gothic", Arial, sans-serif; font-weight: 500; }}
  </style>
{bg_rect}{content}
</svg>
"""


def svg_transform_mark(x: float, y: float, width: float, scheme: str) -> str:
    height = width * TRACED_MARK_ASPECT
    return (
        f'<svg x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}" '
        f'viewBox="{TRACED_MARK_VIEWBOX}" preserveAspectRatio="xMidYMid meet" overflow="visible">\n'
        f"{svg_mark(scheme)}\n  </svg>"
    )


def svg_ps_ai(x: float, y: float, size: float, base: str, accent: str, anchor: str = "start") -> str:
    text_anchor = "middle" if anchor == "middle" else "start"
    return (
        f'<text class="ps-wordmark" x="{x:.2f}" y="{y:.2f}" font-size="{size:.2f}" '
        f'letter-spacing="0" text-anchor="{text_anchor}" dominant-baseline="middle">'
        f'<tspan fill="{base}">PS</tspan><tspan fill="{accent}">.AI</tspan></text>'
    )


def write_svgs() -> None:
    svg_specs = []

    for slug, variant, width, height, bg in [
        ("primary-horizontal-lockup", "primary", 1600, 420, None),
        ("primary-horizontal-lockup-on-dark", "primary", 1600, 420, COLORS["navy"]),
        ("secondary-horizontal-lockup", "secondary", 1600, 320, None),
        ("secondary-horizontal-lockup-on-dark", "secondary", 1600, 320, COLORS["navy"]),
    ]:
        text_fill = COLORS["white"]
        divider = COLORS["mint"]
        mark_scheme = "full-dark"
        div1 = 370 if variant == "primary" else 290
        div2 = 1165 if variant == "primary" else 1240
        mark_w = 230 if variant == "primary" else 170
        mark_y = 114 if variant == "primary" else 88
        text_x = 455 if variant == "primary" else 365
        parts = [
            svg_transform_mark(70, mark_y, mark_w, mark_scheme),
            f'<line x1="{div1}" y1="{70 if variant == "primary" else 58}" x2="{div1}" y2="{350 if variant == "primary" else 262}" stroke="{divider}" stroke-width="4"/>',
            f'<line x1="{div2}" y1="{70 if variant == "primary" else 58}" x2="{div2}" y2="{350 if variant == "primary" else 262}" stroke="{divider}" stroke-width="4"/>',
        ]
        if variant == "primary":
            parts.append(f'<text class="ps-type" x="{text_x}" y="174" font-size="58" letter-spacing="24" fill="{text_fill}">PROPRIETARY</text>')
            parts.append(f'<text class="ps-type" x="{text_x}" y="256" font-size="58" letter-spacing="31" fill="{text_fill}">SYSTEMS</text>')
            parts.append(svg_ps_ai(1265, 216, 96, text_fill, COLORS["mint"]))
        else:
            parts.append(f'<text class="ps-type" x="{text_x}" y="180" font-size="42" letter-spacing="14" textLength="720" lengthAdjust="spacing" fill="{text_fill}" dominant-baseline="middle">PROPRIETARY SYSTEMS</text>')
            parts.append(svg_ps_ai(1325, 176, 72, text_fill, COLORS["mint"]))
        svg_specs.append((slug, width, height, f"Proprietary Systems {slug.replace('-', ' ')}", "\n  ".join(parts), bg))

    stacked_parts = [
        svg_transform_mark(310, 78, 240, "full-dark"),
        f'<text class="ps-type" x="430" y="430" font-size="48" letter-spacing="24" fill="{COLORS["white"]}" text-anchor="middle">PROPRIETARY</text>',
        f'<text class="ps-type" x="430" y="506" font-size="48" letter-spacing="36" fill="{COLORS["white"]}" text-anchor="middle">SYSTEMS</text>',
        f'<line x1="220" y1="586" x2="640" y2="586" stroke="{COLORS["teal"]}" stroke-width="4"/>',
        svg_ps_ai(430, 670, 78, COLORS["white"], COLORS["mint"], "middle"),
    ]
    svg_specs.append(("stacked-logo", 860, 860, "Proprietary Systems stacked logo", "\n  ".join(stacked_parts), None))
    svg_specs.append(("stacked-logo-on-dark", 860, 860, "Proprietary Systems stacked logo on dark", "\n  ".join(stacked_parts), COLORS["navy"]))

    icon_parts = [svg_transform_mark(62, 94, 388, "full-dark")]
    svg_specs.append(("icon-only-mark", 512, 512, "Proprietary Systems icon-only mark", "\n  ".join(icon_parts), None))

    wordmark_parts = [svg_ps_ai(700, 180, 168, COLORS["white"], COLORS["mint"], "middle")]
    svg_specs.append(("wordmark-ps-ai", 1400, 360, "Proprietary Systems PS.AI wordmark", "\n  ".join(wordmark_parts), None))
    svg_specs.append(("wordmark-ps-ai-on-dark", 1400, 360, "Proprietary Systems PS.AI wordmark on dark", "\n  ".join(wordmark_parts), COLORS["navy"]))

    mono_white = [
        svg_transform_mark(75, 78, 190, "mono-white"),
        f'<line x1="335" y1="65" x2="335" y2="255" stroke="{COLORS["white"]}" stroke-width="3"/>',
        f'<text class="ps-type" x="395" y="135" font-size="42" letter-spacing="20" fill="{COLORS["white"]}">PROPRIETARY</text>',
        f'<text class="ps-type" x="395" y="199" font-size="42" letter-spacing="30" fill="{COLORS["white"]}">SYSTEMS</text>',
        f'<line x1="1015" y1="65" x2="1015" y2="255" stroke="{COLORS["white"]}" stroke-width="3"/>',
        svg_ps_ai(1085, 164, 82, COLORS["white"], COLORS["white"]),
    ]
    svg_specs.append(("monochrome-white-horizontal", 1360, 320, "Proprietary Systems monochrome white horizontal", "\n  ".join(mono_white), None))
    svg_specs.append(("monochrome-white-horizontal-on-dark", 1360, 320, "Proprietary Systems monochrome white horizontal on dark", "\n  ".join(mono_white), COLORS["navy"]))

    mono_dark = [
        svg_transform_mark(75, 78, 190, "mono-dark"),
        f'<line x1="335" y1="65" x2="335" y2="255" stroke="{COLORS["navy"]}" stroke-width="3"/>',
        f'<text class="ps-type" x="395" y="135" font-size="42" letter-spacing="20" fill="{COLORS["navy"]}">PROPRIETARY</text>',
        f'<text class="ps-type" x="395" y="199" font-size="42" letter-spacing="30" fill="{COLORS["navy"]}">SYSTEMS</text>',
        f'<line x1="1015" y1="65" x2="1015" y2="255" stroke="{COLORS["navy"]}" stroke-width="3"/>',
        svg_ps_ai(1085, 164, 82, COLORS["navy"], COLORS["navy"]),
    ]
    svg_specs.append(("monochrome-dark-horizontal", 1360, 320, "Proprietary Systems monochrome dark horizontal", "\n  ".join(mono_dark), None))
    svg_specs.append(("monochrome-dark-horizontal-on-light", 1360, 320, "Proprietary Systems monochrome dark horizontal on light", "\n  ".join(mono_dark), COLORS["off_white"]))

    app_icons = [
        ("app-icon-dark", COLORS["navy"], "full-dark", "rounded"),
        ("app-icon-light", COLORS["off_white"], "full-light", "rounded"),
        ("app-icon-black", COLORS["black"], "full-dark", "rounded"),
        ("app-icon-circle", COLORS["navy"], "full-dark", "circle"),
    ]
    for slug, bg, scheme, shape in app_icons:
        if shape == "circle":
            bg_shape = f'<circle cx="256" cy="256" r="256" fill="{bg}"/>'
        else:
            bg_shape = f'<rect width="512" height="512" rx="102" fill="{bg}"/>'
        content = f'{bg_shape}\n  {svg_transform_mark(74, 112, 364, scheme)}'
        svg_specs.append((slug, 512, 512, f"Proprietary Systems {slug}", content, None))

    teal_content = (
        f'<defs><linearGradient id="appIconTeal" x1="0" y1="0" x2="512" y2="512" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{COLORS["mint"]}"/><stop offset="1" stop-color="{COLORS["teal"]}"/></linearGradient></defs>'
        f'\n  <rect width="512" height="512" rx="102" fill="url(#appIconTeal)"/>\n  {svg_transform_mark(74, 112, 364, "mono-white")}'
    )
    svg_specs.append(("app-icon-teal", 512, 512, "Proprietary Systems app icon teal", teal_content, None))
    svg_specs.append(("favicon", 512, 512, "Proprietary Systems favicon", f'<rect width="512" height="512" rx="102" fill="{COLORS["navy"]}"/>\n  {svg_transform_mark(74, 112, 364, "full-dark")}', None))

    for slug, width, height, title, content, bg in svg_specs:
        (DIRS["svg"] / f"{slug}.svg").write_text(svg_shell(width, height, title, content, bg), encoding="utf-8")


def write_pngs() -> None:
    def render(svg_name: str, output_path: Path, width: int | None = None, height: int | None = None) -> None:
        rsvg = shutil.which("rsvg-convert") or "/Users/research/.homebrew/bin/rsvg-convert"
        if Path(rsvg).exists():
            command = [rsvg]
            if width is not None:
                command.extend(["-w", str(width)])
            if height is not None:
                command.extend(["-h", str(height)])
            command.extend(["-o", str(output_path), str(DIRS["svg"] / svg_name)])
            subprocess.run(command, check=True)
            return

        # Fallback for systems that have CairoSVG plus discoverable native Cairo.
        import cairosvg

        kwargs: dict[str, int | str] = {"url": str(DIRS["svg"] / svg_name), "write_to": str(output_path)}
        if width is not None:
            kwargs["output_width"] = width
        if height is not None:
            kwargs["output_height"] = height
        cairosvg.svg2png(**kwargs)

    logo_exports = [
        ("primary-horizontal-lockup-on-dark.svg", "primary-horizontal-lockup-on-dark.png", 2400, 630),
        ("primary-horizontal-lockup.svg", "primary-horizontal-lockup-transparent.png", 2400, 630),
        ("secondary-horizontal-lockup-on-dark.svg", "secondary-horizontal-lockup-on-dark.png", 2400, 480),
        ("secondary-horizontal-lockup.svg", "secondary-horizontal-lockup-transparent.png", 2400, 480),
        ("monochrome-white-horizontal.svg", "monochrome-white-horizontal-transparent.png", 2040, 480),
        ("monochrome-white-horizontal-on-dark.svg", "monochrome-white-horizontal-on-dark.png", 2040, 480),
        ("monochrome-dark-horizontal.svg", "monochrome-dark-horizontal-transparent.png", 2040, 480),
        ("monochrome-dark-horizontal-on-light.svg", "monochrome-dark-horizontal-on-light.png", 2040, 480),
        ("stacked-logo-on-dark.svg", "stacked-logo-on-dark.png", 1600, 1600),
        ("icon-only-mark.svg", "icon-only-mark-transparent.png", 1024, 1024),
        ("wordmark-ps-ai-on-dark.svg", "wordmark-ps-ai-on-dark.png", 1400, 360),
        ("wordmark-ps-ai.svg", "wordmark-ps-ai-transparent.png", 1400, 360),
    ]
    for svg_name, png_name, width, height in logo_exports:
        render(svg_name, DIRS["png"] / png_name, width, height)

    icon_svg_names = {
        "dark": "app-icon-dark.svg",
        "light": "app-icon-light.svg",
        "teal": "app-icon-teal.svg",
        "black": "app-icon-black.svg",
        "circle": "app-icon-circle.svg",
    }
    for size in [1024, 512, 192, 180, 64, 32, 16]:
        for slug in ["dark", "light", "teal"]:
            render(icon_svg_names[slug], DIRS["icons"] / f"app-icon-{slug}-{size}.png", size, size)
        if size in {1024, 512}:
            for slug in ["black", "circle"]:
                render(icon_svg_names[slug], DIRS["icons"] / f"app-icon-{slug}-{size}.png", size, size)

    render("favicon.svg", DIRS["icons"] / "favicon-16.png", 16, 16)
    render("favicon.svg", DIRS["icons"] / "favicon-32.png", 32, 32)
    render("favicon.svg", DIRS["icons"] / "favicon-64.png", 64, 64)
    ico_images = [
        Image.open(DIRS["icons"] / "favicon-16.png"),
        Image.open(DIRS["icons"] / "favicon-32.png"),
        Image.open(DIRS["icons"] / "favicon-64.png"),
    ]
    ico_images[-1].save(DIRS["icons"] / "favicon.ico", sizes=[(16, 16), (32, 32), (64, 64)])

    # Preserve existing Stripe integration filenames while replacing the raster source.
    stripe_dir = WORKSPACE / "stripe-brand-assets"
    stripe_dir.mkdir(exist_ok=True)
    render("app-icon-dark.svg", stripe_dir / "ps-stripe-icon.png", 512, 512)
    render("monochrome-dark-horizontal-on-light.svg", stripe_dir / "ps-stripe-logo-horizontal.png", 1995, 300)
    render("primary-horizontal-lockup-on-dark.svg", stripe_dir / "ps-stripe-logo-dark-bg.png", 2117, 300)


def write_preview() -> None:
    preview = Canvas(1800, 1280, COLORS["off_white"], scale=2)
    heading_fill = COLORS["navy"]
    preview.tracked_text((46, 50), "PROPRIETARY SYSTEMS BRAND ASSETS", 28, heading_fill, 5, "la")

    def paste_png(path: Path, box: tuple[int, int, int, int]) -> None:
        image = Image.open(path).convert("RGBA")
        image.thumbnail((box[2], box[3]), Image.Resampling.LANCZOS)
        preview.image.alpha_composite(image, (box[0] * preview.scale, box[1] * preview.scale))

    paste_png(DIRS["png"] / "primary-horizontal-lockup-on-dark.png", (50, 100, 850, 240))
    paste_png(DIRS["png"] / "secondary-horizontal-lockup-on-dark.png", (50, 390, 850, 180))
    paste_png(DIRS["png"] / "stacked-logo-on-dark.png", (50, 680, 380, 380))
    paste_png(DIRS["png"] / "wordmark-ps-ai-on-dark.png", (510, 700, 430, 140))
    paste_png(DIRS["png"] / "monochrome-dark-horizontal-on-light.png", (510, 930, 640, 160))

    icon_specs = [
        DIRS["icons"] / "app-icon-dark-512.png",
        DIRS["icons"] / "app-icon-light-512.png",
        DIRS["icons"] / "app-icon-teal-512.png",
        DIRS["icons"] / "app-icon-black-512.png",
    ]
    for index, icon_path in enumerate(icon_specs):
        paste_png(icon_path, (1230 + index * 130, 745, 120, 120))

    color_x = 1220
    for index, (name, value) in enumerate(
        [
            ("#00E5C2", COLORS["mint"]),
            ("#0097A7", COLORS["teal"]),
            ("#0A2030", COLORS["navy"]),
            ("#F6FBFB", COLORS["off_white"]),
            ("#E6F2F2", COLORS["mist"]),
        ]
    ):
        x = color_x + index * 104
        preview.rounded((x, 1020, x + 80, 1100), 2, value)
        preview.text((x, 1120), name, 17, heading_fill, "la")

    preview.save(DIRS["preview"] / "proprietary-systems-logo-system-preview.png")


def write_fidelity_preview() -> None:
    reference_crop_path = DIRS["preview"] / "reference-icon-mark-crop.png"
    current_render_svg = DIRS["preview"] / "current-traced-icon-mark.svg"
    current_render_path = DIRS["preview"] / "current-traced-icon-mark.png"
    comparison_path = DIRS["preview"] / "mark-fidelity-comparison.png"

    retained_reference = DIRS["reference"] / "proprietary-systems-logo-spec.jpg"
    reference_source = REFERENCE_IMAGE if REFERENCE_IMAGE.exists() else retained_reference
    try:
        reference = Image.open(reference_source).convert("RGB")
    except PermissionError:
        reference = Image.open(retained_reference).convert("RGB")
    reference.crop((1130, 85, 1320, 235)).resize((760, 600), Image.Resampling.LANCZOS).save(reference_crop_path)

    current_render_svg.write_text(
        svg_shell(
            760,
            600,
            "Proprietary Systems traced mark fidelity render",
            f'<rect width="760" height="600" fill="{COLORS["navy"]}"/>\n'
            f'<svg x="0" y="0" width="760" height="600" viewBox="0 0 760 600">\n{svg_mark("full-dark")}\n  </svg>',
        ),
        encoding="utf-8",
    )
    rsvg = shutil.which("rsvg-convert") or "/Users/research/.homebrew/bin/rsvg-convert"
    subprocess.run([rsvg, "-w", "760", "-h", "600", "-o", str(current_render_path), str(current_render_svg)], check=True)

    comparison = Canvas(1600, 760, COLORS["off_white"], scale=2)
    comparison.tracked_text((50, 48), "MARK FIDELITY CHECK", 26, COLORS["navy"], 4, "la")
    comparison.text((50, 98), "Reference crop", 22, COLORS["navy"], "la")
    comparison.text((820, 98), "Current SVG render", 22, COLORS["navy"], "la")
    if reference_crop_path.exists():
        reference_image = Image.open(reference_crop_path).convert("RGBA").resize((760 * comparison.scale, 600 * comparison.scale), Image.Resampling.LANCZOS)
        comparison.image.alpha_composite(reference_image, (50 * comparison.scale, 130 * comparison.scale))
    current_image = Image.open(current_render_path).convert("RGBA").resize((760 * comparison.scale, 600 * comparison.scale), Image.Resampling.LANCZOS)
    comparison.image.alpha_composite(current_image, (820 * comparison.scale, 130 * comparison.scale))
    comparison.save(comparison_path)


def write_manifest() -> None:
    mode_aliases = {
        "lightMode": {
            "description": "Assets intended for light backgrounds or light UI chrome.",
            "headerLogo": "brand-assets/svg/primary-horizontal-lockup.svg",
            "compactLogo": "brand-assets/svg/secondary-horizontal-lockup.svg",
            "documentLogo": "brand-assets/svg/monochrome-dark-horizontal.svg",
            "wordmark": "brand-assets/svg/wordmark-ps-ai.svg",
            "iconMark": "brand-assets/svg/icon-only-mark.svg",
            "appIcon": "brand-assets/icons/app-icon-light-512.png",
            "recommendedTextColor": COLORS["navy"],
            "recommendedBackground": COLORS["off_white"],
            "tags": ["light-mode", "light-background", "navy-mark", "full-color"],
        },
        "darkMode": {
            "description": "Assets intended for navy, black, or dark UI backgrounds.",
            "headerLogo": "brand-assets/svg/primary-horizontal-lockup-on-dark.svg",
            "compactLogo": "brand-assets/svg/secondary-horizontal-lockup-on-dark.svg",
            "documentLogo": "brand-assets/svg/monochrome-white-horizontal.svg",
            "wordmark": "brand-assets/svg/wordmark-ps-ai-on-dark.svg",
            "iconMark": "brand-assets/svg/icon-only-mark.svg",
            "appIcon": "brand-assets/icons/app-icon-dark-512.png",
            "recommendedTextColor": COLORS["off_white"],
            "recommendedBackground": COLORS["navy"],
            "tags": ["dark-mode", "dark-background", "white-mark", "full-color"],
        },
        "modeIndependent": {
            "description": "Assets that work as standalone icons, favicons, or provider uploads.",
            "faviconSvg": "brand-assets/svg/favicon.svg",
            "faviconIco": "brand-assets/icons/favicon.ico",
            "appleTouchIcon": "brand-assets/icons/app-icon-dark-180.png",
            "pwaIcon192": "brand-assets/icons/app-icon-dark-192.png",
            "pwaIcon512": "brand-assets/icons/app-icon-dark-512.png",
            "socialAvatar": "brand-assets/icons/app-icon-dark-1024.png",
            "tags": ["mode-independent", "favicon", "app-icon", "social-avatar"],
        },
    }
    manifest = {
        "brand": "Proprietary Systems",
        "domain": "proprietarysystems.ai",
        "repository": {
            "github": "https://github.com/Proprietary-Systems/proprietary-systems-brand-assets",
            "ssh": "git@github.com-proprietarysystems:Proprietary-Systems/proprietary-systems-brand-assets.git",
            "rawBase": "https://raw.githubusercontent.com/Proprietary-Systems/proprietary-systems-brand-assets/main",
        },
        "generatedFrom": "brand-assets/scripts/build-brand-assets.py",
        "ecosystemRegistry": "brand-assets/ecosystem/registry.json",
        "reference": "brand-assets/reference/proprietary-systems-logo-spec.jpg",
        "colors": COLORS,
        "typography": {
            "primaryReference": "Geometric sans-serif",
            "preferredSystemFont": "Avenir Next",
            "svgFallback": "Avenir, Montserrat, Century Gothic, Arial, sans-serif",
        },
        "tooling": {
            "pythonRequirements": "brand-assets/requirements.txt",
            "primaryRenderer": "rsvg-convert",
            "nativeUtilities": ["cairo", "librsvg", "potrace", "imagemagick"],
            "buildScript": "brand-assets/scripts/build-brand-assets.py",
        },
        "qualityChecks": {
            "logoSystemPreview": "brand-assets/preview/proprietary-systems-logo-system-preview.png",
            "markFidelityComparison": "brand-assets/preview/mark-fidelity-comparison.png",
            "productIconContactSheet": "brand-assets/preview/product-illustrations-v4-light-contact-sheet.png",
            "productIconDarkContactSheet": "brand-assets/preview/product-illustrations-v4-dark-contact-sheet.png",
            "productIconLegibility": "brand-assets/preview/product-illustrations-v4-48px-legibility.png",
            "productDioramaContactSheet": "brand-assets/preview/product-illustrations-v3-light-contact-sheet.png",
            "productDioramaDarkContactSheet": "brand-assets/preview/product-illustrations-v3-dark-contact-sheet.png",
            "productDioramaThemeComparison": "brand-assets/preview/product-illustrations-v3-theme-comparison.png",
        },
        "sharedComponents": {
            "react": "brand-assets/components/index.ts",
            "logo": "brand-assets/components/ProprietarySystemsLogo.tsx",
            "productIllustration": "brand-assets/components/ProductIllustration.tsx",
            "productTile": "brand-assets/components/ProductTile.tsx",
            "appLauncher": "brand-assets/components/AppLauncher.tsx",
            "productCatalog": "brand-assets/components/productIllustrationCatalog.ts",
            "package": "brand-assets/package.json",
        },
        "integrationTemplates": {
            "modeAliases": "brand-assets/modes.json",
            "cssTokens": "brand-assets/css/proprietary-systems-brand.css",
            "webHead": "brand-assets/snippets/web-head.html",
            "landingHeader": "brand-assets/snippets/landing-header.html",
            "productHeader": "brand-assets/snippets/product-app-header.html",
            "checkoutLogo": "brand-assets/snippets/checkout-logo.html",
            "lightDarkUsage": "brand-assets/snippets/light-dark-usage.md",
            "stripeBranding": "brand-assets/checkout/stripe-branding.json",
            "webManifest": "brand-assets/web/site.webmanifest",
            "emailSignature": "brand-assets/email/signature.html",
            "emailSignatureCompact": "brand-assets/email/signature-compact.html",
            "integrationGuide": "brand-assets/docs/integration-guide.md",
            "agentPrompt": "brand-assets/docs/agent-prompt.md",
            "ecosystemRegistry": "brand-assets/ecosystem/registry.json",
            "productIllustrations": "brand-assets/svg/product-illustrations-v4/manifest.json",
            "productIllustrationsV3": "brand-assets/svg/product-illustrations-v3/manifest.json",
            "productIllustrationsV2": "brand-assets/svg/product-illustrations-v2/manifest.json",
            "productIllustrationsLegacy": "brand-assets/svg/product-illustrations/manifest.json",
            "appLauncherPreview": "brand-assets/preview/app-launcher/index.html",
        },
        "modeAliases": mode_aliases,
        "variants": {
            "primaryHorizontalLockup": {
                "svg": "brand-assets/svg/primary-horizontal-lockup.svg",
                "svgOnDark": "brand-assets/svg/primary-horizontal-lockup-on-dark.svg",
                "pngOnDark": "brand-assets/png/primary-horizontal-lockup-on-dark.png",
                "pngTransparent": "brand-assets/png/primary-horizontal-lockup-transparent.png",
                "tags": ["primary", "horizontal-lockup", "light-mode", "light-background", "full-color"],
            },
            "secondaryHorizontalLockup": {
                "svg": "brand-assets/svg/secondary-horizontal-lockup.svg",
                "svgOnDark": "brand-assets/svg/secondary-horizontal-lockup-on-dark.svg",
                "pngOnDark": "brand-assets/png/secondary-horizontal-lockup-on-dark.png",
                "pngTransparent": "brand-assets/png/secondary-horizontal-lockup-transparent.png",
                "tags": ["secondary", "horizontal-lockup", "compact", "light-mode", "light-background", "full-color"],
            },
            "stackedLogo": {
                "svg": "brand-assets/svg/stacked-logo.svg",
                "svgOnDark": "brand-assets/svg/stacked-logo-on-dark.svg",
                "pngOnDark": "brand-assets/png/stacked-logo-on-dark.png",
                "tags": ["stacked", "dark-mode", "dark-background", "presentation", "full-color"],
            },
            "iconOnlyMark": {
                "svg": "brand-assets/svg/icon-only-mark.svg",
                "pngTransparent": "brand-assets/png/icon-only-mark-transparent.png",
                "tags": ["icon-only", "mark", "transparent", "mode-flexible"],
            },
            "wordmarkPsAi": {
                "svg": "brand-assets/svg/wordmark-ps-ai.svg",
                "svgOnDark": "brand-assets/svg/wordmark-ps-ai-on-dark.svg",
                "pngOnDark": "brand-assets/png/wordmark-ps-ai-on-dark.png",
                "pngTransparent": "brand-assets/png/wordmark-ps-ai-transparent.png",
                "tags": ["wordmark", "ps-ai", "light-mode", "dark-mode"],
            },
            "monochromeWhite": {
                "svg": "brand-assets/svg/monochrome-white-horizontal.svg",
                "svgOnDark": "brand-assets/svg/monochrome-white-horizontal-on-dark.svg",
                "pngTransparent": "brand-assets/png/monochrome-white-horizontal-transparent.png",
                "pngOnDark": "brand-assets/png/monochrome-white-horizontal-on-dark.png",
                "tags": ["monochrome", "white", "dark-mode", "dark-background", "documents", "email"],
            },
            "monochromeDark": {
                "svg": "brand-assets/svg/monochrome-dark-horizontal.svg",
                "svgOnLight": "brand-assets/svg/monochrome-dark-horizontal-on-light.svg",
                "pngTransparent": "brand-assets/png/monochrome-dark-horizontal-transparent.png",
                "pngOnLight": "brand-assets/png/monochrome-dark-horizontal-on-light.png",
                "tags": ["monochrome", "dark", "light-mode", "light-background", "documents", "email"],
            },
            "appIcons": {
                "faviconSvg": "brand-assets/svg/favicon.svg",
                "faviconIco": "brand-assets/icons/favicon.ico",
                "dark1024": "brand-assets/icons/app-icon-dark-1024.png",
                "dark512": "brand-assets/icons/app-icon-dark-512.png",
                "dark192": "brand-assets/icons/app-icon-dark-192.png",
                "appleTouchIcon": "brand-assets/icons/app-icon-dark-180.png",
                "light1024": "brand-assets/icons/app-icon-light-1024.png",
                "teal1024": "brand-assets/icons/app-icon-teal-1024.png",
                "black1024": "brand-assets/icons/app-icon-black-1024.png",
                "circle1024": "brand-assets/icons/app-icon-circle-1024.png",
                "tags": ["app-icon", "favicon", "mode-independent", "social-avatar"],
            },
            "appLauncherTrigger": {
                "light": "brand-assets/svg/app-launcher-grid-light.svg",
                "dark": "brand-assets/svg/app-launcher-grid-dark.svg",
                "tags": ["application-launcher", "nine-dot-grid", "light-mode", "dark-mode"],
            },
        },
        "applications": {
            "stripe": {
                "icon": "stripe-brand-assets/ps-stripe-icon.png",
                "logoOnLight": "stripe-brand-assets/ps-stripe-logo-horizontal.png",
                "logoOnDark": "stripe-brand-assets/ps-stripe-logo-dark-bg.png",
            },
            "websiteAndApps": {
                "headerLogo": "brand-assets/svg/primary-horizontal-lockup.svg",
                "compactLogo": "brand-assets/svg/secondary-horizontal-lockup.svg",
                "favicon": "brand-assets/svg/favicon.svg",
                "pwaIcon192": "brand-assets/icons/app-icon-dark-192.png",
                "pwaIcon512": "brand-assets/icons/app-icon-dark-512.png",
                "appleTouchIcon": "brand-assets/icons/app-icon-dark-180.png",
                "launcherTriggerLight": "brand-assets/svg/app-launcher-grid-light.svg",
                "launcherTriggerDark": "brand-assets/svg/app-launcher-grid-dark.svg",
            },
            "githubOrgOrSocialProfile": {
                "avatar": "brand-assets/icons/app-icon-dark-1024.png",
                "lightAvatar": "brand-assets/icons/app-icon-light-1024.png",
            },
            "documentsSlidesEmail": {
                "darkOnLight": "brand-assets/svg/monochrome-dark-horizontal.svg",
                "whiteOnDark": "brand-assets/svg/monochrome-white-horizontal.svg",
                "stacked": "brand-assets/svg/stacked-logo.svg",
            },
            "productTiles": {
                "manifest": "brand-assets/svg/product-illustrations-v4/manifest.json",
                "preview": "brand-assets/svg/product-illustrations-v4/preview.html",
                "assetDirectory": "brand-assets/svg/product-illustrations-v4",
                "lightDirectory": "brand-assets/svg/product-illustrations-v4/light",
                "darkDirectory": "brand-assets/svg/product-illustrations-v4/dark",
                "v3Manifest": "brand-assets/svg/product-illustrations-v3/manifest.json",
                "v2Manifest": "brand-assets/svg/product-illustrations-v2/manifest.json",
                "legacyManifest": "brand-assets/svg/product-illustrations/manifest.json",
            },
        },
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (ROOT / "modes.json").write_text(json.dumps(mode_aliases, indent=2) + "\n", encoding="utf-8")


def copy_reference() -> None:
    if REFERENCE_IMAGE.exists():
        destination = DIRS["reference"] / "proprietary-systems-logo-spec.jpg"
        try:
            shutil.copy2(REFERENCE_IMAGE, destination)
        except PermissionError:
            if not destination.exists():
                raise
            print(f"Skipped inaccessible source reference; retained {destination}")


def build_product_illustrations() -> None:
    subprocess.run(
        [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / "scripts" / "build-product-illustrations-v4.py")],
        check=True,
    )
    subprocess.run(
        [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / "scripts" / "build-product-illustrations-v3.py")],
        check=True,
    )


def validate_ecosystem() -> None:
    subprocess.run(
        [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / "scripts" / "validate-ecosystem.py")],
        check=True,
    )


def main() -> None:
    ensure_dirs()
    copy_reference()
    write_svgs()
    write_pngs()
    write_preview()
    write_fidelity_preview()
    build_product_illustrations()
    write_manifest()
    validate_ecosystem()
    print(f"Generated Proprietary Systems brand assets in {ROOT}")


if __name__ == "__main__":
    main()
