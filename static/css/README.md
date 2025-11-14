# Linkup Theme - CSS Documentation

## Color Palette

Based on Linkup's official website design:

### Primary Colors
```css
--color-bg: #F5F3EF           /* Beige/Cream background (from Linkup homepage) */
--color-bg-white: #FFFFFF     /* White cards and containers */
--color-primary: #3D5A45      /* Dark olive green (Linkup's primary button color) */
--color-primary-dark: #2D4435 /* Darker green for hover states */
```

### Text Colors
```css
--color-text: #1A1A1A         /* Primary text (near black) */
--color-text-secondary: #666  /* Secondary text (medium gray) */
--color-text-light: #999      /* Light text (for metadata) */
```

### UI Colors
```css
--color-border: #E0DDD8       /* Subtle borders */
--color-success: #3D5A45      /* Success states (matches primary) */
--color-warning: #D4A574      /* Warning/accent gold */
--color-error: #C54B3D        /* Error states (red) */
```

## Typography

### Font Families
```css
--font-sans: 'Inter'          /* Body text, UI elements */
--font-serif: 'Crimson Pro'   /* Headlines, large text */
```

### Font Weights
- Light: 300
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

### Usage
- **Headings (h1, h2)**: Crimson Pro, 700 weight
- **Subheadings (h3, h4)**: Inter, 600 weight
- **Body text**: Inter, 400 weight
- **UI labels**: Inter, 500 weight

## Spacing System

Based on 8px grid:

```css
--spacing-xs: 0.5rem   /* 8px */
--spacing-sm: 1rem     /* 16px */
--spacing-md: 1.5rem   /* 24px */
--spacing-lg: 2rem     /* 32px */
--spacing-xl: 3rem     /* 48px */
--spacing-2xl: 4rem    /* 64px */
```

## Border Radius

```css
--radius-sm: 6px       /* Small elements */
--radius-md: 12px      /* Cards, buttons */
--radius-lg: 16px      /* Large containers */
--radius-full: 9999px  /* Pills, badges */
```

## Shadows

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)      /* Subtle */
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07)      /* Cards */
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1)     /* Modals */
```

## Component Styles

### Buttons

**Primary Button:**
- Background: `var(--color-primary)`
- Text: White
- Padding: `0.75rem 1.5rem`
- Border radius: `var(--radius-md)`
- Hover: Darker background + slight lift

**Secondary Button:**
- Background: Transparent
- Border: `1px solid var(--color-border)`
- Text: `var(--color-text)`
- Hover: Border changes to primary color

### Cards

- Background: White
- Border: `1px solid var(--color-border)`
- Border radius: `var(--radius-md)`
- Padding: `var(--spacing-lg)`
- Shadow: `var(--shadow-md)`
- Hover: Border color changes to primary

### Form Inputs

- Border: `1px solid var(--color-border)`
- Border radius: `var(--radius-sm)`
- Padding: `0.75rem 1rem`
- Focus: Primary color border + subtle shadow

### Badges

Priority badges with semantic colors:
- **High**: Green background (#D4EDDA)
- **Medium**: Yellow background (#FFF3CD)
- **Low**: Red background (#F8D7DA)

## Layout

### Container
- Max width: 1200px
- Horizontal padding: `var(--spacing-lg)`
- Centered with auto margins

### Grid Systems

**Summary Cards:**
```css
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
gap: var(--spacing-md);
```

**Steps/Features:**
```css
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
gap: var(--spacing-lg);
```

## Responsive Design

### Breakpoints
- Mobile: < 480px
- Tablet: 481px - 768px
- Desktop: > 768px

### Mobile Adaptations
- Single column layouts
- Stacked buttons
- Reduced spacing
- Smaller typography

## Animation

### Transitions
```css
transition: all 0.2s ease;  /* Default */
```

### Hover Effects
- Slight elevation (translateY(-1px))
- Shadow increase
- Color changes

### Loading Spinner
```css
@keyframes spin {
    to { transform: rotate(360deg); }
}
```

## Accessibility

- Minimum contrast ratio: 4.5:1 for normal text
- Focus visible states on all interactive elements
- Semantic HTML structure
- ARIA labels where needed

## Usage Example

```css
.my-component {
    background-color: var(--color-bg-white);
    padding: var(--spacing-lg);
    border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
    box-shadow: var(--shadow-md);
}

.my-component:hover {
    border-color: var(--color-primary);
    transform: translateY(-1px);
}
```

## Customization

To customize the theme, edit the CSS variables in `style.css`:

```css
:root {
    --color-primary: #YourColor;
    --font-serif: 'YourFont';
}
```

All components will automatically update!
