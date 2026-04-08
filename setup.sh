#!/usr/bin/env bash
# =============================================================
#  setup.sh — Claude Certification Course
#  Funciona en macOS y Linux. Configura el entorno Python,
#  instala dependencias y registra el kernel de Jupyter para
#  VSCode.
# =============================================================

set -e

# ── Colores ──────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK] $1${NC}"; }
warn() { echo -e "${YELLOW}[AVISO] $1${NC}"; }
err()  { echo -e "${RED}[ERROR] $1${NC}"; exit 1; }

# ── Detectar SO ──────────────────────────────────────────────
OS="$(uname -s)"
case "$OS" in
  Darwin) PLATFORM="macOS" ;;
  Linux)  PLATFORM="Linux" ;;
  *)      err "Sistema operativo no soportado: $OS" ;;
esac
echo -e "\nPlataforma detectada: ${GREEN}${PLATFORM}${NC}\n"

# ── Directorio del proyecto ──────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── 1. Verificar Python 3.10+ ────────────────────────────────
echo "Verificando Python..."
if command -v python3 &>/dev/null; then
  PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
  PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
  PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
  if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
    ok "Python $PY_VERSION encontrado"
  else
    warn "Python $PY_VERSION encontrado, se recomienda 3.10+"
  fi
else
  err "Python 3 no encontrado. Instálalo desde https://www.python.org/downloads/"
fi

# ── 2. Instalar dependencias del sistema ─────────────────────
echo ""
echo "Instalando dependencias del sistema..."

if [ "$PLATFORM" = "macOS" ]; then
  if ! command -v brew &>/dev/null; then
    warn "Homebrew no encontrado. Instalando..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  # python-tk necesario para algunos paquetes en macOS
  brew install python-tk 2>/dev/null || true
  ok "Dependencias macOS OK"

elif [ "$PLATFORM" = "Linux" ]; then
  if command -v apt &>/dev/null; then
    sudo apt update -qq
    sudo apt install -y python3-venv python3-pip build-essential curl git 2>/dev/null
    ok "Dependencias Linux (apt) OK"
  elif command -v dnf &>/dev/null; then
    sudo dnf install -y python3-virtualenv python3-pip gcc git curl 2>/dev/null
    ok "Dependencias Linux (dnf) OK"
  else
    warn "Gestor de paquetes no reconocido. Asegúrate de tener python3-venv instalado."
  fi
fi

# ── 3. Crear entorno virtual ─────────────────────────────────
echo ""
echo "Configurando entorno virtual (.venv)..."
if [ -d ".venv" ]; then
  warn ".venv ya existe, reutilizando..."
else
  python3 -m venv .venv
  ok "Entorno virtual creado en .venv/"
fi

# Activar venv
source .venv/bin/activate

# ── 4. Actualizar pip e instalar paquetes ────────────────────
echo ""
echo "Instalando paquetes Python..."
pip install --upgrade pip setuptools wheel -q
pip install -r requirements.txt -q
ok "Paquetes instalados"

# ── 5. Registrar kernel de Jupyter para VSCode ───────────────
echo ""
echo "Registrando kernel de Jupyter..."
python -m ipykernel install --user \
  --name=claude-course \
  --display-name "Python (Claude Course)"
ok "Kernel 'Python (Claude Course)' registrado"

# ── 6. Crear .env si no existe ───────────────────────────────
echo ""
if [ ! -f ".env" ]; then
  cp .env.example .env
  warn ".env creado desde .env.example — agrega tu ANTHROPIC_API_KEY"
else
  ok ".env ya existe"
fi

# ── 7. Extensiones de VSCode recomendadas ────────────────────
echo ""
echo "Instalando extensiones de VSCode recomendadas..."
if command -v code &>/dev/null; then
  code --install-extension ms-python.python          --force 2>/dev/null
  code --install-extension ms-python.vscode-pylance  --force 2>/dev/null
  code --install-extension ms-toolsai.jupyter         --force 2>/dev/null
  code --install-extension ms-toolsai.jupyter-keymap  --force 2>/dev/null
  ok "Extensiones de VSCode instaladas"
else
  warn "VSCode CLI ('code') no encontrado. Instala las extensiones manualmente:"
  echo "   - ms-python.python"
  echo "   - ms-toolsai.jupyter"
fi

# ── Resumen ──────────────────────────────────────────────────
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Configuracion completada con exito        ${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "  Próximos pasos:"
echo "  1. Edita .env y agrega tu ANTHROPIC_API_KEY"
echo "  2. Abre VSCode en este directorio"
echo "  3. En cada notebook selecciona el kernel:"
echo "     'Python (Claude Course)'"
echo "  4. ¡Ejecuta las celdas con Shift+Enter!"
echo ""
