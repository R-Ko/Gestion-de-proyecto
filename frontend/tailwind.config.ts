import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          900: '#2c106c',
          700: '#4f2fc8',
          500: '#14b8a6',
          400: '#22c55e',
        },
      },
    },
  },
  plugins: [],
};

export default config;
