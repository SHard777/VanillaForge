/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        app: '#0A0F1C',          // Obsidian
        panel: '#151B2B',        // Glass Surface
        borderRing: '#2A3241',   // Slate Ring
        textPrimary: '#FFFFFF',  // Pure White
        textSecondary: '#94A3B8',// Muted Gray
        accentUp: '#10B981',     // Neon Emerald (Call/Up)
        accentDown: '#EF4444',   // Crimson Red (Put/Down)
        brand: '#6366F1',        // Indigo Glow
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Fira Code', 'JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
