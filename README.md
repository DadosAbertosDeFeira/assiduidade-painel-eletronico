# Assiduidade dos vereadores pelo painel eletrônico

Os dados tratados aqui foram conseguidos através de pedido de
acesso à informação feito a Câmara de Vereadores de Feira de Santana.

No dia 01 de Maio de 2021 recebemos via e-mail arquivos `.rar` com
relatórios da assiduidade dos edis (disponíveis na pasta `data/` desse repositório).
Os relatórios estão em formato `.xps`. Aqui encontram-se scripts que convertem
esses relatórios em texto e em seguida estrutura-os em `JSON`.

## Onde encontrar os arquivos

Os arquivos podem ser encontrados no nosso [Kaggle](https://www.kaggle.com/dadosabertosdefeira).

## Desenvolvimento

Para contribuir, basta ter o [Poetry](https://python-poetry.org/) instalado.
Ative o ambiente com `poetry shell` e em seguida instale as dependências com
`poetry install`.

Execute o script de conversão com `python from_xps_to_json.py`. O script vai ler as
pastas dentro de `data/` (você precisa descompactar os dados) e gerar os arquivos de texto
e demais `JSONs`.

Para rodar os testes, execute `pytest`.
