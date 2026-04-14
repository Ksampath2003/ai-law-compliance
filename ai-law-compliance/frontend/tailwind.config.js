/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-body)", "system-ui", "sans-serif"],
        display: ["var(--font-display)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      colors: {
        brand: {
          50:  "#f0f4ff",
          100: "#dce6fd",
          200: "#b9cdfb",
          300: "#8aaff8",
          400: "#5b8cf4",
          500: "#3b6ef0",
          600: "#2250e4",
          700: "#1b3fc7",
          800: "#1a34a1",
          900: "#1b2f7f",
          950: "#131e50",
        },
        slate: {
          950: "#0a0f1e",
        },
      },
    },
  },
  plugins: [],
};
