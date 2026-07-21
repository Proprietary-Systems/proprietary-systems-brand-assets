import { useState } from "react";
import { createRoot } from "react-dom/client";

import { AppLauncher } from "../../components/AppLauncher";
import { ProductIllustration } from "../../components/ProductIllustration";
import {
  PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS,
  type ProprietarySystemsProductId,
} from "../../components/productIllustrationCatalog";
import "../../css/proprietary-systems-brand.css";
import "./preview.css";

function Preview() {
  const [mode, setMode] = useState<"light" | "dark">("light");
  const [selectedProductId, setSelectedProductId] = useState<ProprietarySystemsProductId>("ps-home");
  const selectedProduct = PROPRIETARY_SYSTEMS_PRODUCT_ILLUSTRATIONS[selectedProductId];

  return (
    <main className={`launcher-preview launcher-preview--${mode}`}>
      <header className="launcher-preview__topbar">
        <a className="launcher-preview__brand" href="#workspace" aria-label="Proprietary Systems home">
          <img src={`/brand-assets/svg/icon-only-mark.svg`} alt="" aria-hidden="true" />
          <span>
            <strong>Proprietary Systems</strong>
            <small>Business operating system</small>
          </span>
        </a>

        <div className="launcher-preview__actions">
          <button
            className="launcher-preview__mode"
            type="button"
            onClick={() => setMode((current) => (current === "light" ? "dark" : "light"))}
          >
            {mode === "light" ? "Dark mode" : "Light mode"}
          </button>
          <AppLauncher
            mode={mode}
            basePath="/"
            currentProductId={selectedProductId}
            resolveProductHref={() => "#selected-product"}
            onProductSelect={(product) => setSelectedProductId(product.id)}
          />
          <button className="launcher-preview__avatar" type="button" aria-label="Open account menu">
            BR
          </button>
        </div>
      </header>

      <section className="launcher-preview__workspace" id="workspace">
        <div className="launcher-preview__eyebrow">One workspace · every product</div>
        <h1>Run the business from one connected system.</h1>
        <p>
          The launcher keeps every PS product understandable, reachable, and organized without turning the
          primary navigation into a mega-sidebar.
        </p>

        <div className="launcher-preview__cards">
          <article className="launcher-preview__card launcher-preview__card--selected" id="selected-product">
            <ProductIllustration productId={selectedProductId} mode={mode} basePath="/" decorative />
            <span>
              <small>Current product</small>
              <strong>{selectedProduct.label}</strong>
              <p>{selectedProduct.definition}</p>
            </span>
          </article>
          <article className="launcher-preview__card">
            <span className="launcher-preview__metric">23</span>
            <span>
              <small>Connected products</small>
              <strong>One organization context</strong>
              <p>Shared identity, permissions, search, files, integrations, and audit.</p>
            </span>
          </article>
          <article className="launcher-preview__card">
            <span className="launcher-preview__metric">3</span>
            <span>
              <small>Specialized data planes</small>
              <strong>Dialer, Email Signatures, Places</strong>
              <p>Independent runtimes where scale or evidence requires it, still inside the suite.</p>
            </span>
          </article>
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<Preview />);
