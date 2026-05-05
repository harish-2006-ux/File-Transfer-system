/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#020408',
        surface: '#060d18',
        card: 'rgba(8,20,40,0.9)',
        cyan: '#00c8ff',
        green: '#00ff88',
        violet: '#9b5cff',
        gold: '#ffcc44',
        muted: '#4a6a80'
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'monospace']
      }
    },
  },
  plugins: [],
}
