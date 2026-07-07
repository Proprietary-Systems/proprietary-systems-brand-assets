# Proprietary Systems Brand Assets

This directory contains the canonical Proprietary Systems logo package derived from the supplied brand specification image.

## Canonical Colors

| Name | Hex |
| --- | --- |
| Mint | `#00E5C2` |
| Teal | `#0097A7` |
| Navy | `#0A2030` |
| Off white | `#F6FBFB` |
| Mist | `#E6F2F2` |

## Asset Locations

| Use | Path |
| --- | --- |
| Full manifest | `brand-assets/manifest.json` |
| Light/dark mode aliases | `brand-assets/modes.json` |
| SVG masters | `brand-assets/svg/` |
| PNG lockups | `brand-assets/png/` |
| App icons and favicons | `brand-assets/icons/` |
| Shared React helper | `brand-assets/components/ProprietarySystemsLogo.tsx` |
| CSS tokens/classes | `brand-assets/css/proprietary-systems-brand.css` |
| Landing/product/checkout snippets | `brand-assets/snippets/` |
| Email signature templates | `brand-assets/email/` |
| Web manifest | `brand-assets/web/site.webmanifest` |
| Checkout provider mapping | `brand-assets/checkout/stripe-branding.json` |
| Integration guide | `brand-assets/docs/integration-guide.md` |
| Visual QA sheet | `brand-assets/preview/proprietary-systems-logo-system-preview.png` |
| Mark fidelity QA | `brand-assets/preview/mark-fidelity-comparison.png` |
| Source spec image | `brand-assets/reference/proprietary-systems-logo-spec.jpg` |

## Application Mapping

| Application surface | Canonical asset |
| --- | --- |
| Stripe icon | `stripe-brand-assets/ps-stripe-icon.png` |
| Stripe logo on light | `stripe-brand-assets/ps-stripe-logo-horizontal.png` |
| Stripe logo on dark | `stripe-brand-assets/ps-stripe-logo-dark-bg.png` |
| Website header | `brand-assets/svg/primary-horizontal-lockup.svg` |
| Website compact/header fallback | `brand-assets/svg/secondary-horizontal-lockup.svg` |
| Favicon SVG | `brand-assets/svg/favicon.svg` |
| Favicon ICO | `brand-assets/icons/favicon.ico` |
| PWA 192 icon | `brand-assets/icons/app-icon-dark-192.png` |
| PWA 512 icon | `brand-assets/icons/app-icon-dark-512.png` |
| Apple touch icon | `brand-assets/icons/app-icon-dark-180.png` |
| GitHub/social avatar | `brand-assets/icons/app-icon-dark-1024.png` |
| Documents on light | `brand-assets/svg/monochrome-dark-horizontal.svg` |
| Documents on dark | `brand-assets/svg/monochrome-white-horizontal.svg` |

## Light And Dark Mode

Use `brand-assets/modes.json` when an app needs to choose assets programmatically.

| Surface mode | Header | Compact | Document/email | App/social |
| --- | --- | --- | --- | --- |
| Light UI | `brand-assets/svg/primary-horizontal-lockup.svg` | `brand-assets/svg/secondary-horizontal-lockup.svg` | `brand-assets/svg/monochrome-dark-horizontal.svg` | `brand-assets/icons/app-icon-light-512.png` |
| Dark UI | `brand-assets/svg/primary-horizontal-lockup-on-dark.svg` | `brand-assets/svg/secondary-horizontal-lockup-on-dark.svg` | `brand-assets/svg/monochrome-white-horizontal.svg` | `brand-assets/icons/app-icon-dark-512.png` |

React callers can use:

```tsx
<ProprietarySystemsLogo mode="light" intent="header" />
<ProprietarySystemsLogo mode="dark" intent="compact" />
```

## Integration Surfaces

Use `brand-assets/docs/integration-guide.md` for landing pages, product apps, checkout pages, and email signatures. Templates use `/brand-assets` for same-origin web assets and `{{ASSET_BASE_URL}}` for email signatures that require public HTTPS image URLs.

## GitHub Access

Shared repo:

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

Clone with the PS SSH alias on this Mac. On other computers, use the GitHub URL for `Proprietary-Systems/proprietary-systems-brand-assets`.

## Rebuild

The generator uses SVG masters plus native rendering tools so PNG exports stay consistent.

```bash
brew install cairo librsvg potrace imagemagick
python3 -m venv brand-assets/.venv
brand-assets/.venv/bin/python -m pip install -r brand-assets/requirements.txt
brand-assets/.venv/bin/python brand-assets/scripts/build-brand-assets.py
```

`rsvg-convert` from `librsvg` is the primary renderer. `potrace` and `vtracer` are installed as tracing fallbacks for future raster-only source cleanup, not as the default source of truth.
