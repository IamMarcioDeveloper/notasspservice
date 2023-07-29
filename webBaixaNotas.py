from selenium import webdriver
from time import sleep
import rpa as r
import pyautogui as p
import os as os
from datetime import date as d
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
from datetime import timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome

# Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

##setando variaveis
index = 3
tr = 2
erro = True
mov = True
lista = []
listaCsv = []
posicao = 0
waitnalto = 2
waitbaixo = 1.5
if d.today().day < 15:
    mes_competencia = ('0' + str(d.today().month - 1))[-2:]
else:
    mes_competencia = ('0' + str(d.today().month))[-2:]
ano_competencia = str(d.today().year)
ultimodiames = str(datetime.today() + timedelta(days=-datetime.today().day)).replace('-', '')[0:8]
usuario = os.getlogin()
pastaDownload = (fr'C:\Users\{usuario}\Downloads')

##alimentando serviços web
opts = ChromeOptions()
# esta opcao serve para nao fechar o navegador apos a execucao do script
opts.add_experimental_option("detach", True)
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=opts)

#apagar todos os arquivos da pasta download
for f in os.listdir(pastaDownload):
    os.remove(os.path.join(pastaDownload, f))

# rodando a aplicação
driver.get("https://nfe.prefeitura.sp.gov.br/")
p.getActiveWindow().maximize()

try:
    element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="ctl00_body_pnICP"]/p/a')))
finally:
    p.moveTo(x=1141, y=451)
    p.click()
    p.press('enter')
try:
    element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="ctl00_body_btAcesso"]')))
finally:
    element = driver.find_element(By.XPATH, '//*[@id="ctl00_body_btAcesso"]')
    element.click()

# Laço de reptição para catalogar as procurações vinculadas a contabilidade
while (erro):
    try:
        driver.find_element(By.XPATH, f'//*[@id="ctl00_body_ddlPrestador"]/option[{index}]')
    except:
        posicao = 0
        erro = False
    finally:
        if erro == True:
            lista.append(driver.find_element(By.XPATH, f'//*[@id="ctl00_body_ddlPrestador"]/option[{index}]').text)
            index += 1
            posicao += 1

for i in range(3):
    posicao = 0
    for x in lista:
        if i == 0:
            driver.get(
                f'https://nfe.prefeitura.sp.gov.br/contribuinte/notasrecapuradasnfts.aspx?inscricao={lista[posicao].replace(".", "").replace("-", "")[:9]}&cpfcnpj=&nome=&regime=2&ano={ano_competencia}&mes={mes_competencia}&pagas=1&pendentes=1&canceladas=1&incidencia=true')
            elementTipoArquivo = Select(driver.find_element(By.NAME, 'ctl00$cphPopUp$true$ddlTipoArquivo'))
            elementTipoArquivo.select_by_value('0')
            elementTipoLyout = Select(driver.find_element(By.NAME, 'ctl00$cphPopUp$true$ddlLayoutArquivo'))
            elementTipoLyout.select_by_value('3')
            driver.find_element(By.XPATH, '//*[@id="ctl00_cphPopUp_true_btGerar"]').click()
            p.sleep(int(waitbaixo))
            posicao += 1
        if i == 1:
            driver.get(
                f'https://nfe.prefeitura.sp.gov.br/contribuinte/notasrecapuradas.aspx?inscricao={lista[posicao].replace(".", "").replace("-", "")[:9]}&cpfcnpj=&nome=&regime=2&ano={ano_competencia}&mes={mes_competencia}&pagas=1&pendentes=1&canceladas=1&incidencia=true')
            elementTipoArquivo = Select(driver.find_element(By.NAME, 'ctl00$cphPopUp$true$ddlTipoArquivo'))
            elementTipoArquivo.select_by_value('0')
            elementTipoLyout = Select(driver.find_element(By.NAME, 'ctl00$cphPopUp$true$ddlLayoutArquivo'))
            elementTipoLyout.select_by_value('3')
            driver.find_element(By.XPATH, '//*[@id="ctl00_cphPopUp_true_btGerar"]').click()
            p.sleep(int(waitnalto))
            if os.path.exists(
                    fr'C:\Users\automate\Downloads\NFSe_{lista[posicao].strip().replace(".", "").replace("-", "")[:9].strip()}_{ano_competencia + mes_competencia + "01"}_{ultimodiames}.txt') \
                    or os.path.exists(
                fr'C:\Users\automate\Downloads\NFSe_{lista[posicao].strip().replace(".", "").replace("-", "")[:9].strip()}_{ano_competencia + mes_competencia + "01"}_{ultimodiames}.txt.crdownload'):
                p.sleep(int(waitnalto))
                posicao += 1
            # switch é um metodo usado para bular alertas que não é interação browser, neste caso aparece a Janela de Numero de caracteres maior que 8
            else:
                print(lista[posicao].replace(".", "").replace("-", "")[:9])
                try:
                    driver.switch_to.alert.accept()
                    # alert.accept()
                except:
                    pass
                finally:
                    # Caso exista a janela será salvo o arquivo no modelo CSV
                    driver.get(
                        f'https://nfe.prefeitura.sp.gov.br/contribuinte/notasrecapuradas.aspx?inscricao={lista[posicao].replace(".", "").replace("-", "")[:9]}&cpfcnpj=&nome=&regime=2&ano={ano_competencia}&mes={mes_competencia}&pagas=1&pendentes=1&canceladas=1&incidencia=true')
                    elementTipoArquivo = Select(driver.find_element(By.NAME, 'ctl00$cphPopUp$true$ddlTipoArquivo'))
                    elementTipoArquivo.select_by_value('2')
                    elementTipoLyout = Select(driver.find_element(By.NAME, 'ctl00$cphPopUp$true$ddlLayoutArquivo'))
                    elementTipoLyout.select_by_value('4')
                    driver.find_element(By.XPATH, '//*[@id="ctl00_cphPopUp_true_btGerar"]').click()
                    p.sleep(int(waitnalto))
                    posicao += 1
        if i == 2:
            driver.get(
                f'https://nfe.prefeitura.sp.gov.br/contribuinte/notasapuradas.aspx?inscricao={lista[posicao].replace(".", "").replace("-", "")[:9]}&cpfcnpj=&nome=&regime=2&ano={ano_competencia}&mes={mes_competencia}&pagas=1&pendentes=1&canceladas=1&incidencia=true')
            elementTipoArquivo = Select(driver.find_element(By.NAME, 'ctl00$cphPopUp$true$ddlTipoArquivo'))
            elementTipoArquivo.select_by_value('0')
            elementTipoLyout = Select(driver.find_element(By.NAME, 'ctl00$cphPopUp$true$ddlLayoutArquivo'))
            elementTipoLyout.select_by_value('3')
            driver.find_element(By.XPATH, '//*[@id="ctl00_cphPopUp_true_btGerar"]').click()
            p.sleep(int(waitbaixo))
            posicao += 1