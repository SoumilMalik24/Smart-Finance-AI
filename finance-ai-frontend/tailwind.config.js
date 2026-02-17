/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom Financial Dark Theme
        finance: {
          bg: "#0f172a",       // Deep Slate (Main Background)
          panel: "#1e293b",    // Lighter Slate (Sidebar/Cards)
          surface: "#334155",  // Message Bubbles
          text: "#f1f5f9",     // Main Text
          muted: "#94a3b8",    // Secondary Text
          accent: "#10b981",   // Emerald Green (Success/Money)
          accentHover: "#059669",
          border: "#334155",
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'], // For code/numbers
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}