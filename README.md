# Desafio Justiça Fácil
## Problema
Os diários oficiais são jornais criados, mantidos e administrados por governos para publicar as literaturas dos atos oficiais da administração pública executiva, legislativa e judiciária.

Todos os dias, o sistema desenvolvido pelo Justiça Fácil tem que verificar se os diários do Supremo Tribunal Federal foram baixados corretamente. Para evitar que o mesmo diário seja processado mais de uma vez, é necessário um sistema auxiliar na conferência dos diários baixados pelo sistema, ou seja, um programa que receba uma data e retorne os MD5 dos diários daquele dia.
O candidato deve criar uma solução que receba uma data de disponibilização (data em que o diário foi colocado no sistema do tribunal) e retorne uma lista de hash MD5 dos PDFs dos diários disponibilizados na data buscada.

_ATENÇÃO_: O Supremo Tribunal Federal disponibiliza duas versões do PDF, a versão que deve ser buscada é a Integral.

O código deve ser escrito preferencialmente em Python

# Metodologia

Como análise do problema, foi percebido que seria necessário manipulação de arquivos, string, e estruturas de dados além de conhecimento na linguagem [Python](https://www.python.org/). Porém os dados a serem manipulados seriam extraídos da Web, feito uma pesquisa encontrei a utilização do módulo [Selenium](https://selenium-python.readthedocs.io/#) para extração e inserção de dados entre o navegador e o programa em execução na máquina.
De início foi trabalhado o conhecimento na linguagem, como seus paradigmas, sintaxe e sua semântica. Os problemas encontrados pela frente foi pelo fato de não ter conhecimento na linguagem, e a cada novo passo da resolução do problema era um desafio. Com os problemas em mente, comecei fazendo o básico, estudando o funcionamento do Selenium, realizando aplicações básicas, como abrir uma página, e extrair algum dado a partir do seu HTML. Depois foi como baixar um arquivo .pdf a partir de um link qualquer. Buscando um pouco mais de conhecimento já tinha conseguido extrair informação de qualquer parte do site através dos métodos fornecidos pelo Selenium, o desafio foi juntar todo o processo: abrir o navegador, acessar a data requisitada pelo usuário, acessar a tabela onde estariam os diários fornecidos pela busca, realizar tratamentos em caso de não encontrar nenhum diário na busca. Com esta parte do problema já desenvolvida o desafio foi armazenar os diários com seus respectivos MD5 como nome do arquivo. Para facilitar o Python tem um módulo chamado [hashlib](https://docs.python.org/3/library/hashlib.html) no qual fornece métodos que realiza o processo de gerar o código MD5 de um arquivo. Após ter tudo pronto, foi necessário somente organizar o código para que fique mais fácil de se compreender. Todas as funcionalidades exigidas foram desenvolvidas, até algumas a mais, como a possibilidade de alterar a data buscada dos diários e executar o script novamente, isso devido ao código ser desenvolvido em programação orientada a objetos, sendo possível reutilizar o código de maneira mais flexível.

As fontes de pesquisas utilizadas foram:
- [Stack Overflow](https://stackoverflow.com/)
- [Selenium with Python](https://selenium-python.readthedocs.io/)
- [Python 3.10.0 documentation](https://docs.python.org/3/)
- [Try2Explore](https://qa.try2explore.com/)
- [A Whirlwind Tour of Python](jakevdp.github.io/)
- [PensePython](https://panda.ime.usp.br/pensepy/static/pensepy/)
- [TutorialsTeacher](https://www.tutorialsteacher.com/python/)
- [linuxhint](https://linuxhint.com/)
- [note.nkmk.me](note.nkmk.me)
- [The Geek Stuff](https://www.thegeekstuff.com/)
- [Selenium 3.141 documentation](https://www.selenium.dev/)
