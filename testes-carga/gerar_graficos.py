import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

def gerar_graficos():
    # Configurações
    pasta_arquivos = "."  # Pasta atual
    lista_dados = []

    # 1. Encontrar todos os arquivos .csv
    arquivos = glob.glob(os.path.join(pasta_arquivos, "*-*-*.csv"))
    
    if not arquivos:
        print("❌ Nenhum arquivo CSV encontrado! Verifique se rodou os testes e salvou na pasta certa.")
        return

    print(f"📂 Encontrados {len(arquivos)} arquivos CSV. Processando...")

    for arquivo in arquivos:
        try:
            # 2. Extrair informações do nome do arquivo
            nome_arquivo = os.path.basename(arquivo)
            nome_limpo = nome_arquivo.replace(".csv", "")
            
            # Espera formato: python-rest-50.csv
            partes = nome_limpo.split("-")
            if len(partes) < 3:
                continue 
                
            linguagem = partes[0].capitalize()  # Python ou Java
            tecnologia = partes[1].upper()      # REST, GRAPH, SOAP
            carga = int(partes[2])              # 50, 250, 350
            
            sistema = f"{linguagem} {tecnologia}"

            # 3. Ler o CSV
            df = pd.read_csv(arquivo)

            # Pega a linha de resumo (Aggregated ou última)
            if "Name" in df.columns and "Aggregated" in df["Name"].values:
                linha_resumo = df[df["Name"] == "Aggregated"].iloc[0]
            else:
                linha_resumo = df.iloc[-1]

            # 4. Guardar métricas
            lista_dados.append({
                "Sistema": sistema,
                "Linguagem": linguagem,
                "Tecnologia": tecnologia,
                "Carga (Usuários)": carga,
                "RPS": linha_resumo["Requests/s"],
                "Tempo Médio (ms)": linha_resumo["Average Response Time"],
                "Falhas/s": linha_resumo["Failures/s"]
            })
            
        except Exception as e:
            print(f"⚠️ Pulei o arquivo {arquivo} (Erro: {e})")

    # Cria o DataFrame final
    df_final = pd.DataFrame(lista_dados)
    
    if df_final.empty:
        print("❌ Não consegui extrair dados. Verifique os nomes dos arquivos CSV.")
        return

    # Ordena
    df_final.sort_values(by=["Carga (Usuários)", "Linguagem", "Tecnologia"], inplace=True)

    # Configuração Global
    sns.set_theme(style="whitegrid")
    
    # ==========================================
    # GRÁFICO 1: THROUGHPUT (RPS) - CORES NOVAS
    # ==========================================
    plt.figure(figsize=(14, 7))
    grafico1 = sns.barplot(
        data=df_final,
        x="Carga (Usuários)",
        y="RPS",
        hue="Sistema",
        palette="tab10"  # <--- MUDADO PARA TAB10 (Cores fortes e distintas)
    )
    
    plt.title("Comparativo de Desempenho: Requisições por Segundo (RPS)", fontsize=16, fontweight='bold')
    plt.ylabel("Requisições / Segundo (Quanto maior, melhor)", fontsize=12)
    plt.xlabel("Carga (Número de Usuários Simultâneos)", fontsize=12)
    plt.legend(title="Tecnologia", bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("Grafico_1_Desempenho_RPS.png", dpi=300)
    print("✅ Gráfico 1 gerado: Grafico_1_Desempenho_RPS.png")

    # ==========================================
    # GRÁFICO 2: LATÊNCIA (Tempo) - CORES NOVAS
    # ==========================================
    plt.figure(figsize=(14, 7))
    grafico2 = sns.barplot(
        data=df_final,
        x="Carga (Usuários)",
        y="Tempo Médio (ms)",
        hue="Sistema",
        palette="tab10"  # <--- MANTIDO TAB10 PARA CONSISTÊNCIA
    )
    
    plt.title("Comparativo de Latência: Tempo Médio de Resposta", fontsize=16, fontweight='bold')
    plt.ylabel("Tempo em Milissegundos (Quanto menor, melhor)", fontsize=12)
    plt.xlabel("Carga (Número de Usuários Simultâneos)", fontsize=12)
    plt.legend(title="Tecnologia", bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("Grafico_2_Latencia_Tempo.png", dpi=300)
    print("✅ Gráfico 2 gerado: Grafico_2_Latencia_Tempo.png")

if __name__ == "__main__":
    gerar_graficos()