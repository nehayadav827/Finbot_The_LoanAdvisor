/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        body: ['"DM Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        navy: {
          950: '#040d1a',
          900: '#071428',
          800: '#0d2044',
          700: '#142d5e',
          600: '#1a3a78',
        },
        gold: {
          400: '#f5c842',
          500: '#e8b820',
          600: '#c9990a',
        },
        emerald: {
          400: '#34d399',
          500: '#10b981',
        },
        crimson: {
          400: '#f87171',
          500: '#ef4444',
        }
      },
      animation: {
        'slide-in': 'slideIn 0.35s cubic-bezier(0.16,1,0.3,1)',
        'fade-up': 'fadeUp 0.4s ease-out',
        'pulse-dot': 'pulseDot 1.4s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        slideIn: {
          '0%': { opacity: 0, transform: 'translateY(12px) scale(0.97)' },
          '100%': { opacity: 1, transform: 'translateY(0) scale(1)' },
        },
        fadeUp: {
          '0%': { opacity: 0, transform: 'translateY(20px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        pulseDot: {
          '0%, 80%, 100%': { transform: 'scale(0)', opacity: 0.5 },
          '40%': { transform: 'scale(1)', opacity: 1 },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      }
    },
  },
  plugins: [],
}
