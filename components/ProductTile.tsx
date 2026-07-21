import type { HTMLAttributes, ReactNode } from "react";

import { ProductIllustration, type ProductIllustrationMode } from "./ProductIllustration";
import {
  PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS,
  type ProprietarySystemsProductId,
} from "./productIllustrationCatalog";

export type ProductTileProps = Omit<HTMLAttributes<HTMLElement>, "children"> & {
  productId: ProprietarySystemsProductId;
  mode?: ProductIllustrationMode;
  basePath?: string;
  href?: string;
  description?: string;
  eyebrow?: ReactNode;
  trailing?: ReactNode;
};

export function ProductTile({
  productId,
  mode = "light",
  basePath = "/",
  href,
  description,
  eyebrow,
  trailing,
  className = "",
  ...articleProps
}: ProductTileProps) {
  const product = PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS[productId];
  const content = (
    <>
      <span className="ps-product-tile__visual" aria-hidden="true">
        <ProductIllustration productId={productId} mode={mode} basePath={basePath} decorative />
      </span>
      <span className="ps-product-tile__content">
        {eyebrow ? <span className="ps-product-tile__eyebrow">{eyebrow}</span> : null}
        <strong className="ps-product-tile__title">{product.label}</strong>
        <span className="ps-product-tile__description">{description ?? product.definition}</span>
      </span>
      {trailing ? <span className="ps-product-tile__trailing">{trailing}</span> : null}
    </>
  );

  return (
    <article
      className={`ps-product-tile ps-product-tile--${mode} ${className}`.trim()}
      data-ps-product={productId}
      {...articleProps}
    >
      {href ? (
        <a className="ps-product-tile__link" href={href}>
          {content}
        </a>
      ) : (
        <div className="ps-product-tile__link">{content}</div>
      )}
    </article>
  );
}
