from calculo_geo import obter_geolocalizacao
import csv

#vetores iniciais com os dados padrão
culturas = ["milho", "soja"]  #culturas
figura_geometrica = "retangulo"  #forma geométrica
espacamento = 0.75  #espaçamento fixo entre fileiras (metros)
quantidade_por_metro = 500  #quantidade de insumo por metro quadrado (mL)

#dicionários para os produtos
produto_milho = {
    "nome": "fosfato",
    "quantidade_por_hectare": 100  #quantidade por hectare(kg)
}
produto_soja = {
    "nome": "fosfato",
    "quantidade_por_hectare": 60  #quantidade por hectare(kg)
}

#função para verificar se os dados foram inseridos antes de exibir
def dados_inseridos():
    global largura_terreno, comprimento_terreno
    #verifica se os dados essenciais foram inseridos (largura e comprimento)
    return largura_terreno is not None and comprimento_terreno is not None

#função para exibir os dados e realizar cálculos com alinhamento e gerar um arquivo CSV separado por ";"
def saida_dados():
    global culturas, figura_geometrica, largura_terreno, comprimento_terreno, quantidade_por_metro, latitude, longitude, espacamento, area_total, numero_de_fileiras, volume_por_fileira, volume_total

    #verifica se os dados foram inseridos
    if not dados_inseridos():
        print("Erro: Nenhum dado foi inserido ainda. Por favor, insira os dados primeiro.")
        return
    
    #calcula a área total, número de fileiras e volume, para garantir que essas variáveis estejam sempre definidas
    area_total = largura_terreno * comprimento_terreno
    
    if espacamento > 0:
        numero_de_fileiras = largura_terreno / espacamento
        volume_por_fileira = (quantidade_por_metro / 1000) * comprimento_terreno  #convertendo mL para litros
        volume_total = numero_de_fileiras * volume_por_fileira
    else:
        numero_de_fileiras = None
        volume_por_fileira = None
        volume_total = None

    #nome do arquivo CSV
    csv_filename = 'saida_dados.csv'

    #lista para armazenar os dados que serão gravados no CSV
    csv_data = []
    
    while True:  #laço para permitir a volta ao menu anterior
        print("\nSaída de Dados:")
        print("1. Exibir dados")
        print("2. Gerar CSV")
        print("3. Voltar ao menu anterior")  #opção de voltar
        
        #verifica se o input é válido
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            #tamanho fixo para a coluna de labels (35 caracteres para labels) e valores alinhados
            print(f"{'Culturas:':<35}{culturas}")
            print(f"{'Figura geométrica:':<35}{figura_geometrica}")
            print(f"{'Largura do terreno:':<35}{largura_terreno:.2f} m")
            print(f"{'Comprimento do terreno:':<35}{comprimento_terreno:.2f} m")
            print(f"{'Espaçamento entre fileiras:':<35}{espacamento:.2f} m") 
            print(f"{'Quantidade por metro quadrado:':<35}{quantidade_por_metro:.2f} mL")
            print(f"{'Área total:':<35}{area_total:.2f} m²")
            
            if espacamento > 0:
                print(f"{'Numero de fileiras:':<35}{int(numero_de_fileiras)}")
                print(f"{'Volume por fileira:':<35}{volume_por_fileira:.2f} litros")
                print(f"{'Volume total necessario:':<35}{volume_total:.2f} litros")
            else:
                print(f"{'Erro:':<35}Espaçamento entre fileiras inválido. Não é possível calcular o número de fileiras.")
            
            #exibe a geolocalização, se disponível
            if latitude and longitude:
                print(f"{'Latitude:':<35}{latitude}")
                print(f"{'Longitude:':<35}{longitude}")
            else:
                print(f"{'Geolocalização:':<35}Não disponível.")

        elif opcao == "2":
            #preenche a lista de dados para o CSV
            csv_data.append(['culturas', str(culturas)])
            csv_data.append(['figura geometrica', figura_geometrica])
            csv_data.append(['largura do terreno (m)', f"{largura_terreno:.2f}"])
            csv_data.append(['comprimento do terreno (m)', f"{comprimento_terreno:.2f}"])
            csv_data.append(['espacamento entre fileiras (m)', f"{espacamento:.2f}"])
            csv_data.append(['quantidade por metro quadrado (mL)', f"{quantidade_por_metro:.2f}"])
            csv_data.append(['area total (m2)', f"{area_total:.2f}"])

            if espacamento > 0:
                csv_data.append(['numero de fileiras', str(int(numero_de_fileiras))])
                csv_data.append(['volume por fileira (litros)', f"{volume_por_fileira:.2f}"])
                csv_data.append(['volume total necessario (litros)', f"{volume_total:.2f}"])
            else:
                csv_data.append(['Erro', 'Espaçamento entre fileiras inválido.'])

            if latitude and longitude:
                csv_data.append(['latitude', latitude])
                csv_data.append(['longitude', longitude])
            else:
                csv_data.append(['geolocalizacao', 'nao disponivel'])

            #gera o arquivo CSV com ";" como separador
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')  # Usa o delimitador ";"
                writer.writerows(csv_data)

            print(f"Arquivo CSV '{csv_filename}' gerado com sucesso!")

        elif opcao == "3":
            return  #volta ao menu principal
        else:
            #se o usuário não digitar nada ou digitar uma opção inválida
            print("Opção inválida! Tente novamente.")

