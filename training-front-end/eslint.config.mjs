import globals from "globals";
import astro from "eslint-plugin-astro";
import typescriptEslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import vueParser from "vue-eslint-parser";
import astroParser from "astro-eslint-parser";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all
});

export default [...compat.extends("eslint:recommended", "plugin:@typescript-eslint/recommended"), {

    plugins: {
        "@typescript-eslint": typescriptEslint,
    },
    
    languageOptions: {
        globals: {
            ...globals.browser,
            ...globals.node,
            Fragment: "readonly",
        },

        parser: tsParser,
        ecmaVersion: "latest",
        sourceType: "module",
    },
}, {
    files: ["**/*.js"],

    languageOptions: {
        globals: {
            global: "writeable",
        },
    },
}, ...compat.extends(
    "eslint:recommended",
    "plugin:astro/recommended",
    "plugin:astro/jsx-a11y-strict",
).map(config => ({
    ...config,
    files: ["**/*.astro"],
})), {
    files: ["**/*.astro"],

    languageOptions: {
        parser: astroParser,
        ecmaVersion: 5,
        sourceType: "script",

        parserOptions: {
            parser: "@typescript-eslint/parser",
            extraFileExtensions: [".astro"],
        },
    },

    rules: {
        "astro/jsx-a11y/anchor-is-valid": "off",
    },
}, ...compat.extends("plugin:vue/vue3-recommended", "plugin:vuejs-accessibility/recommended").map(config => ({
    ...config,
    files: ["**/*.vue"],
})), {
    files: ["**/*.vue"],

    languageOptions: {
        parser: vueParser,
        ecmaVersion: "latest",
        sourceType: "module",
    },

    rules: {
        "vuejs-accessibility/label-has-for": ["error", {
            required: {
                some: ["id"],
            },
        }],
        "no-unused-vars": "off",
        "@typescript-eslint/no-unused-vars": "error",
    },
}];