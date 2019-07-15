# Scrapper + Bot Telegram da Agenda Presidencial
Bot que faz scrapping da agenda presidencial (http://www2.planalto.gov.br/acompanhe-o-planalto/agenda-do-presidente-da-republica) e publica no Telegram.
Projeto elaborado para deploy no [AWS Lambda](https://aws.amazon.com/pt/lambda/) baseado no projeto [PyChromeless](https://github.com/21Buttons/pychromeless)


## Dependencias

Instale o Docker e as dependencias:

* Rode o comando `make fetch-dependencies`
* [Instalando Docker](https://docs.docker.com/engine/installation/#get-started)

## Como executar localmente

Com o seu [bot de telegram](https://core.telegram.org/bots) já criado e a chave da API para acessá-lo em mãos
Defina a variável de ambiente BOT_API_KEY com `export BOT_API_KEY=suachave`. 
Execute com: `make docker-run`
