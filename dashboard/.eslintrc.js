module.exports = {
  env: {
    es6: true,
    node: true,
  },
  extends: ['plugin:import/errors', 'plugin:import/warnings'],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  plugins: ['prettier', 'import'],
  rules: {
    'jsx-a11y/anchor-is-valid': 'off',
    'prettier/prettier': 'error',
    'react/prop-types': ['error', { skipUndeclared: true }],
  },
  settings: {
    react: {
      version: "^16.8.2",
    },
    'import/extensions': ['js', 'jsx'],
    'import/resolver': {
      node: {
        extensions: ['.js', '.jsx'],
        moduleDirectory: ['node_modules', 'src', 'js'],
      },
    },
  },
};
