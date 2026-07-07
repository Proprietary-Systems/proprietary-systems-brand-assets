# Proprietary Systems Brand Integration Guide

Use `brand-assets/manifest.json` as the canonical lookup table. The snippets here assume the asset folder is served at `/brand-assets`.

For light/dark selection, use `brand-assets/modes.json`.

| Need | Light mode | Dark mode |
| --- | --- | --- |
| Header logo | `brand-assets/svg/primary-horizontal-lockup.svg` | `brand-assets/svg/primary-horizontal-lockup-on-dark.svg` |
| Compact header/app nav | `brand-assets/svg/secondary-horizontal-lockup.svg` | `brand-assets/svg/secondary-horizontal-lockup-on-dark.svg` |
| Documents/email | `brand-assets/svg/monochrome-dark-horizontal.svg` | `brand-assets/svg/monochrome-white-horizontal.svg` |
| Wordmark | `brand-assets/svg/wordmark-ps-ai.svg` | `brand-assets/svg/wordmark-ps-ai-on-dark.svg` |
| App/social icon | `brand-assets/icons/app-icon-light-512.png` | `brand-assets/icons/app-icon-dark-512.png` |

## Landing Pages

- Include `brand-assets/css/proprietary-systems-brand.css`.
- Add the favicon head tags from `brand-assets/snippets/web-head.html`.
- Use `brand-assets/snippets/landing-header.html` for a primary header lockup.
- Prefer SVG logos for page UI and PNG only where a platform rejects SVG.

## Product Apps

- Use `brand-assets/snippets/product-app-header.html` for dense app headers.
- Use `brand-assets/svg/icon-only-mark.svg` for compact sidebars, launchers, and pinned navigation.
- Use app icons from `brand-assets/icons/` for mobile/PWA surfaces.

## Checkout Pages

- Use `brand-assets/checkout/stripe-branding.json` for upload paths and theme colors.
- Use `brand-assets/snippets/checkout-logo.html` for custom checkout pages that support local assets.
- Stripe dashboard uploads should use the files in `stripe-brand-assets/`.

## Email Signatures

- Email clients should use hosted PNGs, not SVG.
- Upload or serve `brand-assets/png/monochrome-dark-horizontal-transparent.png` and `brand-assets/icons/app-icon-dark-64.png` from an HTTPS origin.
- Replace `{{ASSET_BASE_URL}}`, `{{NAME}}`, and `{{TITLE}}` in the templates under `brand-assets/email/`.

## Recommended Public Hosting Layout

```text
https://proprietarysystems.ai/brand-assets/svg/...
https://proprietarysystems.ai/brand-assets/png/...
https://proprietarysystems.ai/brand-assets/icons/...
https://proprietarysystems.ai/brand-assets/web/site.webmanifest
```

## GitHub Reference

Preferred shared source repo:

```text
Proprietary-Systems/proprietary-systems-brand-assets
```

GitHub URL:

```text
https://github.com/Proprietary-Systems/proprietary-systems-brand-assets
```

Local PS SSH remote:

```text
git@github.com-proprietarysystems:Proprietary-Systems/proprietary-systems-brand-assets.git
```

Raw asset base:

```text
https://raw.githubusercontent.com/Proprietary-Systems/proprietary-systems-brand-assets/main
```

Agent instruction:

```text
Read manifest.json and modes.json first. Do not redraw the logo. Choose assets by light/dark mode from modes.json, then copy or serve the package at /brand-assets.
```
