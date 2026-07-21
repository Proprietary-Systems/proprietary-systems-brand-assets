# Product Diorama QA

Reviewed at `320 × 240` and approximately `200 × 150` product-card size.

## System checks

- 15 of 15 SVGs parse as valid XML.
- Every asset uses `viewBox="0 0 320 240"`.
- No raster images, external URLs, embedded fonts, or text nodes.
- All assets render through `rsvg-convert`.
- Product labels remain outside the SVG and belong to the consuming tile.
- The original flat v1 set remains available as a legacy fallback.

## Visual review

| Product | Primary read | Result |
| --- | --- | --- |
| Peter.ai | Operator on a command pedestal | Pass |
| PS CRM | Records moving through pipeline stages | Pass |
| PS Prospect | Radar identifying a contact | Pass |
| PS Outreach | Connected email, call, and message sequence | Pass after scale refinement |
| PS Dialer | Call hub, queue, and waveform | Pass |
| PS Contracts | Agreement, signing field, and execution shield | Pass |
| PS Signatures | Branded email identity card | Pass |
| PS Finance | Forecast wall, allocation chart, and bars | Pass |
| PS People | Leadership-to-team organization structure | Pass |
| PS Docs | Editable document with comment and cursor | Pass |
| PS Automate | Trigger, workflow router, and completed action | Pass |
| PS Sites | Website canvas and editing tools | Pass |
| PS Projects | Work moving across delivery stages | Pass |
| PS Portal | Secure client room with files and approval | Pass |
| PS Territory | Market map, boundaries, pins, and scorecard | Pass |

## Strongest flagship candidates

1. PS CRM
2. PS Prospect
3. PS Contracts
4. PS Finance
5. PS Sites
6. PS Territory

These six establish the core spatial grammar for future additions. Peter.ai is intentionally more character-led, while the remaining products inherit the same lighting, depth, and palette rules without copying the same composition.
