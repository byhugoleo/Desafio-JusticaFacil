import os
from selenium import webdriver

class ScriptJustica:
    "Script para automatização de processo de downloads de diários oficiais."

    __site_stf_diarios = "http://www.stf.jus.br/portal/diariojusticaeletronico/pesquisarDiarioEletronico.asp"
    @property
    def site_stf_diarios(self):
        return self.__site_stf_diarios

    def __init__(self):
        self.__dir_nome = os.path.join(os.path.dirname(__file__), "script_justica")
        self.__dir_downloads = os.path.join(self.__dir_nome, "tmp")
        if not (os.path.exists(self.__dir_nome)):
            os.mkdir(self.__dir_nome)
            os.mkdir(self.__dir_downloads)
    @property
    def dir_nome(self):
        return self.__dir_nome
    @property
    def dir_downloads(self):
        return self.__dir_downloads

    

    def iniciar_sessao(self):
        opcoes = webdriver.ChromeOptions()
        opcoes.add_experimental_option('prefs', {
        "download.default_directory": self.__dir_downloads,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
        })
        self.__driver = webdriver.Chrome(options=opcoes)

    def finalizar_sessao(self):
        self.__driver.close()

    


S = ScriptJustica()
print(S.site_stf_diarios)
print(S.dir_nome)
S.iniciar_sessao()
S.finalizar_sessao()