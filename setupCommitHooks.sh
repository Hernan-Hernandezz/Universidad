#!/usr/bin/env bash
set -e

echo "🔧 Configurando commitlint + husky + gitmoji para este repositorio..."

# 1. Instalar dependencias
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky

# 2. Crear configuración de commitlint compatible con gitmoji
#    (acepta emoji opcional después del tipo, ej: "feat: ✨ agregar login")
cat > commitlint.config.cjs << 'EOF'
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Permite un emoji opcional al inicio del subject sin romper la regla
    'subject-case': [0]
  }
}
EOF

# 3. Inicializar husky
npx husky init

# 4. Hook commit-msg -> corre commitlint
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
chmod +x .husky/commit-msg

# 5. Instalar gitmoji-cli si no está global
if ! command -v gitmoji &> /dev/null; then
  echo "📦 Instalando gitmoji-cli globalmente..."
  npm install -g gitmoji-cli
fi

# 6. Hook prepare-commit-msg -> sugiere emoji (gitmoji)
gitmoji -i

echo ""
echo "✅ Listo. Cada miembro del equipo que clone el repo debe correr:"
echo "   npm install && bash setup-commit-hooks.sh"
echo ""
echo "Uso diario:"
echo "   git add ."
echo "   gitmoji -c        # commit guiado con emoji"
echo "   git commit -m \"feat: agregar validación\"   # o commit manual (se valida solo)"