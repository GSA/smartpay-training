module.exports = {
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  "env": {
    "browser": true,
    "es6": true
  },
  extends: ['eslint:recommended'],

  overrides: [
    {
      files: ["*.js"],
      "globals": {
        "global": "writeable" // vitest adds global to tests
      },
    },
    {
      files: ['*.astro'],
      plugins: ["astro"],
      parser: 'astro-eslint-parser',
      extends: ['eslint:recommended', 'plugin:astro/recommended', 'plugin:astro/jsx-a11y-strict'],
      rules: {
        'astro/jsx-a11y/anchor-is-valid': 'off'
      }
    },
    {
      files: ['*.vue'],
      parser: 'vue-eslint-parser',
      extends: ['plugin:vue/vue3-recommended', 'plugin:vuejs-accessibility/recommended'],
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module'
      },
      rules: {
        // default rule requires nested label/inputs 
        // which uswds does not do. id is sufficient
        "vuejs-accessibility/label-has-for": ["error", {
          "required": {
            "some": ["id"]
          }
        }]
      }
    }
  ],
}