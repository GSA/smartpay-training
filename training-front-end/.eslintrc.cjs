module.exports = {
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  "env": {
    "browser": true,
    "es6": true
  },
  
  extends: [
    // add more generic rulesets here, such as:
    'eslint:recommended',
  ],
  rules: {
    // override/add rules settings here, such as:
    // 'vue/no-unused-vars': 'error'
  },
  overrides: [
    {
      files: ["*.spec.js"],
      "globals": {
        "global": true
      },
    },
    {
      files: ['*.astro'],
      plugins: ["astro"],
      parser: 'astro-eslint-parser',
      extends: ['plugin:astro/recommended']
    },
    {
      files: ['*.vue'],
      parser: 'vue-eslint-parser',
      extends: ['plugin:vue/vue3-recommended'],
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module'
      },
    }
  ],
}