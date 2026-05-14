import pandas as pd
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ ERRO: Configure a variável GOOGLE_API_KEY no arquivo .env")
    exit()

os.environ["GOOGLE_API_KEY"] = api_key

client = genai.Client()

# ===== FUNÇÕES =====
def classificar_complexidade(nome_peca):
    """Classifica a complexidade da peça baseado no nome"""
    palavras_altas = ["Swap", "Motor", "Turbo", "Supercharger", "forjado", "Bloco"]
    palavras_medias = ["Coilovers", "Freios", "Suspensão", "Câmbio", "Intercooler"]
    
    for palavra in palavras_altas:
        if palavra in nome_peca:
            return "Alta"
    
    for palavra in palavras_medias:
        if palavra in nome_peca:
            return "Média"
    
    return "Baixa"


def gerar_analises_ia():
    """Gera análises usando a IA para todas as peças"""
    df_upgrades = pd.read_csv('upgrades.csv')
    resultados = []
    
    print("\n⏳ Gerando análises com IA... isso vai levar alguns minutos...\n")
    
    for indice, linha in df_upgrades.iterrows():
        complexidade = classificar_complexidade(linha['nome_peca'])
        
        try:
            resposta = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Analise a modificação de carro: {linha['nome_peca']}. Explique ganho de performance em números (potência, torque) e como ficaria a tocada do carro em contexto de rua e circuito. Seja técnico e resumido."
            )
            analise = resposta.text
        except Exception as e:
            analise = f"Erro ao gerar análise: {str(e)}"
        
        print(f"✅ Peça: {linha['nome_peca']} | Categoria: {linha['categoria']} | Preço: R$ {linha['preco']} | Complexidade: {complexidade}")
        print(f"Análise (primeiros 150 caracteres): {analise[:150]}...\n")
        print("---")
        
        resultados.append({
            "peca": linha['nome_peca'],
            "categoria": linha['categoria'],
            "preco": linha['preco'],
            "complexidade": complexidade,
            "compatibilidade": linha['compatibilidade'],
            "analise": analise
        })
    
    # Salva em CSV
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv('resultados_upgrades.csv', index=False, encoding='utf-8')
    print("\n✅ Arquivo CSV salvo com sucesso!")
    
    # Gera relatório em HTML
    gerar_relatorio_html(df_resultados)


def gerar_relatorio_html(df_resultados):
    """Gera um relatório bonito em HTML"""
    html_content = "<html><head><meta charset='utf-8'><style>"
    html_content += "body { font-family: Arial; margin: 20px; background: #f5f5f5; }"
    html_content += "h1 { color: #333; text-align: center; }"
    html_content += "h2 { color: #0066cc; margin-top: 30px; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }"
    html_content += "table { width: 100%; border-collapse: collapse; background: white; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }"
    html_content += "th { background: #0066cc; color: white; padding: 12px; text-align: left; }"
    html_content += "td { padding: 10px; border-bottom: 1px solid #ddd; }"
    html_content += "tr:hover { background: #f9f9f9; }"
    html_content += ".analise { background: #f0f7ff; padding: 15px; margin: 10px 0; border-left: 4px solid #0066cc; }"
    html_content += ".info { color: #666; font-size: 0.9em; margin: 5px 0; }"
    html_content += "</style></head><body>"

    html_content += "<h1>🏎️ Relatório de Upgrades de Carro</h1>"

    for _, linha in df_resultados.iterrows():
        html_content += f"<h2>{linha['peca']}</h2>"
        html_content += f"<div class='info'>"
        html_content += f"<strong>Categoria:</strong> {linha['categoria']} | "
        html_content += f"<strong>Complexidade:</strong> {linha['complexidade']} | "
        html_content += f"<strong>Preço:</strong> R$ {linha['preco']} | "
        html_content += f"<strong>Compatibilidade:</strong> {linha['compatibilidade']}"
        html_content += f"</div>"
        html_content += f"<div class='analise'><strong>Análise Técnica:</strong><br>{linha['analise']}</div>"

    html_content += "</body></html>"

    with open("relatorio.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Relatório HTML gerado: relatorio.html")


