/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#00bcd4',
          600: '#00acc1',
        },
        navy: {
          700: '#1e3a5f',
          800: '#0f172a',
          900: '#020617',
        },
        cyan: {
          400: '#26c6da',
          500: '#00bcd4',
        },
        emerald: {
          400: '#34d399',
          500: '#10b981',
        },
      },
    },
  },
  plugins: [],
}