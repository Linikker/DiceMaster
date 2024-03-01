from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

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

    # Envia a mensagem
    enviar_mensagem(driver, 'Oi')