/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./reportes/templates/**/*.html",
    "./templates/**/*.html",
    "./reportes/static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        brand: '#FE2020',
      },
    },
  },
  plugins: [],
}