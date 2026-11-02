# autoUP

> Assistente de linha de comando que analisa peças de upgrade de carro com **Pandas** e **Gemini 2.5 Flash** e gera um relatório em HTML.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_API-8E75B2?logo=google&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-yellow)

<!--
  TODO: adicionar um print do menu no terminal e do relatorio.html.
  Salvar em docs/ e descomentar:

  ![Menu no terminal](docs/menu.png)
  ![Relatório HTML](docs/relatorio.png)
-->

## O que faz

O autoUP lê um catálogo de peças em `upgrades.csv` e, para cada uma:

1. **Classifica a complexidade** de instalação (Alta, Média ou Baixa) a partir de palavras-chave no nome da peça (por exemplo, "Turbo" e "Swap" caem em Alta).
2. **Pede ao Gemini 2.5 Flash** um resumo técnico do ganho de desempenho (potência e torque) e de como o carro fica na rua e no circuito.
3. **Salva os resultados** em `resultados_upgrades.csv` e gera o `relatorio.html`.

Depois, o menu permite rever as análises e filtrar peças por categoria ou complexidade.

> **Aviso:** as análises são geradas por um modelo de linguagem. Os números de potência e torque são **estimativas**, não medições, e não devem orientar uma compra ou instalação sem validação.

## Como usar

### 1. Instalar

```bash
git clone https://github.com/Raphael-Ribeiro-Pereira/autoUP.git
cd autoUP
python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install pandas google-genai python-dotenv
```

### 2. Configurar a chave da API

Crie uma chave do Gemini no Google AI Studio e coloque-a em um arquivo `.env` na raiz do projeto:

```
GOOGLE_API_KEY=sua_chave_aqui
```

O `.env` não deve ser versionado e já está no `.gitignore` do projeto.

### 3. Executar

```bash
python main.py
```

### Menu

| Opção | Ação |
|---|---|
| 1 | Analisar todas as peças com IA (gera o CSV e o HTML) |
| 2 | Ver análises anteriores (lê `resultados_upgrades.csv`) |
| 3 | Filtrar por categoria |
| 4 | Filtrar por complexidade |
| 5 | Sair |

As opções 2 a 4 dependem de ter rodado a opção 1 pelo menos uma vez.

## Formato do `upgrades.csv`

| Coluna | Descrição |
|---|---|
| `nome_peca` | Nome da peça (usado também na classificação de complexidade) |
| `categoria` | Tipo da peça, por exemplo Motor ou Suspensão |
| `preco` | Preço em reais |
| `dificuldade_instalacao` | Dificuldade informada no catálogo |
| `compatibilidade` | Modelos ou plataformas compatíveis |

## Estrutura

```
autoUP/
├── main.py                 # menu, chamadas à IA, filtros e geração do relatório
├── upgrades.csv            # catálogo de peças (entrada)
├── resultados_upgrades.csv # análises geradas (criado ao rodar; fora do git)
├── relatorio.html          # relatório visual (criado ao rodar; fora do git)
├── LICENSE
└── README.md
```

## Decisões técnicas

- **Falha isolada por peça.** Se a API falhar em uma peça, o erro é registrado no resultado e o loop continua nas demais.
- **Chave fora do código.** A `GOOGLE_API_KEY` é lida do ambiente com `python-dotenv`, e o programa avisa e encerra se ela não existir.
- **Classificação por regras.** A complexidade usa listas de palavras-chave, simples de auditar e sem custo de API.
- **Relatório sem dependências.** O HTML é gerado direto do DataFrame, sem framework.

## Limitações e próximos passos

- [ ] Usar a coluna `dificuldade_instalacao` do CSV (hoje a complexidade vem só das palavras-chave).
- [ ] Guardar respostas em cache para não repetir chamadas à API a cada execução.
- [ ] Escapar o texto da IA antes de inserir no HTML.
- [ ] Adicionar `requirements.txt` e `.env.example`.
- [ ] Testes para `classificar_complexidade`.
- [ ] Validar as estimativas contra fontes reais (dinamômetro, fabricantes).

## O que este projeto demonstra

Leitura e escrita de CSV com Pandas · integração com API de IA generativa · variáveis de ambiente · tratamento de erros com `try/except` · menu interativo em CLI · geração de relatório HTML.

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).

## Autor

**Raphael Ribeiro Pereira** · [LinkedIn](https://linkedin.com/in/raphael-ribeiro-pereira) · [GitHub](https://github.com/Raphael-Ribeiro-Pereira)
