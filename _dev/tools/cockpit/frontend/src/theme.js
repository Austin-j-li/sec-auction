import { createLightTheme } from '@fluentui/react-components';

// One control blue (brand 80 = --accent #1f4f99). Values mirror the :root tokens in style.css.
const brand = {
  10: '#06101f', 20: '#0b1a35', 30: '#0f244b', 40: '#122f62', 50: '#163b79', 60: '#1a4589',
  70: '#1c4a91', 80: '#1f4f99', 90: '#3663a7', 100: '#4d78b5', 110: '#668dc3', 120: '#82a3d0',
  130: '#9fb9dd', 140: '#bccfe8', 150: '#d8e4f2', 160: '#eef3fa',
};

const mono = '"IBM Plex Mono", SFMono-Regular, Menlo, Consolas, monospace';

export const cockpitTheme = {
  ...createLightTheme(brand),
  fontFamilyBase: '"Cabinet Grotesk", "Helvetica Neue", Arial, sans-serif',
  fontFamilyMonospace: mono,
  fontFamilyNumeric: mono,
  fontSizeBase200: '12px', lineHeightBase200: '16px',
  fontSizeBase300: '13px', lineHeightBase300: '18px',
  fontSizeBase400: '14px', lineHeightBase400: '20px',
  fontSizeBase500: '16px', lineHeightBase500: '22px',
  fontSizeBase600: '20px', lineHeightBase600: '26px',
  fontWeightSemibold: 500, fontWeightBold: 700,
  borderRadiusSmall: '2px', borderRadiusMedium: '3px', borderRadiusLarge: '4px', borderRadiusXLarge: '6px',
  colorNeutralBackground1: '#ffffff', colorNeutralBackground2: '#f4f4f1', colorNeutralBackground3: '#ebebe6',
  colorNeutralForeground1: '#1a1a18', colorNeutralForeground2: '#4a4a45', colorNeutralForeground3: '#66665f',
  colorNeutralForeground4: '#66665f', colorNeutralForegroundDisabled: '#7d7d76',
  colorNeutralStroke1: '#94948c', colorNeutralStroke2: '#c9c9c2', colorNeutralStroke3: '#e3e3de',
  colorNeutralStrokeAccessible: '#66665f', colorNeutralStrokeDisabled: '#c9c9c2',
  colorNeutralBackgroundDisabled: '#f4f4f1',
  colorStrokeFocus2: '#1f4f99',
  // Hover and press follow the same neutral family: hover --tint, press --rule, text stays --ink.
  colorNeutralBackground1Hover: '#ebebe6', colorNeutralBackground1Pressed: '#e3e3de', colorNeutralBackground1Selected: '#ebebe6',
  colorSubtleBackgroundHover: '#ebebe6', colorSubtleBackgroundPressed: '#e3e3de', colorSubtleBackgroundSelected: '#ebebe6',
  colorNeutralForeground1Hover: '#1a1a18', colorNeutralForeground1Pressed: '#1a1a18', colorNeutralForeground1Selected: '#1a1a18',
  colorNeutralForeground2Hover: '#1a1a18', colorNeutralForeground2Pressed: '#1a1a18', colorNeutralForeground2Selected: '#1a1a18',
  colorNeutralForeground2BrandHover: '#1a1a18', colorNeutralForeground2BrandPressed: '#1a1a18', colorNeutralForeground2BrandSelected: '#1a1a18',
  colorNeutralForeground3Hover: '#4a4a45', colorNeutralForeground3Pressed: '#4a4a45',
  colorNeutralStroke1Hover: '#66665f', colorNeutralStroke1Pressed: '#4a4a45', colorNeutralStroke1Selected: '#66665f',
};
