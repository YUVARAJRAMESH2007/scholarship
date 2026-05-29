/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#16171d', // Dark modern background
        surface: '#2c303a',
        primary: '#4caf50',
        secondary: '#2196f3',
        accent: '#c084fc',
        textMain: '#f3f4f6',
        textMuted: '#9ca3af',
      },
      fontFamily: {
        sans: ['"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      }
    },
  },
  plugins: [],
}
