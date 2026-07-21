# Proprietary Systems Brand Integration Guide

Use `brand-assets/manifest.json` as the canonical lookup table. The snippets here assume the asset folder is served at `/brand-assets`.

For light/dark selection, use `brand-assets/modes.json`.

For application consumption, use `brand-assets/ecosystem/registry.json` for product labels, application routes, navigation groups, technical boundaries, hostnames, and product illustrations. Architecture authors must make topology changes in `architecture/catalog/system.json` first; the control-plane verifier prevents the presentation registry from drifting from it.

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
- Build launchers and product navigation from `brand-assets/ecosystem/registry.json`.
- Use the shared `ProductIllustration`, `ProductTile`, and `AppLauncher` React components instead of reconstructing asset paths.

```tsx
import {
  AppLauncher,
  ProductIllustration,
  ProductTile,
  ProprietarySystemsLogo,
} from "@proprietary-systems/brand-assets/react";

<ProprietarySystemsLogo mode="dark" intent="compact" />
<ProductIllustration productId="ps-crm" mode="dark" />
<ProductTile productId="ps-projects" mode="light" href="/projects" />
<AppLauncher mode="light" currentProductId="ps-crm" />
```

The launcher defaults to a three-column quick-access grid followed by the canonical product groups. Use `availableProductIds` to filter it through tenant entitlements; do not fork the component or maintain a second product map.

Do not use the deprecated `ps-portal` or `peter-studio` names for new work. They resolve to `ps-home` and `ps-creatives` only as compatibility aliases. Use `ps-client-portal` for the external customer-facing portal.

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

The target asset host is `assets.proprietarysystems.ai`; same-origin `/brand-assets` remains the recommended deployment path until that versioned asset host is live.

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
