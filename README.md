# F1 Race Strategy Simulator

Um simulador interativo de estratégias de corrida de Fórmula 1 em tempo real, permitindo comparar diferentes abordagens de pit stops, degradação de pneus e consumo de combustível.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![React](https://img.shields.io/badge/React-18+-61dafb)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791)

## Features

### Core Features (MVP)
1º - Motor de simulação de corrida com física realista
2º - Cálculo de degradação de pneus (5 compostos)
3º - Simulação de consumo de combustível
4º - Comparação de múltiplas estratégias
5º - Visualização em tempo real
6º - Cálculo de undercut/overcut

## Stack Técnica de Planejamento

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Banco de Dados:** PostgreSQL 15+
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **WebSockets:** FastAPI WebSocket
- **Validação:** Pydantic v2

### Frontend
- **Framework:** React 18 + Vite
- **Linguagem:** JavaScript (ES6+)
- **Estilização:** Tailwind CSS
- **Gráficos:** Recharts
- **Estado:** React Hooks + Context API
- **HTTP Client:** Axios

### DevOps (Futuro)
- **Containerização:** Docker + Docker Compose
- **Variáveis de Ambiente:** python-dotenv
- **Testes:** Pytest (backend), Vitest (frontend)

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/devkayky83/f1-strategy-simulator.git
cd f1-strategy-simulator
```

### 2. Backend Setup

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Executar migrations
alembic upgrade head

# Popular banco de dados com dados iniciais
python -m app.scripts.seed_database

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env

# Iniciar servidor de desenvolvimento
npm run dev
```

### 4. Usando Docker (Alternativa)

```bash
# Na raiz do projeto
docker-compose up -d

# Acessar aplicação
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Documentação da API

Após iniciar o backend, acesse:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc


## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Roadmap Atual

- [x] Setup inicial do projeto
- [ ] Motor de simulação básico
- [ ] API REST completa
- [ ] Interface React funcional
- [ ] WebSockets para tempo real
- [ ] Integração com API Ergast
- [ ] Sistema de autenticação
- [ ] Modo multiplayer/competitivo

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

Criado com ❤️ e paixão por Dev Kayky Júnio

## Agradecimentos

- [Ergast API](http://ergast.com/mrd/) - Dados históricos de F1
- [OpenF1](https://openf1.org/) - Dados ao vivo de F1
- Comunidade F1 por toda inspiração

---

**⚠️ Disclaimer:** Este é um projeto educacional e não possui afiliação oficial com a Fórmula 1, FIA ou equipes.

**Em desenvolvimento para mostrar paixão por F1 e habilidades em programação!**