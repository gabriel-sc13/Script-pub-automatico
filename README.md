![Descrição da imagem](./img/tbx.png)

# Release Notes Dinâmico

Automatização de Release Notes com GitHub Pages + Docker + Python

Este projeto permite publicar automaticamente novas *Release Notes* diretamente no **GitHub Pages**, lendo dados via **CLI** ou via arquivo **.env**, e montando o arquivo `CHANGELOG.md` de forma totalmente dinâmica.

Ideal para automações, pipelines CI/CD e repositórios que precisam manter histórico atualizado de releases.

---

## 📘 Funcionalidades

- 🔄 Atualização automática do `CHANGELOG.md`
- 📄 Publicação instantânea no GitHub Pages
- 🐳 Execução via Docker (CLI ou .env)
- 🔐 Suporte total a variáveis de ambiente
- 🚫 `.env` protegido por padrão no `.gitignore`

---

## 📂 Estrutura do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `publish_release.py` | Script principal responsável por gerar, atualizar e publicar o `CHANGELOG.md` no repositório via API do GitHub. |
| `Dockerfile` | Define a imagem Docker do projeto, instalando dependências e preparando o ambiente para execução automática. |
| `docker-compose.yml` | Arquivo que permite rodar o projeto via Docker Compose, definindo variáveis e comandos de execução. |
| `index.html` | O arquivo index.html funciona como a página inicial do GitHub Pages para este projeto. |
| `.env.example` | Modelo de arquivo `.env` contendo todas as variáveis necessárias (`GITHUB_TOKEN`, `REPO_OWNER`, `REPO_NAME`, `MSG`). |
| `.gitignore` | Define arquivos e pastas que não devem ser enviados ao repositório, incluindo o `.env`. |
| `CHANGELOG.md` *(opcional, criado pelo script)* | Arquivo gerado/atualizado automaticamente contendo o histórico das releases. |

---

## 🌐 Como habilitar o GitHub Pages

1. Abra seu repositório no GitHub
2. Vá em **Settings → Pages**
3. Em **Build and Deployment**, configure:
   - **Source:** Deploy from branch
   - **Branch:** `main` (ou outra que você use)
4. Clique em **Save**

O GitHub exibirá a URL da página após alguns segundos.

---

## Como gerar seu Token (PAT)

Acesse:
GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)

Gere um novo token com permissão repo

**Copie o token (ele só aparece uma vez!)**

---

## 🔧 Configurando o `.env`

Crie o arquivo `.env` baseado no modelo:

```bash
cp .env.example .env
```

---

## Preencha os valores:

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx
REPO_OWNER=seu-usuario-ou-organizacao
REPO_NAME=nome-do-repositorio
MSG=Mensagem padrão da release
```

---

## 🔐 Segurança

O arquivo .env não será commitado, pois já está listado no .gitignore.

---

## 🐳 Uso com Docker
✔️ Modo .env (automático)

A mensagem será lida automaticamente da variável MSG do .env:

```bash
docker compose run --rm release-notes-dinamico
```

✔️ Modo CLI (passando a mensagem no comando)

```bash
docker compose run --rm release-notes-dinamico "Minha mensagem de release via CLI"
```

---

## 📝 Exemplo de saída do CHANGELOG.md

### Release (Atual) - 26/11/2025 10:24
Minha nova release automática!

---

### Histórico de Versões
#### Release - 25/11/2025 09:12
Texto da release anterior

---

## 🧠 Como o script funciona

    1. Lê variáveis de ambiente (via .env ou CLI)

    2. Autentica na API do GitHub usando PyGithub

    3. Localiza o arquivo CHANGELOG.md no repositório

    4. Adiciona uma nova seção de "Release (Atual)"

    5. Move a release anterior para o histórico

    6. Atualiza ou cria o arquivo diretamente no repositório

    7. O GitHub Pages detecta a mudança e exibe automaticamente
