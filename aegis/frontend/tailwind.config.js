export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Inter", "ui-sans-serif", "system-ui"],
        mono: ["JetBrains Mono", "SFMono-Regular", "ui-monospace", "monospace"]
      },
      boxShadow: {
        glass: "0 24px 80px rgba(3, 12, 30, 0.42)"
      }
    }
  },
  plugins: []
};

