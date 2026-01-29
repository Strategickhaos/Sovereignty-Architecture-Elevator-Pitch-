module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: [
    'dist',
    '.eslintrc.cjs',
    'recon',
    'src/bot.js',
    'src/bot.ts',
    'src/config.js',
    'src/config.ts',
    'src/event-gateway.js',
    'src/event-gateway.ts',
    'src/discord.ts',
    'src/refinory',
    'src/routes',
  ],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  settings: { react: { version: '18.2' } },
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}
