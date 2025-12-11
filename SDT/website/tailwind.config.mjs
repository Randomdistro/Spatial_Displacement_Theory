/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // SDT Brand Colors
        'sdt-primary': {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        'sdt-gold': {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        'sdt-dark': '#0f172a',
        'sdt-light': '#f8fafc',
      },
      fontFamily: {
        'display': ['Inter', 'system-ui', 'sans-serif'],
        'body': ['Source Serif Pro', 'Georgia', 'serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            maxWidth: '75ch',
            color: theme('colors.slate.700'),
            a: {
              color: theme('colors.sdt-primary.600'),
              '&:hover': {
                color: theme('colors.sdt-primary.800'),
              },
            },
            'code::before': { content: '""' },
            'code::after': { content: '""' },
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
