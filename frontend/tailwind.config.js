/** @type {import('tailwindcss').Config} */
const config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "var(--background)",
                foreground: "var(--foreground)",
                primary: "var(--brand-primary)",
                secondary: "var(--brand-secondary)",
                accent: {
                    primary: "var(--accent-primary)",
                    secondary: "var(--accent-secondary)",
                    light: "var(--accent-light)",
                },
            },
        },
    },
    plugins: [],
};
module.exports = config;