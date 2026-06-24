---
name: Groww Pulse AI
colors:
  surface: '#0b1326'
  surface-dim: '#0c1324'
  surface-bright: '#33394c'
  surface-container-lowest: '#070d1f'
  surface-container-low: '#151b2d'
  surface-container: '#171f33'
  surface-container-high: '#23293c'
  surface-container-highest: '#2e3447'
  on-surface: '#dce1fb'
  on-surface-variant: '#bccbb9'
  inverse-surface: '#dce1fb'
  inverse-on-surface: '#2a3043'
  outline: '#869585'
  outline-variant: '#3d4a3d'
  surface-tint: '#4ae176'
  primary: '#4be277'
  on-primary: '#003915'
  primary-container: '#22c55e'
  on-primary-container: '#004b1e'
  inverse-primary: '#006e2f'
  secondary: '#4cd7f6'
  on-secondary: '#003640'
  secondary-container: '#03b5d4'
  on-secondary-container: '#00424e'
  tertiary: '#d1bdff'
  on-tertiary: '#37265d'
  tertiary-container: '#b5a2e2'
  on-tertiary-container: '#47366e'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6aff90'
  primary-fixed-dim: '#4ae176'
  on-primary-fixed: '#002109'
  on-primary-fixed-variant: '#005322'
  secondary-fixed: '#acedff'
  secondary-fixed-dim: '#4cd7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#e9ddff'
  tertiary-fixed-dim: '#d0bcfe'
  on-tertiary-fixed: '#210f47'
  on-tertiary-fixed-variant: '#4e3d75'
  background: '#0c1324'
  on-background: '#dce1fb'
  surface-variant: '#2e3447'
  glass-bg: rgba(30, 41, 59, 0.4)
  glass-modal: rgba(51, 65, 85, 0.8)
  error-accent: '#ffb4ab'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
  gutter: 24px
  margin-x: 32px
  container-max: 1440px
---

## Brand & Style
Groww Pulse is a high-performance fintech dashboard designed for data-intensive AI insights. The brand personality is **technical, precise, and futuristic**, targeting sophisticated investors and product managers. 

The design style is a hybrid of **Modern Corporate and Glassmorphism**. It utilizes deep obsidian backgrounds contrasted with neon-accented primary colors to create a "command center" aesthetic. Key visual identifiers include subtle backdrop blurs, luminous borders, and a rhythmic "AI shimmer" animation that suggests real-time processing and intelligence. The emotional response should be one of confidence, speed, and analytical depth.

## Colors
The palette is rooted in a **deep navy/black foundation** (#020617) to maximize contrast for data visualization. 

- **Primary (Neon Green):** Used for critical growth metrics, active navigation states, and primary call-to-actions. It carries a subtle glow effect to signify vitality.
- **Secondary (Cyber Blue):** Reserved for auxiliary data points, specific clusters, and interactive secondary elements.
- **Tertiary (Soft Lavender):** Used for AI-driven "Action Ideas" and insights, providing a distinct visual bucket for machine-generated content.
- **Semantic Colors:** Soft reds (#ffb4ab) are used sparingly for negative sentiment or urgent warnings, often paired with low-opacity backgrounds to prevent visual fatigue.

## Typography
The system employs a dual-font strategy. **Geist** is used for all headlines, labels, and technical data to reinforce the "developer-centric" and precise nature of the platform. **Inter** is used for body copy and long-form reviews to ensure maximum readability and a slightly softer humanist touch in narrative sections.

Large display sizes utilize tight letter spacing and heavy weights to create a strong information hierarchy. Data points should prioritize the `mono-data` style for alignment and legibility.

## Layout & Spacing
The layout follows a **Fixed Grid with Side Navigation** model. The main content area is constrained to a max-width of 1440px to prevent excessive line lengths on ultra-wide monitors.

- **Desktop:** A permanent 64px (or 16rem/256px) sidebar provides high-level navigation. Sections are separated by large vertical gaps (64px) to allow the "glass" cards room to breathe.
- **Mobile:** The sidebar collapses into a hamburger menu. The horizontal `gutter` reduces to 16px. 
- **Rhythm:** An 8px base unit drives all internal padding and spacing. KPI rows utilize a 3-column grid on desktop, collapsing to 1-column on mobile.

## Elevation & Depth
Depth is created through **Glassmorphism and Tonal Layering** rather than traditional shadows.

1.  **Level 0 (Background):** Deepest black (#020617).
2.  **Level 1 (Navigation/Sidebar):** Semi-transparent surfaces with high backdrop-blur (24px-32px) and a subtle 1px white/10% border to define edges against the background.
3.  **Level 2 (Cards/Containers):** `glass` class using `rgba(30, 41, 59, 0.4)` with a linear-gradient border (top-left to bottom-right) that simulates a light source hitting the edge.
4.  **Level 3 (Modals/Overlays):** Higher opacity glass (#334155 at 80%) to pull focus forward.

**Neon Glow:** Interactive elements like the "Run Pipeline" button use a soft green outer glow (`box-shadow: 0 0 15px rgba(75, 226, 119, 0.3)`) to indicate high-priority status.

## Shapes
The shape language is **Structured and Modern**. 
- **Standard Cards/KPIs:** Use 0.75rem (rounded-xl) for a premium, approachable feel.
- **Buttons & Inputs:** Use 0.5rem (rounded-lg) to maintain a tighter, more functional appearance.
- **Badges/Tags:** Use "Full" rounding (Pill-shaped) to distinguish them from interactive buttons.
- **Sidebar Indicators:** Use sharp vertical bars for active states to emphasize the "grid-based" technical nature of the UI.

## Components

### Buttons
- **Primary:** Neon green background, dark green text. Features a hover scale-down effect (95%) and a persistent neon-glow-primary shadow.
- **Ghost/Secondary:** Surface-container background with a low-contrast border. Text and icons inherit the primary or secondary brand colors.

### Cards
- **KPI Cards:** Glass-base with vertical stacks of labels and large display values. Include a footer area for "trend" micro-copy.
- **Cluster Cards:** Feature a colored left-border (4px) corresponding to the sentiment (Error, Secondary, or Primary) and an "AI Shimmer" background animation.

### Data Table
- **Header:** Darker, high-contrast surface-container-highest with uppercase labels.
- **Rows:** Transparent backgrounds with `white/5%` separators. Hover states use a subtle `white/3%` fill.
- **Text:** Use `truncate` for long review strings to maintain table vertical rhythm.

### Inputs
- **Search:** Background in `surface-container-lowest` with an `outline-variant` border. On focus, the border transitions to the primary green and the entire container scales slightly (105%).

### Indicators
- **Sentiment Circle:** SVG-based circular progress indicators using the primary green and surface-container-highest for the track.