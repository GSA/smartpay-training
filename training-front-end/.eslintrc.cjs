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
      extends: ['eslint:recommended', 'plugin:astro/recommended']
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