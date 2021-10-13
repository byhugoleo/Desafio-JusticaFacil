import os
import shutil
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import sys

class ScriptJustica:
    "Script para automatização de processo de downloads de diários oficiais."

    __site_stf_diarios = "http://www.stf.jus.br/portal/diariojusticaeletronico/pesquisarDiarioEletronico.asp"
    @property
    def site_stf_diarios(self):
        return self.__site_stf_diarios

    def __init__(self):
        self.data_public = sys.argv[1]
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
        "plugins.always_open_pdf_externally": True
        })
    @property
    def dir_nome(self):
        return self.__dir_nome
    @property
    def dir_downloads(self):
        return self.__dir_downloads

    def verifica_downloads_chrome(self, auxdriver):
        if not self.__driver.current_url.startswith("chrome://downloads"):
            self.__driver.get("chrome://downloads/")
        return self.__driver.execute_script("""
        var items = document.querySelector('downloads-manager').shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
        
    def executar(self):
        #Conexão e acesso ao site
        self.__driver = webdriver.Chrome(options=self.__opcoes)
        self.__driver.get(self.__site_stf_diarios)

        #Pesquisa pela data fornecida
        aux_textcpy = self.__driver.find_element_by_id("argumento")
        aux_textcpy.send_keys(self.data_public.replace('-', '/', 2))
        aux_textcpy.send_keys(Keys.CONTROL, 'a')
        aux_textcpy.send_keys(Keys.CONTROL, 'c')
        aux_textcpy.clear()

        pesq_datapub = self.__driver.find_element_by_id("dataP")
        pesq_datapub.clear()
        pesq_datapub.send_keys(Keys.CONTROL, 'v')

        botao_pesq = self.__driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td/input[1]")
        botao_pesq.click()
        time.sleep(5)
        
        dados_tab = self.__driver.find_element_by_class_name("resultadoLista")
        dados_lin = dados_tab.find_elements_by_tag_name("tr")

        # Downloas dos diários
        for i in dados_lin:
            dados_col = i.find_elements_by_tag_name("td")
            if (len(dados_col)):
                self.__driver.get(dados_col[3].find_element_by_tag_name("a").get_attribute("href"))
        
        # Salvar arquivos renomeados com seu respectivo MD5
        diarios_pdf = WebDriverWait(self.__driver, 120, 1).until(self.verifica_downloads_chrome)
        diarios_pdf = list(map(lambda nome_pdf : nome_pdf[8:].replace('%20', ' '), diarios_pdf))
        dir_diarios = os.path.join(self.dir_nome, self.data_public.replace('-', '_', 2))
        if not (os.path.exists(dir_diarios)):
            os.mkdir(dir_diarios)
        diarios_pdf_MD5 = list(map(lambda nome_pdf : hashlib.md5(open(nome_pdf, 'rb').read()).hexdigest(), diarios_pdf))
        for i in range(0, len(diarios_pdf)):
            shutil.move(diarios_pdf[i], os.path.join(dir_diarios, diarios_pdf_MD5[i] + ".pdf"))

        self.__driver.close()

        return True

    


S = ScriptJustica()
print(S.site_stf_diarios)
print(S.dir_nome)
S.executar()
S.data_public = '22-09-2021'
S.executar()