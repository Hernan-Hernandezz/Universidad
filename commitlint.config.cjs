module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Permite un emoji opcional al inicio del subject sin romper la regla
    'subject-case': [0]
  }
}
