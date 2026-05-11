/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    fontFamily: {
      sans: ["'Pretendard'", "'Inter'", "system-ui", "sans-serif"],
    },
    extend: {
      colors: {
        // Neon Gradient Colors (로고 맞춤)
        neon: {
          cyan: "#00D9FF",
          blue: "#0099FF",
          purple: "#A855F7",
          magenta: "#EC4899",
          green: "#00FF88",
        },
        // Light Mode
        light: {
          bg: "#F9FAFB",
          text: "#10142A",
          border: "#E5E7EB",
        },
        // Dark Mode
        dark: {
          bg: "#0A0F2C",
          bg2: "#10142A",
          text: "#E6EFFF",
          border: "#1F2B4D",
        },
      },
      borderRadius: {
        xl: "12px",
        "2xl": "16px",
      },
      boxShadow: {
        soft: "0 4px 16px rgba(0, 0, 0, 0.08)",
        "soft-dark": "0 4px 16px rgba(0, 217, 255, 0.08)",
        glow: "0 0 20px rgba(168, 85, 247, 0.3)",
        "glow-cyan": "0 0 30px rgba(0, 217, 255, 0.4)",
      },
      backgroundImage: {
        "gradient-neon": "linear-gradient(135deg, #00D9FF 0%, #0099FF 33%, #A855F7 66%, #EC4899 100%)",
        "gradient-neon-light": "linear-gradient(135deg, #00D9FF 0%, #A855F7 50%, #EC4899 100%)",
        "gradient-light-bg": "linear-gradient(135deg, #F9FAFB 0%, #F0F9FF 100%)",
        "gradient-dark-bg": "linear-gradient(135deg, #0A0F2C 0%, #10142A 100%)",
      },
      animation: {
        "gradient-flow": "gradient-flow 6s ease infinite",
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "float": "float 3s ease-in-out infinite",
      },
      keyframes: {
        "gradient-flow": {
          "0%, 100%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
        },
        "pulse-glow": {
          "0%, 100%": { opacity: "1", boxShadow: "0 0 20px rgba(168, 85, 247, 0.3)" },
          "50%": { opacity: "0.8", boxShadow: "0 0 40px rgba(0, 217, 255, 0.5)" },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        },
      },
    },
  },
  plugins: [],
};
