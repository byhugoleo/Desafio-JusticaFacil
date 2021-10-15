# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from datetime import datetime
import hashlib
import shutil
import time
import sys
import os

class ScriptJustica:
    "Script para automatização de processo de downloads de diários oficiais."

    __site_stf_diarios = "http://www.stf.jus.br/portal/diariojusticaeletronico/pesquisarDiarioEletronico.asp"
    @property
    def site_stf_diarios(self):
        return self.__site_stf_diarios

    # Construtor
    def __init__(self):
        try:
            self.__data_public = sys.argv[1]
        except IndexError as idxE:
            raise Exception('\n' + ('─' * 100) + "\nNão foi passado a data como argumento na execução, tente: \npython script.py DD-MM-AAAA\n" + ('─' * 100) + '\n')
        self.__valida_data()

        self.__dir_nome = os.path.join(os.path.dirname(__file__), "script_justica")
        self.__dir_downloads = os.path.join(self.__dir_nome, "tmp")

        if not (os.path.exists(self.__dir_nome)):
            os.mkdir(self.__dir_nome)
            os.mkdir(self.__dir_downloads)

        self.__opcoes = webdriver.ChromeOptions()
        self.__opcoes.add_experimental_option('prefs', {
        "download.default_directory": self.__dir_downloads,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        })
        self.__opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
    @property
    def dir_nome(self):
        return self.__dir_nome
    @property
    def dir_downloads(self):
        return self.__dir_downloads

    # Muda a data de publicação a ser pesquisada para execução do script
    def mudar_data_pesq(self, data_nova):
        self.__data_public = data_nova
        self.__valida_data()

    # Função interna, valida a data de entrada
    def __valida_data(self):
        try:
            datetime.strptime(self.__data_public, "%d-%m-%Y")
        except ValueError:
            raise ValueError('\n' + ('─' * 100) + f"\nData \"{self.__data_public}\" no formato incorreto, correto sendo: DD-MM-AAAA.\n" + ('─' * 100) + '\n')

    def __verifica_downloads_chrome(self, driver):
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")
        return driver.execute_script("""
        var items = document.querySelector('downloads-manager').shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
    
    # Executa o processo de automatização de downloads dos diários e renomeá-los para seu respectivo MD5
    def executar(self):
        # Conexão e acesso ao site
        driver = webdriver.Chrome(options=self.__opcoes)
        driver.get(self.__site_stf_diarios)

        # Pesquisa pela data fornecida
        aux_textcpy = driver.find_element_by_id("argumento")
        aux_textcpy.send_keys(self.__data_public.replace('-', '/', 2))
        aux_textcpy.send_keys(Keys.CONTROL, 'a')
        aux_textcpy.send_keys(Keys.CONTROL, 'c')
        aux_textcpy.clear()

        pesq_datapub = driver.find_element_by_id("dataP")
        pesq_datapub.clear()
        pesq_datapub.send_keys(Keys.CONTROL, 'v')

        botao_pesq = driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td/input[1]")
        botao_pesq.click()

        # Aguarda carregar a tabela com os diários
        time.sleep(10)
        
        try:
            dados_tab = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "resultadoLista")))
        except TimeoutException:
            print('\n' + ('─' * 100) + f"\nNenhum diário oficial encontrado na data {self.__data_public}.\n" + ('─' * 100) + '\n')
            driver.close()
            return False # Não há diários nessa data : Retorna Falso.

        # Downloas dos diários
        dados_lin = dados_tab.find_elements_by_tag_name("tr")
        for i in dados_lin:
            dados_col = i.find_elements_by_tag_name("td")
            if (len(dados_col)):
                driver.get(dados_col[3].find_element_by_tag_name("a").get_attribute("href"))
        
        # Salvar arquivos renomeados com seu respectivo MD5
        diarios_pdf = WebDriverWait(driver, 120, 1).until(self.__verifica_downloads_chrome)
        diarios_pdf = list(map(lambda nome_pdf : nome_pdf[8:].replace('%20', ' ').replace('/', '\\'), diarios_pdf))
        dir_diarios = os.path.join(self.dir_nome, self.__data_public.replace('-', '_', 2))

        if not (os.path.exists(dir_diarios)):
            os.mkdir(dir_diarios)

        print('\n' + ('─' * 100) + f"\nDiretorio diarios PDF: {dir_diarios}\n")

        diarios_pdf_MD5 = list(map(lambda nome_pdf : hashlib.md5(open(nome_pdf, 'rb').read()).hexdigest(), diarios_pdf))
        for i in range(0, len(diarios_pdf)):
            print(diarios_pdf[i] + '\n' + os.path.join(dir_diarios, diarios_pdf_MD5[i] + ".pdf") + '\n' + ('─' * 100) + '\n')
            shutil.move(diarios_pdf[i], os.path.join(dir_diarios, diarios_pdf_MD5[i] + ".pdf"))

        driver.close()

        return True # Script executado com sucesso : Retorna Verdadeiro.

    # Objeto para string
    def __str__(self):
        return '\n' + ('─' * 100) + (f"\nSite: {self.__site_stf_diarios}" + f"\nDiretório principal: {self.__dir_nome}" +
        f"\nDiretório de Download (temporário): {self.__dir_downloads}" +
        f"\nData atual de pesquisa: {self.__data_public}\n") + ('─' * 100) + '\n'
        

# Testes
S = ScriptJustica()
# print(S)
S.executar()
# S.mudar_data_pesq("04-03-2021")
# print(S)
# S.executar()