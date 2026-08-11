#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAND_PREFIX = "brand-assets/"

NAVY = "#0A2030"
MINT = "#00E5C2"
TEAL = "#0097A7"
OFF_WHITE = "#F6FBFB"
WHITE = "#FFFFFF"


def fail(message: str) -> None:
    raise SystemExit(f"Logo mode validation failed: {message}")


def asset_path(value: str) -> Path:
    relative = value.removeprefix(BRAND_PREFIX)
    return ROOT / relative


def svg_colors(name: str) -> set[str]:
    path = ROOT / "svg" / name
    if not path.is_file():
        fail(f"missing SVG: {path.relative_to(ROOT)}")
    source = path.read_text(encoding="utf-8")
    return {value.upper() for value in re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', source)}


def expect_colors(name: str, *, required: set[str], forbidden: set[str] = frozenset()) -> None:
    colors = svg_colors(name)
    missing = required - colors
    unexpected = forbidden & colors
    if missing:
        fail(f"{name} is missing {sorted(missing)}; found {sorted(colors)}")
    if unexpected:
        fail(f"{name} contains forbidden surface colors {sorted(unexpected)}")


def expect_mode_path(mode: dict[str, object], key: str, expected: str) -> None:
    actual = mode.get(key)
    if actual != expected:
        fail(f"{key} expected {expected!r}, received {actual!r}")
    if not asset_path(expected).is_file():
        fail(f"{key} points to missing asset {expected}")


def main() -> None:
    light_assets = [
        "primary-horizontal-lockup.svg",
        "secondary-horizontal-lockup.svg",
        "wordmark-ps-ai.svg",
        "icon-only-mark-on-light.svg",
    ]
    for name in light_assets:
        expect_colors(name, required={NAVY, MINT}, forbidden={WHITE, OFF_WHITE})

    dark_assets = [
        "primary-horizontal-lockup-on-dark.svg",
        "secondary-horizontal-lockup-on-dark.svg",
        "wordmark-ps-ai-on-dark.svg",
        "icon-only-mark.svg",
    ]
    for name in dark_assets:
        expect_colors(name, required={OFF_WHITE if name == "icon-only-mark.svg" else WHITE, MINT})

    expect_colors("icon-only-mark-on-light.svg", required={NAVY, MINT, TEAL}, forbidden={WHITE, OFF_WHITE})
    expect_colors("icon-only-mark.svg", required={OFF_WHITE, MINT, TEAL})
    expect_colors("monochrome-dark-mark.svg", required={NAVY}, forbidden={MINT, TEAL, WHITE, OFF_WHITE})
    expect_colors("monochrome-white-mark.svg", required={WHITE}, forbidden={NAVY, MINT, TEAL, OFF_WHITE})

    modes = json.loads((ROOT / "modes.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if manifest.get("version") != package.get("version"):
        fail("manifest version does not match package.json")
    if manifest.get("modeAliases") != modes:
        fail("manifest modeAliases do not match modes.json")

    light = modes["lightMode"]
    dark = modes["darkMode"]
    expect_mode_path(light, "headerLogo", "brand-assets/svg/primary-horizontal-lockup.svg")
    expect_mode_path(light, "compactLogo", "brand-assets/svg/secondary-horizontal-lockup.svg")
    expect_mode_path(light, "wordmark", "brand-assets/svg/wordmark-ps-ai.svg")
    expect_mode_path(light, "iconMark", "brand-assets/svg/icon-only-mark-on-light.svg")
    expect_mode_path(light, "monochromeMark", "brand-assets/svg/monochrome-dark-mark.svg")
    expect_mode_path(dark, "headerLogo", "brand-assets/svg/primary-horizontal-lockup-on-dark.svg")
    expect_mode_path(dark, "compactLogo", "brand-assets/svg/secondary-horizontal-lockup-on-dark.svg")
    expect_mode_path(dark, "wordmark", "brand-assets/svg/wordmark-ps-ai-on-dark.svg")
    expect_mode_path(dark, "iconMark", "brand-assets/svg/icon-only-mark.svg")
    expect_mode_path(dark, "monochromeMark", "brand-assets/svg/monochrome-white-mark.svg")

    variants = manifest["variants"]
    if "mode-flexible" in variants["iconOnlyMark"].get("tags", []):
        fail("surface-specific icon mark is still tagged mode-flexible")

    required_pngs = [
        "png/icon-only-mark-on-light-transparent.png",
        "png/monochrome-dark-mark-transparent.png",
        "png/monochrome-white-mark-transparent.png",
    ]
    for relative in required_pngs:
        if not (ROOT / relative).is_file():
            fail(f"missing generated PNG: {relative}")

    component = (ROOT / "components" / "ProprietarySystemsLogo.tsx").read_text(encoding="utf-8")
    for expected in [
        'mark: "brand-assets/svg/icon-only-mark-on-light.svg"',
        'monochromeDarkMark: "brand-assets/svg/monochrome-dark-mark.svg"',
        'monochromeWhiteMark: "brand-assets/svg/monochrome-white-mark.svg"',
    ]:
        if expected not in component:
            fail(f"React mapping is missing {expected}")

    print("Logo surface modes validated")


if __name__ == "__main__":
    main()
