#!/usr/bin/env bash
set -euo pipefail

BOLD='\033[1m'
DIM='\033[2m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

spell()      { echo -e "${MAGENTA}✦${RESET}  $1"; }
incantation(){ echo -e "${CYAN}◈${RESET}  $1"; }
warning()    { echo -e "${YELLOW}⚠${RESET}  $1"; }
success()    { echo -e "${GREEN}★${RESET}  $1"; }
fail()       { echo -e "${RED}✗${RESET}  $1"; exit 1; }

echo -e "\n${BOLD}${MAGENTA}   ⬟  Pottery Assistant — Ritual de Invocação  ⬟${RESET}\n"

spell "Consultando os pergaminhos antigos..."
command -v docker &>/dev/null || fail "O cajado Docker não foi encontrado. Instale-o antes de continuar."

if [ ! -f .env ]; then
    warning "Nenhum grimório de segredos (.env) encontrado."
    warning "Copie .env.example para .env e preencha sua chave mágica (GOOGLE_API_KEY)."
    echo
    fail "O ritual não pode prosseguir sem os segredos."
fi

incantation "Preparando a argila primordial (construindo imagens)..."
docker compose build --quiet

spell "Invocando os espíritos do barro..."
docker compose up -d

incantation "Aquecendo o forno sagrado..."
MAX_ATTEMPTS=30
attempt=0
until curl -sf http://localhost:8000/health > /dev/null 2>&1; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge "$MAX_ATTEMPTS" ]; then
        echo
        fail "O feitiço falhou após $MAX_ATTEMPTS tentativas. Verifique os logs: docker compose logs"
    fi
    printf "${DIM}.${RESET}"
    sleep 2
done
echo

success "O assistente está desperto e pronto para guiar seus alunos!"
echo
echo -e "  ${DIM}Portal mágico:${RESET}    ${BOLD}http://localhost:8000${RESET}"
echo -e "  ${DIM}Grimório (docs):${RESET}  ${BOLD}http://localhost:8000/docs${RESET}"
echo -e "  ${DIM}Encerrar ritual:${RESET}  ${BOLD}docker compose down${RESET}"
echo
