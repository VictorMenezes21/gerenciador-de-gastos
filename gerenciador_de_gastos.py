import locale, json
import pandas as pd
import matplotlib.pyplot as plt

locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")

# cria função de exibir as chaves do dicionário de forma organizada
def exibir_empresas(dicionario): 
    for i, empresa in enumerate(dicionario, 1):
        print(f'{i}. {empresa}')

# cria função que pega as chaves do dicionário e coloca em uma lista para ser chamado pelos índices
def obter_empresa_por_indice(escolha, dicionario): 
    empresas = list(dicionario)
    if 1 <= escolha <= len(empresas):
        return empresas[escolha -1]
    return None

# cria função que carrega os dados do .json
def carregar_dados():
    try:
        with open('gerenciador_de_gastos.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo) # load Lẽ o arquivo e transforma de volta em dicionário
    except FileNotFoundError:
        return {} # Se o arquivo não existir ainda, retorna um dicionário

# cria função de salvar dados no Json
def salvar_dados(dados): 
    with open('gerenciador_de_gastos.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False) # indent=4 deixa bonito e ensure=ascii=False deixa ler acentuação

# cria função de formatar valor
def formatar_valor(valor_digitado):
    # Se tiver vírgula no valor, considero que é Brasileiro
    if ',' in valor_digitado:
        valor_formatado = valor_digitado.replace('.', '').replace(',', '.')
    else:
        valor_formatado = valor_digitado
    return float(valor_formatado)

def gerar_grafico_barra(resumo_de_gastos):
    # -> Gráfico de Barras <-
    # O Gráfico - # kind = tipo do gráfico (bar,line,pie)
    # Se fosse barras - colorbar = preenchimento das barras, edgecolor = cor da borda
    resumo_de_gastos.plot(kind='bar', color='orange', edgecolor='black')
    plt.title('Total de Gastos por Empresa') # título principal no topo do gráfico
    plt.tight_layout() # ajusta as margens automaticamente para que o título ou os nomes não fiquem cortados para fora da janela
    plt.savefig('grafico_barras.png') # Salvando arquivo na pasta
    plt.close()

def gerar_grafico_linha(resumo_de_gastos):
    # -> Gráfico de linhas <-
    # Se fosse linhas - marker = coloca um marcador em cada empresa, linewidth define a grossura da linha
    resumo_de_gastos.plot(kind='line', marker='o', markeredgecolor='black', markerfacecolor='orange', color='red', linewidth=2)
    plt.title('Tendência de Gastos') # título principal no topo do gráfico
    plt.grid(True, linestyle='--', alpha=0.6) # Adiciona uma grade no fundo
    plt.tight_layout() # ajusta as margens automaticamente para que o título ou os nomes não fiquem cortados para fora da janela
    plt.savefig('grafico_linhas.png')
    plt.close()

def gerar_grafico_pizza(resumo_de_gastos):     
    # -> Gráfico de Pizza <-
    # Se fosse pizza - 
    resumo_de_gastos.plot(
        kind='pie',
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        colors=['orange', 'skyblue', 'lightgreen', 'tomato', 'violet', 'gold'],
        wedgeprops={'width': 0.5}
        )
    plt.title('Resumo de Gastos por Empresa') # título principal no topo do gráfico
    plt.ylabel('') # Define o texto no Eixo Y (linha vertical)
    plt.tight_layout() # ajusta as margens automaticamente para que o título ou os nomes não fiquem cortados para fora da janela
    plt.savefig('grafico_pizza.png')
    plt.close()


# tenta carregar o conteúdo json que foi salvo anteriormente
gastos_empresa = carregar_dados()

while True:

    print(f'\n{'=' * 25} Gerenciador de Gastos {'=' * 25}')
    try:
        opcao = int(input('[1] Empresas\n[2] Gastos\n[3] Ver Extrato\n[4] Relatórios\n[5] Sair\n\nOpção: ')) # Verifica a opção do usuário

        if opcao == 1:
            opcao = int(input('\n[1] Adicionar empresa\n[2] Remover empresa\n\nOpção: '))

            if opcao == 1:
                print(f'\n{'=' * 25} Adicionar Empresa {'=' * 25}\n')
                nome_empresa = input('Digite o nome da empresa: ') # Recebe o nome da empresa

                if nome_empresa not in gastos_empresa: # Confere se o nome digitado já existe no dicionario
                    gastos_empresa[nome_empresa] = [] # Adiciona o nome da empresa como chave no dicionario gasto_empresa
                    salvar_dados(gastos_empresa)
                    print('\nEmpresa Adicionada!')
                else:
                    print('\nEmpresa já existe!')

            elif opcao == 2:                

                if gastos_empresa:            
                    print(f'\n{'=' * 28} Remover Empresa {'=' * 28}\n')
                    exibir_empresas(gastos_empresa)  

                    try:
                        escolha = int(input('Escolha a empresa a ser removida: ')) # Recebe o número correspondente a empresa

                        # Chama a função
                        empresa_escolhida = obter_empresa_por_indice(escolha, gastos_empresa)

                        if empresa_escolhida:
                            del gastos_empresa[empresa_escolhida]
                            print(f'\nA empresa {empresa_escolhida} foi removida.\n')
                            salvar_dados(gastos_empresa)                            

                        else:
                            print('\nEscolha um número válido.')                        

                    except ValueError:
                        print('\nPor favor, digite um número.\n')
                else:
                    print('\nNão há empresas para remover!')

        elif opcao == 2:

            if gastos_empresa:
                print(f'\n{'=' * 25} Adicionar Gastos {'=' * 25}\n')
                exibir_empresas(gastos_empresa)
                                
                try:                    
                    escolha = int(input('Escolha a empresa: ')) # Recebe o número correspondente a empresa
                    empresa_escolhida = obter_empresa_por_indice(escolha, gastos_empresa)
                    
                    valor_gasto = input(f'Digite o valor gasto pela {empresa_escolhida} (Ex: 1250,00 ou 1250.00): R$ ') # Recebe um gasto

                    try:
                        valor_convertido = formatar_valor(valor_gasto)
                        gastos_empresa[empresa_escolhida].append(valor_convertido)
                        salvar_dados(gastos_empresa)

                        print(f'\nGasto de {locale.currency(valor_convertido)} adicionado na empresa {empresa_escolhida}\n')

                    except Exception:
                        print('\nValor inválido.\n')

                except ValueError:
                    print('\nOpção inválida\n')
            else:
                print('Não há empresas cadastradas')

        elif opcao == 3:
            print(f'\n{'=' * 30} Ver extrato {'=' * 30}\n')

            if not gastos_empresa:
                print('Não há empresas cadastradas!')
            else:                
                try:
                    valor_total = 0

                    exibir_empresas(gastos_empresa)
                    escolha = int(input('\nEscolha a empresa: ')) # Recebe o número correspondente a empresa
                    empresa_escolhida = obter_empresa_por_indice(escolha, gastos_empresa)

                    if empresa_escolhida:

                        print(f'\nEmpresa: {empresa_escolhida}\nGastos: ', end='')

                        if gastos_empresa[empresa_escolhida]: 

                            for gastos in gastos_empresa[empresa_escolhida]: # pega cada gasto e imprime na tela
                                print(f'- {locale.currency(gastos)}') # imprime o valor convertido em real
                                valor_total += gastos # soma cada gasto e guarda na variavel

                            print(f'Valor total: {locale.currency(valor_total)}\n')
                        else:
                            print(f'Não há gastos da empresa {empresa_escolhida}')

                    else:
                        print('\nEscolha um número válido.\n')
                
                except ValueError:
                    print('\nValor inválido\n')

        elif opcao == 4:
            if not gastos_empresa:
                print('\nNão há dados para gerar relatórios!')
                continue

            # Criando a tabela (Data frame)
            dados_para_tabela = []
            for empresa, valores in gastos_empresa.items():
                for v in valores:
                    dados_para_tabela.append({'Empresa': empresa, "Gastos": v})

            # pandas pega as linhas e monta estrutura de colunas
            df = pd.DataFrame(dados_para_tabela) 
            pd.options.display.float_format = '{:,.2f}'.format # configurando saída do pandas deixando trilhões legíveis

            # Somando os valores e filtrando
            resumo_de_gastos = df.groupby('Empresa')['Gastos'].sum()
            
            print(f'\n{'=' * 25} Relatórios Visuais {'=' * 25}')
            opcao = int(input('\n[1] Gráfico de Barras\n[2] Gráfico de Linhas\n[3] Gráfico de Pizza/Rosca\n[4] Todos\n\nOpção: '))
            
            # chama função que gera gráficos
            if opcao == 1:
                gerar_grafico_barra(resumo_de_gastos)
            elif opcao == 2:
                gerar_grafico_linha(resumo_de_gastos)
            elif opcao == 3:
                gerar_grafico_pizza(resumo_de_gastos)
            elif opcao == 4:
                gerar_grafico_barra(resumo_de_gastos)
                gerar_grafico_linha(resumo_de_gastos)
                gerar_grafico_pizza(resumo_de_gastos)
            else:
                print('Opção inválida')                 
            
        elif opcao == 5:
            print('\nSaindo..\n')
            break

        else:
            print('\nOpção inválida\n')


    except ValueError:
        print('\nOpção inválida\n')