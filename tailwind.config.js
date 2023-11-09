/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      boxShadow: {
        'lg': '0 0px 30px rgba(0, 0, 0, 0.1)',
      }
      }
  },
  plugins: [],
}

