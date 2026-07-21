import type { ImgHTMLAttributes } from "react";

import {
  PROPRIETARY_SYSTEMS_PRODUCT_ALIASES,
  PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS,
  type ProprietarySystemsProductId,
} from "./productIllustrationCatalog";

export type ProprietarySystemsProductAlias = keyof typeof PROPRIETARY_SYSTEMS_PRODUCT_ALIASES;
export type ProprietarySystemsProductReference = ProprietarySystemsProductId | ProprietarySystemsProductAlias;
export type ProductIllustrationMode = "light" | "dark";

export type ProductIllustrationProps = Omit<ImgHTMLAttributes<HTMLImageElement>, "src"> & {
  productId: ProprietarySystemsProductReference;
  mode?: ProductIllustrationMode;
  basePath?: string;
  decorative?: boolean;
};

function normalizeBasePath(basePath: string) {
  return basePath.endsWith("/") ? basePath : `${basePath}/`;
}

export function resolveProprietarySystemsProductId(
  productId: ProprietarySystemsProductReference,
): ProprietarySystemsProductId {
  if (productId in PROPRIETARY_SYSTEMS_PRODUCT_ALIASES) {
    return PROPRIETARY_SYSTEMS_PRODUCT_ALIASES[productId as ProprietarySystemsProductAlias];
  }
  return productId as ProprietarySystemsProductId;
}

export function getProductIllustrationPath(
  productId: ProprietarySystemsProductReference,
  mode: ProductIllustrationMode = "light",
  basePath = "/",
) {
  const canonicalId = resolveProprietarySystemsProductId(productId);
  const asset = PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS[canonicalId];
  return `${normalizeBasePath(basePath)}${asset[mode]}`;
}

export function ProductIllustration({
  productId,
  mode = "light",
  basePath = "/",
  decorative = false,
  alt,
  ...imgProps
}: ProductIllustrationProps) {
  const canonicalId = resolveProprietarySystemsProductId(productId);
  const asset = PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS[canonicalId];

  return (
    <img
      src={getProductIllustrationPath(canonicalId, mode, basePath)}
      alt={decorative ? "" : (alt ?? asset.label)}
      aria-hidden={decorative || undefined}
      data-ps-product={canonicalId}
      data-ps-mode={mode}
      {...imgProps}
    />
  );
}
