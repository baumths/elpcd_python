# ElPCD 0.1 alpha
Elaborador de Plano de Classificação de Documentos (e Tabela de Temporalidade Documental 'WIP')

- versão 0.1:
    - Cria, edita e apaga classes, padrão das classes: e-ARQ Brasil
    - Exporta os dados em .CSV podendo ser importado pelo AtoM (https://accesstomemory.org)
    
- Futuras versões:
    - Modulo Importação do PCD em .CSV
    - Modulo Tabela de Temporalidade Documental, no padrão e-ARQ Brasil
    - Modulos Importação e Exportação de .CSV para o Modulo TTD
    - Modulo de Importação e Exportação de .XML para os Modulos PCD e TTD

Quaisquer sugestões, por favor entre em contato pelo Twitter.

Email do grupo de pesquisa: cnpqdocsdigitais@gmail.com

Link do projeto no GitHub: (https://github.com/MBaumgartenBR/ElPCD)
Link para contato: (https://twitter.com/mbaumgartenbr)

Para rodar o projeto no seu ambiente de desenvolvimento (assumindo que já possua python,pip,venv instalados):
Clone o repositório do projeto:
```bash
git clone https://github.com/MBaumgartenBR/ElPCD.git
```
Abra a pasta do repositório:
```bash
cd ElPCD/
```
Crie o ambiente virtual para os pacotes do python:
```bash
python3 -m virtualenv venv
```
Ative o ambiente virtual:
```bash
source venv/bin/activate
```
Atualize os pacotes pip, wheel, setuptools e instale o cython:
```bash
pip3 install --upgrade pip, wheel, setuptools, cython
```
Instale o Kivy (1.11.1) Framework para Python 3.8:
```bash
pip3 install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/
```
Instale o KivyMD:
```bash
pip3 install git+https://github.com/HeaTTheatR/KivyMD.git
```
Tudo pronto para modificar quaisquer arquivos que desejar.
#Para executar a aplicação:
```bash
python3 main.py
```
**Caso ocorra algum erro, por favor informe à mim pelo Twitter.**