#função para entrada de dados sem permitir inputs vazios e com tratamento de erros
def entrada_dados():
    global culturas, figura_geometrica, largura_terreno, comprimento_terreno, quantidade_por_metro, latitude, longitude
    
    print("\nEntrada de Dados:")

    #verificação para largura do terreno: não pode ser 0 ou negativa
    while True:
        try:
            largura_terreno_input = input("Digite a largura do terreno em metros: ")
            largura_terreno = float(largura_terreno_input)  # Tenta converter para float
            if largura_terreno <= 0:
                print("A largura deve ser maior que 0. Digite novamente.")
                continue  #solicita nova entrada se a largura for inválida
            break  #sai do loop se a conversão for bem-sucedida e o valor for válido
        except ValueError:
            print("Dado inválido, digite novamente.")  #exibe a mensagem de erro e pede nova entrada

    #verificação para comprimento do terreno: não pode ser 0, negativa e deve ser maior que a largura
    while True:
        try:
            comprimento_terreno_input = input("Digite o comprimento do terreno em metros: ")
            comprimento_terreno = float(comprimento_terreno_input)  # Tenta converter para float
            if comprimento_terreno <= 0:
                print("O comprimento deve ser maior que 0. Digite novamente.")
                continue  #solicita uma nova entrada se o comprimento for inválido
            if comprimento_terreno <= largura_terreno:
                print("O comprimento deve ser maior que a largura (formato escolhido: retângulo). Digite novamente.")
                continue  #solicita uma nova entrada se o comprimento for menor ou igual à largura
            break  #sai do loop se a conversão for bem-sucedida e o valor for válido
        except ValueError:
            print("Dado inválido, digite novamente.")  #exibe a mensagem de erro e pede nova entrada

    #coleta os dados de endereço sem permitir inputs vazios
    while True:
        rua = input("Digite o nome da rua: ")
        if rua:
            break
        else:
            print("Dado inválido, digite novamente.")  #se o usuário deixar em branco, pede novamente

    while True:
        numero = input("Digite o número: ")
        if numero:
            break
        else:
            print("Dado inválido, digite novamente.")  #se o usuário deixar em branco, pede novamente

    while True:
        cidade = input("Digite a cidade: ")
        if cidade:
            break
        else:
            print("Dado inválido, digite novamente.")  #se o usuário deixar em branco, pede novamente

    while True:
        estado = input("Digite o estado (abreviado): ")
        if estado:
            break
        else:
            print("Dado inválido, digite novamente.")  #se o usuário deixar em branco, pede novamente

    #obtém as coordenadas geográficas com base no endereço
    latitude, longitude = obter_geolocalizacao(rua, numero, cidade, estado)

    #verifica se a geolocalização foi bem-sucedida
    if latitude is None or longitude is None:
        print("Não foi possível encontrar a geolocalização. Verifique o endereço.")
    else:
        print(f"Geolocalização obtida com sucesso! Latitude: {latitude}, Longitude: {longitude}")

    print("Dados inseridos com sucesso!")

#função para atualizar os dados
def atualizar_dados():
    global culturas, figura_geometrica, largura_terreno, comprimento_terreno, quantidade_por_metro, latitude, longitude
    while True:  #laço para continuar exibindo o menu até que uma opção válida seja inserida
        print("\nAtualizar Dados:")
        
        #exibe as opções de dados que podem ser atualizados
        print("1. Culturas")
        print("2. Figura geométrica")
        print("3. Largura do terreno")
        print("4. Comprimento do terreno")
        print("5. Quantidade por metro quadrado")
        print("6. Atualizar endereço e geolocalização")  #nova opção para atualizar geolocalização
        print("7. Voltar ao menu anterior")
        
        #o usuário escolhe qual dado deseja atualizar
        escolha = input("Escolha qual dado deseja atualizar (1-7): ")
        
        #verifica se o input foi inserido e chama a função correspondente
        if escolha == "1":
            novas_culturas = input("Digite as novas culturas (separadas por vírgula): ")
            if novas_culturas:
                culturas = novas_culturas.split(",")
        elif escolha == "2":
            nova_figura_geometrica = input("Digite a nova figura geométrica da área plantada: ")
            if nova_figura_geometrica:
                figura_geometrica = nova_figura_geometrica
        elif escolha == "3":
            nova_largura = input("Digite a nova largura do terreno em metros: ")
            if nova_largura:
                largura_terreno = float(nova_largura)
        elif escolha == "4":
            novo_comprimento = input("Digite o novo comprimento do terreno em metros: ")
            if novo_comprimento:
                comprimento_terreno = float(novo_comprimento)
        elif escolha == "5":
            nova_quantidade = input("Digite a nova quantidade de insumo por metro quadrado em mL: ")
            if nova_quantidade:
                quantidade_por_metro = float(nova_quantidade)
        elif escolha == "6":
            #atualiza o endereço e obtém a nova geolocalização
            nova_rua = input("Digite o novo nome da rua: ")
            novo_numero = input("Digite o novo número: ")
            nova_cidade = input("Digite a nova cidade: ")
            novo_estado = input("Digite o novo estado: ")
            if nova_rua and novo_numero and nova_cidade and novo_estado:
                latitude, longitude = obter_geolocalizacao(nova_rua, novo_numero, nova_cidade, novo_estado)
                if latitude is None or longitude is None:
                    print("Não foi possível encontrar a geolocalização. Verifique o endereço.")
                else:
                    print(f"Nova geolocalização obtida! Latitude: {latitude}, Longitude: {longitude}")
        elif escolha == "7":
            return  #volta ao menu principal
        else:
            print("Escolha inválida! Tente novamente.")
        
        print("Dados atualizados com sucesso!")

