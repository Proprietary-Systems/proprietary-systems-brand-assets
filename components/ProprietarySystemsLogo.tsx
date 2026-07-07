import type { ImgHTMLAttributes } from "react";

export type ProprietarySystemsLogoVariant =
  | "primary"
  | "primaryOnDark"
  | "secondary"
  | "secondaryOnDark"
  | "stacked"
  | "icon"
  | "wordmark"
  | "monochromeWhite"
  | "monochromeDark"
  | "favicon";

export type ProprietarySystemsLogoMode = "light" | "dark" | "any";

export type ProprietarySystemsLogoIntent =
  | "header"
  | "compact"
  | "document"
  | "wordmark"
  | "mark"
  | "appIcon"
  | "favicon"
  | "socialAvatar";

const LOGO_PATHS: Record<ProprietarySystemsLogoVariant, string> = {
  primary: "brand-assets/svg/primary-horizontal-lockup.svg",
  primaryOnDark: "brand-assets/svg/primary-horizontal-lockup-on-dark.svg",
  secondary: "brand-assets/svg/secondary-horizontal-lockup.svg",
  secondaryOnDark: "brand-assets/svg/secondary-horizontal-lockup-on-dark.svg",
  stacked: "brand-assets/svg/stacked-logo.svg",
  icon: "brand-assets/svg/icon-only-mark.svg",
  wordmark: "brand-assets/svg/wordmark-ps-ai.svg",
  monochromeWhite: "brand-assets/svg/monochrome-white-horizontal.svg",
  monochromeDark: "brand-assets/svg/monochrome-dark-horizontal.svg",
  favicon: "brand-assets/svg/favicon.svg",
};

const MODE_PATHS: Record<ProprietarySystemsLogoMode, Record<ProprietarySystemsLogoIntent, string>> = {
  light: {
    header: "brand-assets/svg/primary-horizontal-lockup.svg",
    compact: "brand-assets/svg/secondary-horizontal-lockup.svg",
    document: "brand-assets/svg/monochrome-dark-horizontal.svg",
    wordmark: "brand-assets/svg/wordmark-ps-ai.svg",
    mark: "brand-assets/svg/icon-only-mark.svg",
    appIcon: "brand-assets/icons/app-icon-light-512.png",
    favicon: "brand-assets/svg/favicon.svg",
    socialAvatar: "brand-assets/icons/app-icon-light-1024.png",
  },
  dark: {
    header: "brand-assets/svg/primary-horizontal-lockup-on-dark.svg",
    compact: "brand-assets/svg/secondary-horizontal-lockup-on-dark.svg",
    document: "brand-assets/svg/monochrome-white-horizontal.svg",
    wordmark: "brand-assets/svg/wordmark-ps-ai-on-dark.svg",
    mark: "brand-assets/svg/icon-only-mark.svg",
    appIcon: "brand-assets/icons/app-icon-dark-512.png",
    favicon: "brand-assets/svg/favicon.svg",
    socialAvatar: "brand-assets/icons/app-icon-dark-1024.png",
  },
  any: {
    header: "brand-assets/svg/primary-horizontal-lockup.svg",
    compact: "brand-assets/svg/secondary-horizontal-lockup.svg",
    document: "brand-assets/svg/monochrome-dark-horizontal.svg",
    wordmark: "brand-assets/svg/wordmark-ps-ai.svg",
    mark: "brand-assets/svg/icon-only-mark.svg",
    appIcon: "brand-assets/icons/app-icon-dark-512.png",
    favicon: "brand-assets/svg/favicon.svg",
    socialAvatar: "brand-assets/icons/app-icon-dark-1024.png",
  },
};

export type ProprietarySystemsLogoProps = Omit<ImgHTMLAttributes<HTMLImageElement>, "src" | "alt"> & {
  variant?: ProprietarySystemsLogoVariant;
  mode?: ProprietarySystemsLogoMode;
  intent?: ProprietarySystemsLogoIntent;
  basePath?: string;
  alt?: string;
};

export function getProprietarySystemsLogoPath(
  variant: ProprietarySystemsLogoVariant = "primary",
  basePath = "/",
) {
  const normalizedBase = basePath.endsWith("/") ? basePath : `${basePath}/`;
  return `${normalizedBase}${LOGO_PATHS[variant]}`;
}

export function getProprietarySystemsLogoPathForMode(
  mode: ProprietarySystemsLogoMode = "light",
  intent: ProprietarySystemsLogoIntent = "header",
  basePath = "/",
) {
  const normalizedBase = basePath.endsWith("/") ? basePath : `${basePath}/`;
  return `${normalizedBase}${MODE_PATHS[mode][intent]}`;
}

export function ProprietarySystemsLogo({
  variant = "primary",
  mode,
  intent = "header",
  basePath = "/",
  alt = "Proprietary Systems",
  ...imgProps
}: ProprietarySystemsLogoProps) {
  const src = mode ? getProprietarySystemsLogoPathForMode(mode, intent, basePath) : getProprietarySystemsLogoPath(variant, basePath);
  return <img src={src} alt={alt} {...imgProps} />;
}

export { LOGO_PATHS as PROPRIETARY_SYSTEMS_LOGO_PATHS };
export { MODE_PATHS as PROPRIETARY_SYSTEMS_LOGO_MODE_PATHS };
