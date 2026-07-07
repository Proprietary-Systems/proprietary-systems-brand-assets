# Light/Dark Brand Asset Calls

Use `brand-assets/modes.json` for programmatic lookup.

## HTML

```html
<!-- Light UI -->
<img src="/brand-assets/svg/primary-horizontal-lockup.svg" alt="Proprietary Systems">

<!-- Dark UI -->
<img src="/brand-assets/svg/primary-horizontal-lockup-on-dark.svg" alt="Proprietary Systems">
```

## React

```tsx
import { ProprietarySystemsLogo } from "./brand-assets/components";

export function HeaderLogo({ dark = false }: { dark?: boolean }) {
  return <ProprietarySystemsLogo mode={dark ? "dark" : "light"} intent="header" />;
}
```

## CSS Theme Switch

```css
[data-theme="light"] .ps-logo {
  content: url("/brand-assets/svg/primary-horizontal-lockup.svg");
}

[data-theme="dark"] .ps-logo {
  content: url("/brand-assets/svg/primary-horizontal-lockup-on-dark.svg");
}
```