#função para deletar os dados
def deletar_dados():
    global culturas, figura_geometrica, largura_terreno, comprimento_terreno, espacamento, quantidade_por_metro
    print("\nDeletar Dados:")
    
    #exibe as opções de dados que podem ser deletados
    print("1. Culturas")
    print("2. Figura geométrica")
    print("3. Largura do terreno")
    print("4. Comprimento do terreno")
    print("5. Espaçamento entre fileiras")
    print("6. Quantidade por metro quadrado")
    print("7. Voltar ao menu anterior")  #opção para voltar sem deletar

    #o usuário escolhe qual dado deseja deletar
    escolha = input("Escolha qual dado deseja deletar (1-7): ")
    
    #verifica e deleta o dado escolhido (zerando ou limpando a variável)
    if escolha == "1":
        if culturas:
            culturas = []
            print("Culturas deletadas com sucesso!")
            print("Esse dado foi deletado. Vá para a opção 3 no menu principal para atualizar os dados.")
        else:
            print("Nenhum dado para deletar em Culturas.")
    elif escolha == "2":
        if figura_geometrica:
            figura_geometrica = ""
            print("Figura geométrica deletada com sucesso!")
            print("Esse dado foi deletado. Vá para a opção 3 no menu principal para atualizar os dados.")
        else:
            print("Nenhum dado para deletar em Figura geométrica.")
    elif escolha == "3":
        if largura_terreno is not None and largura_terreno > 0:
            largura_terreno = 0
            print("Largura do terreno deletada com sucesso!")
            print("Esse dado foi deletado. Vá para a opção 3 no menu principal para atualizar os dados.")
        else:
            print("Nenhum dado para deletar em Largura do terreno.")
    elif escolha == "4":
        if comprimento_terreno is not None and comprimento_terreno > 0:
            comprimento_terreno = 0
            print("Comprimento do terreno deletado com sucesso!")
            print("Esse dado foi deletado. Vá para a opção 3 no menu principal para atualizar os dados.")
        else:
            print("Nenhum dado para deletar em Comprimento do terreno.")
    elif escolha == "5":
        if espacamento is not None and espacamento > 0:
            espacamento = 0.75  #ou redefinir para o valor padrão
            print("Espaçamento deletado com sucesso!")
            print("Esse dado foi deletado. Vá para a opção 3 no menu principal para atualizar os dados.")
        else:
            print("Nenhum dado para deletar em Espaçamento.")
    elif escolha == "6":
        if quantidade_por_metro is not None and quantidade_por_metro > 0:
            quantidade_por_metro = 0
            print("Quantidade por metro quadrado deletada com sucesso!")
            print("Esse dado foi deletado. Vá para a opção 3 no menu principal para atualizar os dados.")
        else:
            print("Nenhum dado para deletar em Quantidade por metro quadrado.")
    elif escolha == "7":
        return  #volta ao menu principal sem deletar nada
    else:
        print("Escolha inválida! Tente novamente.")


#função principal com o menu de opções
def menu():
    while True:
        print("\n--- Menu de Opções ---")
        print("1. Entrada de Dados")
        print("2. Saída de Dados")
        print("3. Atualizar Dados")
        print("4. Deletar Dados")
        print("5. Sair do Programa")
        
        #captura a escolha do usuário
        opcao = input("Escolha uma opção (1-5): ")
        
        #verifica se o usuário digitou uma opção válida e não deixou em branco
        if opcao == "1":
            entrada_dados()  #entrada de dados
        elif opcao == "2":
            saida_dados()  #exibe os dados e realiza cálculos
        elif opcao == "3":
            atualizar_dados()  #atualiza os dados existentes
        elif opcao == "4":
            deletar_dados()  #deleta os dados
        elif opcao == "5":
            print("Saindo do programa...")
            break  #sai do loop e encerra o programa
        else:
            print("Opção inválida! Tente novamente.")

#variáveis globais para armazenar os dados
largura_terreno = None
comprimento_terreno = None
latitude = None
longitude = None

#executa o menu
menu()
