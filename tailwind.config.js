/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");
module.exports = {
  content: [
    "client/templates/client/*.html",
    "core/templates/core/*.html",
    "core/templates/core/partials/*.html",
    "dashboard/templates/dashboard/*.html",
    "lead/templates/lead/*.html",
    "team/templates/team/*.html",
    "userprofile/templates/userprofile/*.html",
  ],
  theme: {
    theme: {
      extend: {
        colors: {
          ...colors,
        },
      },
    },
  },
  plugins: [],
};
