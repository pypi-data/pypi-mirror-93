# victorbaptistalemos_libpythonpro

Módulo para exemplificar construção de projetos Python no curso PyTools.

Nesse curso é ensinado como contribuir para projetos de código aberto.

Link para o curso [Python Pro](https://www.python.pro.br).

Este projeto tem como base o repositório [pythonprobr/libpythonpro](https://www.github.com/pythonprobr/libpythonpro).

Suportada a versão 3 do Python.

Tópicos a serem abordados:

1. Git
   1. Clone 
   2. Fork
   3. Branch
   4. Pull request
   5. Issues
   6. Feature branch

   
2. Virtualenv
   1. Criar
      ```console
      python3 -m venv .venv
      ```
   2. Ativar
      ```console
      source .venv/bin/activate
      ```
   3. Desativar
      ```console
      deactivate
      ```


3. Pip
   1. Instalar
      ```console
      pip install -r requirements.txt
      ```
   2. Atualizar
      ```console
      pip install --upgrade requests
      ```
   3. Desinstalar
      ```console
      pip uninstall -r requirements.txt -y
      ```
   4. Requirements
      ```console
      pip freeze > requirements.txt
      ```
   5. Flake8
      1. Instalar
         ```console
         pip install flake8
         ```
      2. Configurar 
         ```console
         # Crie um arquivo .flake8
         # Insira no arquivo .flake8 as configurações abaixo (sem o #)
         # [flake8]
         # max-line-length = 120
         # exclude = .venv
         ```
      3. Conferir qualidade do código
         ```console
         flake8
         ```
4. Travis CI
   [![Build Status](https://www.travis-ci.com/victorbaptistalemos/libpythonpro.svg?branch=main)](https://www.travis-ci.com/victorbaptistalemos/libpythonpro)
   

5. PyUp 
   [![Updates](https://pyup.io/repos/github/victorbaptistalemos/libpythonpro/shield.svg)](https://pyup.io/repos/github/victorbaptistalemos/libpythonpro/)
   [![Python 3](https://pyup.io/repos/github/victorbaptistalemos/libpythonpro/python-3-shield.svg)](https://pyup.io/repos/github/victorbaptistalemos/libpythonpro/)
