"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt semente do desafio
3. Salva localmente em prompts/bug_to_user_story_v1.yml

DICAS DE IMPLEMENTAÇÃO:

- O pull é feito pelo cliente do LangSmith:

      from langsmith import Client
      client = Client()
      prompt = client.pull_prompt(
          "leonanluppi/bug_to_user_story_v1",
          dangerously_pull_public_prompt=True,
      )

- O parâmetro `dangerously_pull_public_prompt=True` é obrigatório sempre que o
  identificador tem dono explícito ("owner/nome"). O LangSmith bloqueia esse pull
  por padrão porque um prompt do Hub é um objeto LangChain serializado, que pode
  vir de terceiros. Aqui o prompt é o do desafio, então o risco é conhecido.

- O retorno é um ChatPromptTemplate. Para extrair o conteúdo das mensagens,
  use a serialização nativa do LangChain (`prompt.messages`, e o atributo
  `.prompt.template` de cada mensagem).

- Use `save_yaml` de utils.py para gravar o resultado no arquivo .yml.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header


def pull_prompts_from_langsmith():
    client = Client()
    prompt = client.pull_prompt(
        "leonanluppi/bug_to_user_story_v1",
        dangerously_pull_public_prompt=True,
    )

    system_prompt = prompt.messages[0]
    user_prompt = prompt.messages[1]

    save_yaml(
        {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt.prompt.template,
                "user_prompt": user_prompt.prompt.template,
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"],
            }
        },
        "prompts/bug_to_user_story_test.yml",
    )
    print_section_header("Prompt pulled and saved to prompts/bug_to_user_story_test.yml")


def main():
    """Função principal"""
    print_section_header("Pulling prompts from LangSmith")
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
