from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import re

def procurar_contato(driver, contato):
    try:
        # Aguarda o carregamento completo da página
        time.sleep(5)
        
        # Localiza a caixa de pesquisa
        search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div/p')
        search_box.clear()  # Limpa o campo de pesquisa
        search_box.send_keys(contato)
        
        # Aguarda um tempo curto para que o WhatsApp sugira os resultados de pesquisa
        time.sleep(2)
        
        # Localiza o contato na lista de resultados
        search_result = driver.find_element(By.XPATH, f'//span[@title="{contato}"]')
        search_result.click()  # Clica no resultado da pesquisa
    except Exception as e:
        print("Erro ao procurar o contato:", e)

def abrir_conversa(driver, contato):
    try:
        # Aguarda o carregamento completo da página
        time.sleep(5)
        
        # Localiza o nome da conversa na lista de conversas recentes e clica nele
        conversation_name = driver.find_element(By.XPATH, f'//span[@title="{contato}"]')
        conversation_name.click()
        
        # Aguarda um tempo curto para o carregamento da conversa
        time.sleep(5)
    except Exception as e:
        print("Erro ao abrir a conversa:", e)

def enviar_mensagem(driver, mensagem):
    try:
        # Aguarda o carregamento completo da página
        time.sleep(5)
        
        # Localiza a caixa de mensagem e envia a mensagem
        message_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
        message_box.send_keys(mensagem)
        message_box.send_keys(Keys.ENTER)
        
        # Aguarda um tempo antes de fechar o navegador
        time.sleep(2)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

def enviar_mensagem_inicial(driver):
    mensagem_inicial = "Olá eu sou DiceMaster!! Vamos rolar uns dados? 🎲"
    enviar_mensagem(driver, mensagem_inicial)

def rolar_dados(quantidade, lados):
    resultados = [random.randint(1, lados) for _ in range(quantidade)]
    return resultados

def calcular_resultado(comando):
    partes = re.split(r'(\+|\-|\*|\/)', comando)
    dados_partes = partes[0].split("d")
    quantidade = int(dados_partes[0])
    lados = int(dados_partes[1])
    dados = rolar_dados(quantidade, lados)
    operador = partes[1]
    if len(partes) > 2:
        numero = int(partes[2])
    else:
        numero = 0
    if operador == "+":
        resultado = sum(dados) + numero
    elif operador == "-":
        resultado = sum(dados) - numero
    elif operador == "*":
        resultado = sum(dados) * numero
    elif operador == "/":
        resultado = sum(dados) / numero if numero != 0 else "Divisão por zero"
    return dados, operador, numero, resultado

def lidar_com_mensagem(mensagem):
    comando = mensagem.split()[0]  # Extrair o comando da mensagem
    if re.match(r'^\d+d\d+[\+\-\*\/]\d*$', comando):
        dados, operador, numero, resultado = calcular_resultado(comando)
        mensagem_resultado = f"Resultado da operação {comando}: 🎲 {dados} {operador} {numero if numero else 'os dados'} = {resultado}"
    else:
        mensagem_resultado = "Comando inválido. Use /XdY[+|-|*|/]Z para realizar uma operação com dados, onde X é a quantidade de dados, Y é o número de lados dos dados e Z é o número para a operação."
    return mensagem_resultado

def verificar_pedido_rolagem(mensagem):
    # Verifica se a mensagem é um pedido de rolagem de dados
    return re.match(r'^rolar\s+\d+d\d+$', mensagem)

def enviar_rolagem_dados(driver, mensagem):
    # Extrai os parâmetros da mensagem de rolagem de dados
    parametros = mensagem.split()[1]  # Ignora o comando "rolar"
    quantidade, lados = map(int, parametros.split("d"))
    
    # Rola os dados e calcula o resultado
    resultados = rolar_dados(quantidade, lados)
    resultado_final = sum(resultados)
    
    # Envia a mensagem com o resultado
    mensagem_resultado = f"🎲 Resultado da rolagem de {quantidade}d{lados}: {resultados}. Total: {resultado_final}"
    enviar_mensagem(driver, mensagem_resultado)

def verificar_e_responder_mensagens(driver):
    while True:
        # Aguarda um tempo antes de verificar novas mensagens
        time.sleep(2)
        
        # Verifica se há novas mensagens
        mensagens = driver.find_elements(By.CLASS_NAME, "copyable-text")
        if mensagens:
            # Extrai o texto de cada mensagem
            for mensagem in mensagens:
                texto = mensagem.text
                if verificar_pedido_rolagem(texto):
                    enviar_rolagem_dados(driver, texto)

if __name__ == "__main__":
    # Inicializa o navegador
    driver = webdriver.Chrome()
    
    # Abre o WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    input("Pressione Enter depois de escanear o código QR...")

    # Procura o contato
    procurar_contato(driver, 'O chamado do cthulhu')

    # Abre a conversa
    abrir_conversa(driver, 'O chamado do cthulhu')

    # Envia a mensagem inicial
    enviar_mensagem_inicial(driver)

    # Inicia o loop para verificar e responder mensagens
    verificar_e_responder_mensagens(driver)
