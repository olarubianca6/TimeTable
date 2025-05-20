import recommendedPrettier from "eslint-plugin-prettier/recommended";
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt()
  .append(recommendedPrettier, {
    rules: {
      "prettier/prettier": [
        "error",
        {
          endOfLine: "auto",
        },
      ],
    },
  })
  .override("nuxt/vue/rules", {
    rules: {
      "vue/html-self-closing": "off",
      "vue/multi-word-component-names": "off",
    },
  });
