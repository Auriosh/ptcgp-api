# API de Pokémon TCG Pocket

![Build Status](https://github.com/Auriosh/ptcgp-api/actions/workflows/build-api.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma API RESTful, gratuita e de código aberto, que fornece dados estruturados sobre as cartas do jogo Pokémon TCG Pocket. Este é um projeto pessoal, desenvolvido e mantido por **Auriosh**.

---

## Navegador Interativo da API

Para uma forma fácil de explorar visualmente todos os dados, coleções e cartas, aceda ao nosso navegador interativo:

**[➡️ Aceder ao Navegador da API](https://Auriosh.github.io/ptcgp-api/)**

---

## URL Base da API

Todos os endpoints partilham o mesmo URL base, que aponta para os ficheiros gerados e hospedados através do GitHub Pages.


**[https://Auriosh.github.io/ptcgp-api/v1](https://Auriosh.github.io/ptcgp-api/v1)**


---

## Endpoints Principais

### 1. Obter a Lista de Coleções (Sets)
* **URL:** `/cards/{idioma}/sets.json`

### 2. Obter os Dados de uma Carta Específica
* **URL:** `/cards/{idioma}/{set_id}/{card_id}.json`

---

## Ferramentas e Agradecimentos

* **Fonte dos Dados:** Os dados de texto das cartas são obtidos através da fantástica API pública [**TCGdex.net**](https://tcgdex.net). Um agradecimento especial à equipa do TCGdex por fornecerem este recurso valioso à comunidade.
* **Assistência de IA:** Este projeto foi desenvolvido com o auxílio extensivo da **Gemini**, a IA da Google, que foi fundamental desde a fase de brainstorming e planeamento da arquitetura até à criação e depuração dos scripts de automação.

---

## Sugestões e Relatório de Erros

Se encontrar algum erro nos dados ou tiver sugestões para melhorar a API, sinta-se à vontade para abrir uma [**Issue**](https://github.com/Auriosh/ptcgp-api/issues) no repositório do GitHub.

## Licença

Este projeto é distribuído sob a **Licença MIT**. Veja o ficheiro [**LICENSE**](LICENSE) para mais detalhes.
 