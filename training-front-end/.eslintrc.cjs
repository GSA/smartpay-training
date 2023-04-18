module.exports = {
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },

  extends: [
    // add more generic rulesets here, such as:
    // 'eslint:recommended',
    //'plugin:vue/vue3-recommended',
    //'plugin:astro/recommended'
    // 'plugin:vue/recommended' // Use this if you are using Vue.js 2.x.
  ],
  rules: {
    // override/add rules settings here, such as:
    // 'vue/no-unused-vars': 'error'
  },
  overrides: [
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