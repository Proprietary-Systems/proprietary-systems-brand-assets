# Proprietary Systems Ecosystem Registry

`registry.json` is the published presentation contract for the Proprietary Systems suite. It projects the product names, navigation groups, routes, technical-boundary labels, and illustration mapping that application shells need.

The authored architecture authority is `../../architecture/catalog/system.json`. The generated handoff for shells is `../../architecture/generated/PRODUCT_NAVIGATION_REGISTRY.json`. This registry may add presentation metadata, but it must not contradict the catalog's product IDs, labels, categories, application locations, or marketing locations.

This registry publishes:

- the organization and workspace model;
- product names, meanings, routes, and technical boundaries;
- promoted launcher groups and the explicit hidden-product projection;
- canonical, separate-runtime, migration, client-delivery, and retired hostnames;
- the mapping from every product to its V4 light/dark illustration.

## Boundary Rules

- A customer business is a tenant of Proprietary Systems, not a project in the PS product catalog.
- One tenant receives one connected workspace by default. Divisions, departments, locations, and teams live inside it.
- Every product is accessible through the suite. Launcher promotion is separate from direct-route access. A separate runtime or data plane is a security and operational boundary, not a separate customer identity.
- Core module marketing pages use `proprietarysystems.ai/products/{slug}` and open routes under `app.proprietarysystems.ai`.
- Dialer, Email Signatures, and Places use the suite marketing and application routes; current browser hosts remain compatibility evidence, while bounded APIs and data planes remain independent where justified.
- `PS Home` is the internal application launcher. `Client Portal` is the external customer-facing collaboration surface.
- `PS Creatives` is the core visual-design and creative-production product. `peter-studio` is only a compatibility alias.
- Customer websites use customer-owned domains. Temporary client staging hosts are not product hosts.

## Consumers

Applications should consume the published `@proprietary-systems/brand-assets/ecosystem` export or a versioned package copy. They should not maintain their own product labels, routes, hostname rules, or illustration maps. Architecture changes begin in the control-plane catalog; presentation-only additions begin here.

Run `npm run verify:ecosystem` after changing the registry or illustrations, then run `../../scripts/verify-control-plane.sh` to prove that the published projection still matches the authored architecture.

The registry also records the three-column launcher contract, featured products, and the canonical runtime repository owner for every product.
