# Agent Prompt

Use this prompt when asking another agent to use the Proprietary Systems brand package:

```text
Use the canonical Proprietary Systems brand assets from the GitHub repo:
Proprietary-Systems/proprietary-systems-brand-assets

GitHub URL:
https://github.com/Proprietary-Systems/proprietary-systems-brand-assets

Raw base:
https://raw.githubusercontent.com/Proprietary-Systems/proprietary-systems-brand-assets/main

On this Mac, the local source is:
/Users/research/Projects/ps-projects/ps-internal/brand-assets

Start with:
manifest.json
modes.json
docs/integration-guide.md

Choose assets by mode:
- Light UI: lightMode in modes.json, or modeAliases.lightMode in manifest.json
- Dark UI: darkMode in modes.json, or modeAliases.darkMode in manifest.json
- Favicons/app/social: modeIndependent in modes.json, or modeAliases.modeIndependent in manifest.json

Do not redraw or regenerate the logo unless explicitly asked. Copy or serve the package at /brand-assets in web apps. Use SVG for web UI, PNG for email/client dashboards, and stripe-brand-assets files for Stripe dashboard uploads.
```
