/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        paper: 'rgb(var(--paper) / <alpha-value>)',
        surface: 'rgb(var(--surface) / <alpha-value>)',
        'surface-raised': 'rgb(var(--surface-raised) / <alpha-value>)',
        sidebar: 'rgb(var(--sidebar) / <alpha-value>)',
        ink: {
          DEFAULT: 'rgb(var(--ink) / <alpha-value>)',
          soft: 'rgb(var(--ink-soft) / <alpha-value>)',
          faint: 'rgb(var(--ink-faint) / <alpha-value>)',
        },
        line: 'rgb(var(--line) / <alpha-value>)',

        // Primary brand — Toasted Walnut
        walnut: {
          50: 'rgb(var(--walnut-50) / <alpha-value>)',
          100: 'rgb(var(--walnut-100) / <alpha-value>)',
          400: 'rgb(var(--walnut-400) / <alpha-value>)',
          500: 'rgb(var(--walnut-500) / <alpha-value>)',
          600: 'rgb(var(--walnut-600) / <alpha-value>)',
          700: 'rgb(var(--walnut-700) / <alpha-value>)',
        },
        // AI / sparkle accent — Warm Caramel
        caramel: {
          50: 'rgb(var(--caramel-50) / <alpha-value>)',
          100: 'rgb(var(--caramel-100) / <alpha-value>)',
          500: 'rgb(var(--caramel-500) / <alpha-value>)',
          600: 'rgb(var(--caramel-600) / <alpha-value>)',
        },
        // Action items / active — Raw Tobacco
        tobacco: {
          50: 'rgb(var(--tobacco-50) / <alpha-value>)',
          100: 'rgb(var(--tobacco-100) / <alpha-value>)',
          500: 'rgb(var(--tobacco-500) / <alpha-value>)',
          600: 'rgb(var(--tobacco-600) / <alpha-value>)',
        },
        // Decisions / done — Olive Cedar
        olive: {
          50: 'rgb(var(--olive-50) / <alpha-value>)',
          100: 'rgb(var(--olive-100) / <alpha-value>)',
          500: 'rgb(var(--olive-500) / <alpha-value>)',
          600: 'rgb(var(--olive-600) / <alpha-value>)',
        },
        // Warnings / follow-ups — Burnt Ochre
        ochre: {
          50: 'rgb(var(--ochre-50) / <alpha-value>)',
          100: 'rgb(var(--ochre-100) / <alpha-value>)',
          500: 'rgb(var(--ochre-500) / <alpha-value>)',
          600: 'rgb(var(--ochre-600) / <alpha-value>)',
        },
        // Urgent deadlines — Oxblood
        oxblood: {
          50: 'rgb(var(--oxblood-50) / <alpha-value>)',
          100: 'rgb(var(--oxblood-100) / <alpha-value>)',
          500: 'rgb(var(--oxblood-500) / <alpha-value>)',
          600: 'rgb(var(--oxblood-600) / <alpha-value>)',
        },
      },
      fontFamily: {
        display: ['"Sora"', 'sans-serif'],
        body: ['"Inter"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        soft: '0 1px 2px rgb(0 0 0 / 0.05), 0 1px 1px rgb(0 0 0 / 0.04)',
        raised: '0 4px 16px rgb(0 0 0 / 0.10), 0 1px 2px rgb(0 0 0 / 0.08)',
      },
      borderRadius: {
        md: '10px',
        lg: '14px',
      },
    },
  },
  plugins: [],
}