def ver_analises_anteriores():
    """Mostra análises do CSV anterior"""
    try:
        df_lido = pd.read_csv('resultados_upgrades.csv')
        print(f"\n📖 Total de peças analisadas: {len(df_lido)}\n")
        
        for idx, linha in df_lido.iterrows():
            print(f"{idx + 1}. {linha['peca']}")
            print(f"   Categoria: {linha['categoria']} | Complexidade: {linha['complexidade']} | R$ {linha['preco']}")
            print(f"   Análise: {linha['analise'][:200]}...\n")
    except FileNotFoundError:
        print("\n❌ Nenhuma análise anterior encontrada. Execute a opção 1 primeiro!")


def filtrar_por_categoria():
    """Filtra peças por categoria"""
    try:
        df_lido = pd.read_csv('resultados_upgrades.csv')
        
        print("\n📂 Categorias disponíveis:")
        categorias = df_lido['categoria'].unique()
        for i, cat in enumerate(categorias, 1):
            print(f"   {i}. {cat}")
        
        categoria_busca = input("\nDigite a categoria (ou número): ").strip()
        
        # Se for número, converte
        try:
            cat_idx = int(categoria_busca) - 1
            if 0 <= cat_idx < len(categorias):
                categoria_busca = categorias[cat_idx]
        except:
            pass
        
        resultado = df_lido[df_lido['categoria'] == categoria_busca]
        
        if len(resultado) == 0:
            print(f"\n❌ Nenhuma peça encontrada para '{categoria_busca}'")
        else:
            print(f"\n🔍 Peças de {categoria_busca}:\n")
            print(resultado[['peca', 'complexidade', 'preco']].to_string(index=False))
    except FileNotFoundError:
        print("\n❌ Nenhuma análise anterior encontrada. Execute a opção 1 primeiro!")


def filtrar_por_complexidade():
    """Filtra peças por complexidade"""
    try:
        df_lido = pd.read_csv('resultados_upgrades.csv')
        
        print("\n⚙️ Complexidades disponíveis:")
        complexidades = df_lido['complexidade'].unique()
        for i, comp in enumerate(complexidades, 1):
            print(f"   {i}. {comp}")
        
        complexidade_busca = input("\nDigite a complexidade (ou número): ").strip()
        
        # Se for número, converte
        try:
            comp_idx = int(complexidade_busca) - 1
            if 0 <= comp_idx < len(complexidades):
                complexidade_busca = complexidades[comp_idx]
        except:
            pass
        
        resultado = df_lido[df_lido['complexidade'] == complexidade_busca]
        
        if len(resultado) == 0:
            print(f"\n❌ Nenhuma peça encontrada com complexidade '{complexidade_busca}'")
        else:
            print(f"\n🔍 Peças com complexidade {complexidade_busca}:\n")
            print(resultado[['peca', 'categoria', 'preco']].to_string(index=False))
    except FileNotFoundError:
        print("\n❌ Nenhuma análise anterior encontrada. Execute a opção 1 primeiro!")


def menu_principal():
    """Exibe o menu principal e gerencia as opções"""
    while True:
        print("\n" + "="*60)
        print("🏎️  ASSISTENTE INTELIGENTE DE UPGRADES DE CARRO")
        print("="*60)
        print("\n1 - Analisar todas as peças com IA")
        print("2 - Ver análises anteriores")
        print("3 - Filtrar peças por categoria")
        print("4 - Filtrar peças por complexidade")
        print("5 - Sair")
        print("\n" + "="*60)
        
        opcao = input("\nEscolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            gerar_analises_ia()
        
        elif opcao == "2":
            ver_analises_anteriores()
        
        elif opcao == "3":
            filtrar_por_categoria()
        
        elif opcao == "4":
            filtrar_por_complexidade()
        
        elif opcao == "5":
            print("\n👋 Obrigado por usar o Assistente de Upgrades! Até logo!\n")
            break
        
        else:
            print("\n❌ Opção inválida! Digite um número entre 1 e 5.")


# ===== MAIN =====
if __name__ == "__main__":
    menu_principal()