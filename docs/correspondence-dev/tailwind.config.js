/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],

  theme: {
    extend: {
      colors:{
        'matt-gray': '#36363a',
        'stone-750' : '#22201e',
      }
    },
  },
  plugins: [],
}
