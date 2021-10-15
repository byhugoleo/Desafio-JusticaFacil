# Documentação

Para o funcionamento do projeto algumas ferramentas precisam ser instaladas, assumindo que seja usado um **editor de código** ou **IDE** qualquer, será necessário a **instalação do Python** na máquina, fica a cargo do leitor providenciar buscar tutoriais de como instalar. Tendo o ambiente de desenvolvimento já pronto, o próximo passo é a **instalação do Selenium** WebDriver, que nos vai permitir manipular elementos da Web utilizando a linguagem Python, o link e downloads das ferramentas está no tópico "Ferramentas utilizadas". Tendo o Selenium WebDriver instalado, será necessário instalar o Driver, o utilitário que será utilizado pelo Selenium, como o script foi desenvolvido como base o navegador Chrome, ele será nosso navegador padrão para execução do script. Após baixar o arquivo do **ChromeDriver**, será necessário adicioná-lo à variável do sistema "Path".

## Ferramentas utilizadas
- [Windows 10 21H1](https://www.microsoft.com/pt-br/software-download/windows10)
-  [Visual Studio Code (Editor de código)](https://code.visualstudio.com/download)
-  [Linguagem de desenvolvimento Python 3.9.7](https://www.python.org/downloads/)
-  [API Selenium WebDriver](https://pypi.org/project/selenium/)
-  [ChromeDriver 94.0.4606.61](https://chromedriver.chromium.org/)
-  [Google Chrome 94.0.4606.81](https://www.google.com/intl/pt-BR/chrome/)


### Instalação do Selenium WebDriver
Abrindo o terminal do seu sistema operacional, digite a seguinte instrução:

    pip install -U selenium
### Instalação do ChromeDriver
Acessar o link disponível no tópico "Ferramentas utilizadas" e realizar o download do arquivo do ChromeDriver.
Assumindo que o sistema operacional seja Windows, após extrair o arquivo, será necessário adicionar "chromedriver.exe" variável do sistema "Path".

# Desenvolvimento
A classe criada **ScriptJustica** contém métodos para execução do script automatizado e alteração da data de publicação requisitada pelo usuário, esses **métodos** são os visíveis ao usuário, os outros demais métodos são internos e não são visíveis ao usuário.
```python
class  ScriptJustica:
# Muda a data de publicação a ser pesquisada para execução do script
	def  mudar_data_pesq(self,  data_nova):---
# Executa o processo de automatização de downloads dos diários e renomeá-los para seu respectivo MD5
	def  executar(self):---
```
**Atributos** da classe ScriptJustica
```python
class ScriptJustica:
	__site_stf_diarios # Armazena o link da página de pesquisa dos diários oficiais
	def __init__(self):
		__data_public # Armazena a data requisitada pelo usuário, e será utilizada para execução do script, formato: DD-MM-AAAA
		__dir_nome # Armazena o caminho do diretório principal, nele terá subpastas relacionadas a data os diários e uma subpasta temporária para downloads tmp
		__dir_downloads # Armazena o caminho para pasta de downloads chamada tmp
		__opcoes # Adiciona configurações à interface do ChromeDrivew
```

Os **métodos** da classe ScriptJustica são seis métodos ao todo, sendo quatro internos sendo usados somente dentro da classe e não visíveis aos usuários. O método **\_\_init__(self)**:

```python
# Construtor da classe
def  __init__(self):
# Trata se o argumento da data foi passada na inicialização do programa: python script.py 15-09-2021. Com isso é garantido que o programe não continue caso não seja passado a data
	try:
		self.__data_public = sys.argv[1]
	except  IndexError  as idxE:
		raise  Exception('\n'  +  ('─'  *  100)  +  "\nNão foi passado a data como argumento na execução, tente: \npython script.py DD-MM-AAAA\n"  +  ('─'  *  100)  +  '\n')
	self.__valida_data() # Validador de data, verifica se o formato passado é DD-MM-AAAA
	
# Cria os nomes dos diretórios, principal e de download
	self.__dir_nome = os.path.join(os.path.dirname(__file__),  "script_justica") # Formato: caminho_qualquer\script_justica
	self.__dir_downloads = os.path.join(self.__dir_nome,  "tmp") # Formato: caminho_qualquer\script_justica\tmp

# Cria os diretórios no disco
	if  not  (os.path.exists(self.__dir_nome)): # Caso não existir os diretórios, então são criados
		os.mkdir(self.__dir_nome)
		os.mkdir(self.__dir_downloads)

# Configurações do ChromeWebDriver
	self.__opcoes = webdriver.ChromeOptions()
# Configuração para não abrir os .pdf no navegador e fazer os downloads
	self.__opcoes.add_experimental_option('prefs', {
	"download.default_directory": self.__dir_downloads,
	"download.prompt_for_download": False,
	"download.directory_upgrade": True,
	"plugins.always_open_pdf_externally": True,})
#Configuração para desabilitar os logs durante execução do programa
	self.__opcoes.add_experimental_option('excludeSwitches'
	['enable-logging'])
```
O método **mudar_data_pesq(self,  data_nova)** e **\_\_valida_data(self)**:

```python
# Muda o valor da variável __data_public e valida
def  mudar_data_pesq(self,  data_nova):
	self.__data_public = data_nova
	self.__valida_data()

# Valida o formato da variável __data_public
def  __valida_data(self):
# Tratamento para caso o formato não seja o requisitado
	try:
		datetime.strptime(self.__data_public,  "%d-%m-%Y")
	except  ValueError:
		raise  ValueError('\n'  +  ('─'  *  100)  +  f"\nData \"{self.__data_public}\" no formato incorreto, correto sendo: DD-MM-AAAA.\n"  +  ('─'  *  100)  +  '\n')
```
Método **\_\_verifica_downloads_chrome(self,  driver)**:
```python
# Método utilizado para verificar os downloads ativos no momento e retorna seu caminho onde foram salvos
def  __verifica_downloads_chrome(self,  driver):
# Navega para página de downloads do Chrome
	if  not driver.current_url.startswith("chrome://downloads"):
		driver.get("chrome://downloads/")

# Retorna o script que captura os downloas do Chrome e retorna seu caminho.
	return driver.execute_script("""
	var items = document.querySelector('downloadsmanager').shadowRoot.getElementById('downloadsList').items;
	if (items.every(e => e.state === "COMPLETE"))
		return items.map(e => e.fileUrl || e.file_url);""")
```

Método **executrar(self)**, a estratégia de realizar a busca no site pela data fornecida foi afetada, devido o campo de busca de "Data de Publicação" não estar aceitando outros tipos de caracteres além o dígito "8", por isso no campo de pesquisa "Pesquisa Livre", foi inserido o a data neste campo no formato "DD/MM/AAAA" e selecionado todo o texto e copiado, o campo "Pesquisa Livre" foi limpo, a data copiada do campo "Pesquisa Livre" foi colado no campo "Data de Publicação", neste caso, este campo estava aceitando a entrada de texto e funcionou normalmente o restante do processo. Segue explicação do método:
```python
# Executa o processo de automatização de downloads dos diários e renomeá-los para seu respectivo MD5
def  executar(self):
# Conexão e acesso ao site
	driver = webdriver.Chrome(options=self.__opcoes)
	driver.get(self.__site_stf_diarios)

# Pesquisa pela data fornecida
	# Procura elemento pela sua ID "argumento"
	aux_textcpy = driver.find_element_by_id("argumento")
	# Envia o valor de __data_public para o campo "Pesquisa Livre"
	aux_textcpy.send_keys(self.__data_public.replace('-',  '/',  2))
	# Seleciona todo o texto
	aux_textcpy.send_keys(Keys.CONTROL,  'a')
	# Copia o texto
	aux_textcpy.send_keys(Keys.CONTROL,  'c')
	# Limpa a caixa de pesquisa
	aux_textcpy.clear()
	
	# Busca o elemento da caixa de pesquisa "Data Publicação"
	pesq_datapub = driver.find_element_by_id("dataP")
	# Limpa o campo
	pesq_datapub.clear()
	# Cola o texto copiado do campo "Pesquisa Livre"
	pesq_datapub.send_keys(Keys.CONTROL,  'v')

	# Busca o elemento do botão "Pesquisar"
	botao_pesq = driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/div[2]/div[2]/form/table/tbody/tr[3]/td/input[1]")
	# Realiza a ação de clicar	
	botao_pesq.click()

	# Aguarda carregar a tabela com os diários
	time.sleep(10)

# Tratamento para caso a busca não retorne nenhum diário oficial
	try:
		dados_tab =  WebDriverWait(driver,  5).until(EC.presence_of_element_located((By.CLASS_NAME,  "resultadoLista")))
	except TimeoutException:
		print('\n'  +  ('─'  *  100)  +  f"\nNenhum diário oficial encontrado na data {self.__data_public}.\n"  +  ('─'  *  100)  +  '\n')
		driver.close()
		return  False  # Não há diários nessa data : Retorna Falso.

# Downloas dos diários
	# Busca o elemento das linhas da tabela extraída
	dados_lin = dados_tab.find_elements_by_tag_name("tr")
	# Percorre as linhas da tabela
	for i in dados_lin:
		# Busca os elementos da coluna na i-ésima linha
		dados_col = i.find_elements_by_tag_name("td")
		# Condição para pular o cabeçalho da tabela
		if  (len(dados_col)):
			# Realiza o downloads do url retornado da busca
			driver.get(dados_col[3].find_element_by_tag_name("a").get_attribute("href"))

# Salvar arquivos renomeados com seu respectivo MD5
	# Aguarda os downloads completarem, retornano os seus caminhos
	diarios_pdf =  WebDriverWait(driver,  120,  1).until(self.__verifica_downloads_chrome)
	# O formato retornado começa com "file:///", e os caracteres de " " são "%20", dessa forma a instrução remove "file:///" e substitui "%20" por " "
	diarios_pdf =  list(map(lambda  nome_pdf  : nome_pdf[8:].replace('%20',  '  ').replace('/',  '\\'), diarios_pdf))
	# Cria o nome do diretório em que os diários serão movidos, formato: caminho_qualquer/data_publicao
	dir_diarios = os.path.join(self.dir_nome,  self.__data_public.replace('-',  '_',  2))
	# Cria o diretório caso não foi criado ainda
	if  not  (os.path.exists(dir_diarios)):
		os.mkdir(dir_diarios)
	# Relatório da operação, mostrando o diretório onde serão salvos os diários
	print('\n'  +  ('─'  *  100)  +  f"\nDiretorio diarios PDF: {dir_diarios}\n")
	# Para cara diário baixado, é retornado o seu código MD5
	diarios_pdf_MD5 =  list(map(lambda  nome_pdf  : hashlib.md5(open(nome_pdf,  'rb').read()).hexdigest(), diarios_pdf))
	# percorre o caminho dos diários na pasta "caminho_qualquer/tmp"
	for i in  range(0,  len(diarios_pdf)):
		# Relatório da operação, mostrano o caminho antigo e o nome do diário antigo, e mostrando o caminho novo com o diário ja renomeado com seu MD5
		print(diarios_pdf[i]  +  '\n'  + os.path.join(dir_diarios, diarios_pdf_MD5[i]  +  ".pdf")  +  '\n'  +  ('─'  *  100)  +  '\n')
		# Processo para mover os arquivos da pasta "tmp" para o novo diretório
		shutil.move(diarios_pdf[i], os.path.join(dir_diarios, diarios_pdf_MD5[i]  +  ".pdf"))
	# Encerra a conexão
	driver.close()
	return  True  # Script executado com sucesso : Retorna Verdadeiro.
```
O último método é para converter o objeto da classe em uma string:
```python
# Objeto para string
def  __str__(self):
	return  '\n'  +  ('─'  *  100) +  (f"\nSite: {self.__site_stf_diarios}" 
	+  f"\nDiretório principal: {self.__dir_nome}" 
	+ f"\nDiretório de Download (temporário): {self.__dir_downloads}" 
	+ + f"\nData atual de pesquisa: {self.__data_public}\n")  +  ('─'  *  100)  +  '\n'
```

# Conclusão
Com isso foi possível realizar as operações necessárias para resolução do problema proposto. Foi adquirido conhecimentos em Python e API Selenium, podendo manipular em um nível básico para intermediário.
Segue execução do código:

![Teste](https://i.imgur.com/zYBXxEe.gif)