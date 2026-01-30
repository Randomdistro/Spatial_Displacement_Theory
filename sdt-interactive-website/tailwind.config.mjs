/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'sdt-blue': {
          deep: '#1a365d',
          medium: '#2d5a87',
          light: '#4299e1',
        },
        'sdt-gold': {
          primary: '#d69e2e',
          bright: '#f6ad55',
          light: '#fbbf24',
        },
      },
      fontFamily: {
        display: ['Inter', 'system-ui', 'sans-serif'],
        body: ['Source Serif Pro', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
};








