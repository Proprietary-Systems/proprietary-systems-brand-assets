#!/usr/bin/env python3
"""Validate the PS ecosystem, host map, and V4 product illustration contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "ecosystem" / "registry.json"
ILLUSTRATION_MANIFEST_PATH = ROOT / "svg" / "product-illustrations-v4" / "manifest.json"
HOST_PATTERN = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> None:
    errors: list[str] = []
    registry = json.loads(REGISTRY_PATH.read_text())
    manifest = json.loads(ILLUSTRATION_MANIFEST_PATH.read_text())

    if registry.get("schemaVersion") != 1:
        fail(errors, "ecosystem registry schemaVersion must be 1")

    products = registry.get("products", [])
    ids = [product.get("id") for product in products]
    if len(ids) != len(set(ids)):
        fail(errors, "ecosystem registry contains duplicate product ids")

    product_by_id = {product["id"]: product for product in products}
    navigation_ids: list[str] = []
    category_ids = {group["id"] for group in registry.get("navigation", [])}
    for group in registry.get("navigation", []):
        for product_id in group.get("products", []):
            navigation_ids.append(product_id)
            product = product_by_id.get(product_id)
            if product is None:
                fail(errors, f"navigation references unknown product {product_id}")
            elif product.get("category") != group.get("id"):
                fail(errors, f"{product_id} category does not match navigation group {group.get('id')}")

    if len(navigation_ids) != len(set(navigation_ids)):
        fail(errors, "a product appears in more than one navigation group")
    if set(navigation_ids) != set(ids):
        missing = sorted(set(ids) - set(navigation_ids))
        extra = sorted(set(navigation_ids) - set(ids))
        fail(errors, f"navigation/product mismatch; missing={missing}, extra={extra}")

    launcher = registry.get("launcher", {})
    featured_ids = launcher.get("featuredProducts", [])
    if launcher.get("columns") != 3:
        fail(errors, "launcher must use the canonical three-column product grid")
    if len(featured_ids) != len(set(featured_ids)):
        fail(errors, "launcher featuredProducts contains duplicates")
    for product_id in featured_ids:
        if product_id not in product_by_id:
            fail(errors, f"launcher references unknown featured product {product_id}")

    for product in products:
        product_id = product["id"]
        for field in ("label", "productClass", "slug", "category", "technicalBoundary", "defaultRoute", "marketingPath", "definition", "visual"):
            if not product.get(field):
                fail(errors, f"{product_id} is missing {field}")
        if product.get("category") not in category_ids:
            fail(errors, f"{product_id} uses unknown category {product.get('category')}")
        if product.get("includedInSuite") is not True:
            fail(errors, f"{product_id} must be available through the suite")
        product_class = product.get("productClass")
        if product_class not in {"suite-home", "suite-module", "external-surface"}:
            fail(errors, f"{product_id} uses unsupported productClass {product_class}")
        if product_class == "suite-home" and product.get("defaultRoute") != "/":
            fail(errors, f"{product_id} suite-home must use /")
        if product_class == "suite-module" and not re.match(r"^/[^/]", product.get("defaultRoute", "")):
            fail(errors, f"{product_id} suite-module must use a non-root suite route")
        if product_class == "external-surface" and not product.get("defaultRoute", "").startswith("https://"):
            fail(errors, f"{product_id} external-surface must use an absolute reviewed host")

    home_ids = [product["id"] for product in products if product.get("productClass") == "suite-home"]
    if home_ids != ["ps-home"]:
        fail(errors, f"suite-home must be exactly ps-home; found={home_ids}")

    hosts: list[str] = []
    hosts.extend(entry["host"] for entry in registry["hosts"].get("canonical", []))
    for host_set in registry["hosts"].get("separateRuntimeProducts", {}).values():
        hosts.extend(host_set.values())
    hosts.extend(entry["host"] for entry in registry["hosts"].get("migrations", []))
    hosts.extend(entry["host"] for entry in registry["hosts"].get("clientDelivery", []))
    hosts.extend(entry["host"] for entry in registry["hosts"].get("retired", []))
    if len(hosts) != len(set(hosts)):
        fail(errors, "host map contains duplicate hostnames")
    for host in hosts:
        if not HOST_PATTERN.match(host):
            fail(errors, f"invalid hostname: {host}")

    active_host_text = json.dumps({
        "canonical": registry["hosts"].get("canonical", []),
        "separateRuntimeProducts": registry["hosts"].get("separateRuntimeProducts", {}),
        "migrations": registry["hosts"].get("migrations", []),
        "clientDelivery": registry["hosts"].get("clientDelivery", []),
    }).lower()
    if "root2roof" in active_host_text or "roofexteriors" in active_host_text:
        fail(errors, "Root2Roof may only appear in the retired host archive")
    if "projectimpact" in json.dumps(registry).lower():
        fail(errors, "Project Impact may not appear in the PS ecosystem registry")

    manifest_products = {product["id"]: product for product in manifest.get("products", [])}
    if set(manifest_products) != set(product_by_id):
        missing = sorted(set(product_by_id) - set(manifest_products))
        extra = sorted(set(manifest_products) - set(product_by_id))
        fail(errors, f"V4 illustration/product mismatch; missing={missing}, extra={extra}")

    for product_id, illustration in manifest_products.items():
        product = product_by_id[product_id]
        for field in ("label", "productClass", "category", "technicalBoundary", "defaultRoute", "marketingPath", "definition"):
            if illustration.get(field) != product.get(field):
                fail(
                    errors,
                    f"V4 illustration manifest {product_id}.{field} does not match the ecosystem registry",
                )
        for variant_path in illustration.get("variants", {}).values():
            asset = ILLUSTRATION_MANIFEST_PATH.parent / variant_path
            if not asset.exists():
                fail(errors, f"missing illustration asset for {product_id}: {variant_path}")

    aliases = registry.get("aliases", {})
    for alias, canonical in aliases.items():
        if alias in product_by_id:
            fail(errors, f"deprecated alias {alias} may not be an active product")
        if canonical not in product_by_id:
            fail(errors, f"alias {alias} points to unknown product {canonical}")

    runtime_repositories: dict[str, list[str]] = {}
    repository_groups = (
        registry.get("repositories", {}).get("canonical", [])
        + registry.get("repositories", {}).get("consolidate", [])
    )
    for repository in repository_groups:
        repository_name = repository.get("name", "unknown")
        for product_id in repository.get("runtimeProducts", []):
            if product_id not in product_by_id:
                fail(errors, f"repository {repository_name} owns unknown product {product_id}")
            else:
                runtime_repositories.setdefault(product_id, []).append(repository_name)
    if set(runtime_repositories) != set(ids):
        missing = sorted(set(ids) - set(runtime_repositories))
        extra = sorted(set(runtime_repositories) - set(ids))
        fail(errors, f"repository runtime coverage mismatch; missing={missing}, extra={extra}")

    if errors:
        print("Ecosystem validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Ecosystem ok: {len(products)} products, {len(hosts)} hosts, {len(registry.get('navigation', []))} launcher groups")


if __name__ == "__main__":
    main()
