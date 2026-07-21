import type { MouseEvent as ReactMouseEvent } from "react";
import { useCallback, useEffect, useId, useMemo, useRef, useState } from "react";

import { ProductIllustration, type ProductIllustrationMode } from "./ProductIllustration";
import {
  PROPRIETARY_SYSTEMS_FEATURED_PRODUCTS,
  PROPRIETARY_SYSTEMS_NAVIGATION_GROUPS,
  PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS,
  type ProprietarySystemsNavigationGroup,
  type ProprietarySystemsProductId,
  type ProprietarySystemsProductIllustration,
} from "./productIllustrationCatalog";

export type AppLauncherProps = {
  mode?: ProductIllustrationMode;
  basePath?: string;
  className?: string;
  align?: "start" | "end";
  triggerLabel?: string;
  organizationLabel?: string;
  featuredLabel?: string;
  allProductsLabel?: string;
  currentProductId?: ProprietarySystemsProductId;
  availableProductIds?: readonly ProprietarySystemsProductId[];
  featuredProductIds?: readonly ProprietarySystemsProductId[];
  groups?: readonly ProprietarySystemsNavigationGroup[];
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  onProductSelect?: (
    product: ProprietarySystemsProductIllustration,
    event: ReactMouseEvent<HTMLAnchorElement>,
  ) => void;
  resolveProductHref?: (product: ProprietarySystemsProductIllustration) => string;
};

function normalizeBasePath(basePath: string) {
  return basePath.endsWith("/") ? basePath : `${basePath}/`;
}

export function getAppLauncherGridIconPath(
  mode: ProductIllustrationMode = "light",
  basePath = "/",
) {
  return `${normalizeBasePath(basePath)}brand-assets/svg/app-launcher-grid-${mode}.svg`;
}

function getLauncherLabel(label: string) {
  return label.replace(/^PS\s+/, "").replace(/^Proprietary\s+/, "");
}

export function AppLauncher({
  mode = "light",
  basePath = "/",
  className = "",
  align = "end",
  triggerLabel = "Open Proprietary Systems applications",
  organizationLabel = "Proprietary Systems",
  featuredLabel = "Quick access",
  allProductsLabel = "All products",
  currentProductId,
  availableProductIds,
  featuredProductIds = PROPRIETARY_SYSTEMS_FEATURED_PRODUCTS,
  groups = PROPRIETARY_SYSTEMS_NAVIGATION_GROUPS,
  open,
  defaultOpen = false,
  onOpenChange,
  onProductSelect,
  resolveProductHref = (product) => product.defaultRoute,
}: AppLauncherProps) {
  const [uncontrolledOpen, setUncontrolledOpen] = useState(defaultOpen);
  const isControlled = open !== undefined;
  const isOpen = isControlled ? open : uncontrolledOpen;
  const panelId = useId();
  const launcherRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);

  const updateOpen = useCallback(
    (nextOpen: boolean) => {
      if (!isControlled) setUncontrolledOpen(nextOpen);
      onOpenChange?.(nextOpen);
    },
    [isControlled, onOpenChange],
  );

  const availableSet = useMemo(
    () =>
      new Set<ProprietarySystemsProductId>(
        availableProductIds ??
          (Object.keys(PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS) as ProprietarySystemsProductId[]),
      ),
    [availableProductIds],
  );

  const featuredProducts = useMemo(
    () =>
      featuredProductIds
        .filter((productId) => availableSet.has(productId))
        .map((productId) => PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS[productId]),
    [availableSet, featuredProductIds],
  );

  const availableGroups = useMemo(
    () =>
      groups
        .map((group) => ({
          ...group,
          products: group.products.filter((productId) => availableSet.has(productId)),
        }))
        .filter((group) => group.products.length > 0),
    [availableSet, groups],
  );

  useEffect(() => {
    if (!isOpen) return;

    const handlePointerDown = (event: PointerEvent) => {
      if (!launcherRef.current?.contains(event.target as Node)) updateOpen(false);
    };
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      event.preventDefault();
      updateOpen(false);
      triggerRef.current?.focus();
    };

    document.addEventListener("pointerdown", handlePointerDown);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("pointerdown", handlePointerDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, updateOpen]);

  useEffect(() => {
    if (!isOpen) return;
    const frame = window.requestAnimationFrame(() => {
      launcherRef.current?.querySelector<HTMLAnchorElement>(".ps-app-launcher__product")?.focus();
    });
    return () => window.cancelAnimationFrame(frame);
  }, [isOpen]);

  const renderProduct = (product: ProprietarySystemsProductIllustration) => (
    <a
      className="ps-app-launcher__product"
      href={resolveProductHref(product)}
      key={product.id}
      aria-current={product.id === currentProductId ? "page" : undefined}
      title={product.definition}
      onClick={(event) => {
        onProductSelect?.(product, event);
        if (!event.defaultPrevented) updateOpen(false);
      }}
    >
      <span className="ps-app-launcher__product-visual" aria-hidden="true">
        <ProductIllustration productId={product.id} mode={mode} basePath={basePath} decorative />
      </span>
      <span className="ps-app-launcher__product-label">{getLauncherLabel(product.label)}</span>
    </a>
  );

  return (
    <div
      ref={launcherRef}
      className={`ps-app-launcher ps-app-launcher--${align} ps-app-launcher--${mode} ${className}`.trim()}
      data-ps-mode={mode}
    >
      <button
        ref={triggerRef}
        className="ps-app-launcher__trigger"
        type="button"
        aria-label={triggerLabel}
        aria-haspopup="dialog"
        aria-expanded={isOpen}
        aria-controls={panelId}
        onClick={() => updateOpen(!isOpen)}
      >
        <img src={getAppLauncherGridIconPath(mode, basePath)} alt="" aria-hidden="true" />
      </button>

      {isOpen ? (
        <div
          className="ps-app-launcher__panel"
          id={panelId}
          role="dialog"
          aria-label="Proprietary Systems applications"
        >
          <header className="ps-app-launcher__header">
            <span className="ps-app-launcher__brand-dot" aria-hidden="true" />
            <span>
              <strong>Applications</strong>
              <small>{organizationLabel}</small>
            </span>
          </header>

          {featuredProducts.length > 0 ? (
            <section className="ps-app-launcher__section" aria-labelledby={`${panelId}-featured`}>
              <h2 id={`${panelId}-featured`}>{featuredLabel}</h2>
              <div className="ps-app-launcher__grid">{featuredProducts.map(renderProduct)}</div>
            </section>
          ) : null}

          <div className="ps-app-launcher__all-products">
            <h2>{allProductsLabel}</h2>
            {availableGroups.map((group) => (
              <section
                className="ps-app-launcher__section ps-app-launcher__section--group"
                aria-labelledby={`${panelId}-${group.id}`}
                key={group.id}
              >
                <h3 id={`${panelId}-${group.id}`}>{group.label}</h3>
                <div className="ps-app-launcher__grid">
                  {group.products.map((productId) =>
                    renderProduct(PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS[productId]),
                  )}
                </div>
              </section>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}
