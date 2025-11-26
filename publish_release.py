import sys
import os
from datetime import datetime
import pytz
from github import Github, Auth

def publicar_no_pages(mensagem_release):
    token = os.getenv("GITHUB_TOKEN")
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")
    
    # MSG do .env é fallback
    # Se a mensagem foi passada pelo .env, ela sobrescreve a do argumento
    mensagem_env  = os.getenv("MSG")
    if not mensagem_release:
        mensagem_release = mensagem_env
        
    file_path = "CHANGELOG.md"

    # Validação do token
    if not token:
        print("Erro: Variável GITHUB_TOKEN não encontrada.")
        return

    # Validação do repositório
    if not repo_owner or not repo_name:
        print("Erro: REPO_OWNER e REPO_NAME precisam ser informados.")
        return

    # monta o nome completo do repositório
    repo_full = f"{repo_owner}/{repo_name}"

    try:
        print(f"Conectando à API do GitHub no repositório {repo_full}...")
        
        # Autenticação
        # Instância permite chamadas à API
        g = Github(auth=Auth.Token(token))
        repo = g.get_repo(repo_full)

        # 2. Tenta buscar o arquivo existente
        # Precisamos do 'sha' (hash) do arquivo para ter permissão de editá-lo
        try:
            contents = repo.get_contents(file_path)
            conteudo_atual = contents.decoded_content.decode("utf-8")
            sha_arquivo = contents.sha
            print(f"Arquivo {file_path} encontrado. Atualizando...")
        except:
            # Se o arquivo não existir, cria um novo
            conteudo_atual = ""
            sha_arquivo = None # Sem SHA pois é criação
            print(f"Arquivo {file_path} não encontrado. Criando novo...")

        # 3. Formata o novo conteúdo (Markdown)
        # Adiciona a data e a mensagem no TOPO do conteúdo existente
        tz = pytz.timezone("America/Sao_Paulo")
        data_hoje = datetime.now(tz).strftime("%d/%m/%Y %H:%M")
        nova_entrada = f"## Release (Atual) - {data_hoje}\n{mensagem_release}\n\n---\n\n"

        titulo_historico = "# Histórico de Versões"

        # reorganizar o conteúdo antigo
        if titulo_historico in conteudo_atual:
            before, after = conteudo_atual.split(titulo_historico, 1)

            antigo_atual = before.strip()

            if antigo_atual:
                antigo_atual = antigo_atual.replace("Release (Atual)", "Release")
                antigo_atual = antigo_atual.strip() + "\n"

                # Coloca o antigo atual como o primeiro do histórico
                novo_historico = antigo_atual + after.strip()
            else:
                novo_historico = after.strip()

        else:
            antigo_atual = conteudo_atual.strip()
            if antigo_atual:
                antigo_atual = antigo_atual.replace("Release (Atual)", "Release")
                novo_historico = antigo_atual
            else:
                novo_historico = ""

        novo_conteudo_completo = (
            nova_entrada
            + f"{titulo_historico}\n\n"
            + novo_historico.strip() + "\n"
        )

        # 4. Realiza o Commit via API
        commit_msg = f"docs: atualiza release notes via script - {data_hoje}"

        if sha_arquivo:
            # Update (requer o SHA do arquivo original)
            repo.update_file(file_path, commit_msg, novo_conteudo_completo, sha_arquivo)
        else:
            # Create
            repo.create_file(file_path, commit_msg, novo_conteudo_completo)

        print("Sucesso! O GitHub Pages deve atualizar em instantes.")

    except Exception as e:
        print(f"Falha ao publicar no GitHub: {e}")

if __name__ == "__main__":
    msg_cli = sys.argv[1] if len(sys.argv) > 1 else None
    publicar_no_pages(msg_cli)