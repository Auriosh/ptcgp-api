# API de Pokémon TCG Pocket

![Build Status](https://github.com/Auriosh/ptcgp-api/actions/workflows/build-api.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma API RESTful, gratuita e de código aberto, que fornece dados estruturados sobre as cartas do jogo Pokémon TCG Pocket. Este é um projeto pessoal, desenvolvido e mantido por **Auriosh**.

---

## URL Base da API

Todos os endpoints partilham o mesmo URL base, que aponta para os ficheiros gerados e hospedados através do GitHub Pages.

```
[https://Auriosh.github.io/ptcgp-api/v1](https://Auriosh.github.io/ptcgp-api/v1)
```

---

## Endpoints Principais

A API está organizada de forma a ser intuitiva e fácil de usar.

### 1. Obter a Lista de Coleções (Sets)

Para obter uma lista de todas as coleções disponíveis num determinado idioma, use o seguinte endpoint:

* **URL:** `/cards/{idioma}/sets.json`
* **Método:** `GET`
* **Parâmetros:**
    * `{idioma}`: O código do idioma desejado (ex: `pt_BR`, `en_US`, `ja_JP`).

#### Exemplo de Requisição (em Português)

```
[https://Auriosh.github.io/ptcgp-api/v1/cards/pt_BR/sets.json](https://Auriosh.github.io/ptcgp-api/v1/cards/pt_BR/sets.json)
```

#### Exemplo de Resposta (`sets.json`)

```json
[
  {
    "id": "A1",
    "name": "Dominação Genética",
    "logo": "/assets/logoImage/pt_BR/logo_A1_pt_BR.png"
  },
  {
    "id": "A1a",
    "name": "A Ilha Mítica",
    "logo": "/assets/logoImage/pt_BR/logo_A1a_pt_BR.png"
  }
]
```

### 2. Obter os Dados de uma Carta Específica

Para obter os detalhes completos de uma carta, utilize o seu ID único.

* **URL:** `/cards/{idioma}/{set_id}/{card_id}.json`
* **Método:** `GET`
* **Parâmetros:**
    * `{idioma}`: O código do idioma (ex: `pt_BR`).
    * `{set_id}`: O ID da coleção (ex: `A1`).
    * `{card_id}`: O ID completo da carta (ex: `A1-004`).

#### Exemplo de Requisição (Venusaur ex)

```
[https://Auriosh.github.io/ptcgp-api/v1/cards/pt_BR/A1/A1-004.json](https://Auriosh.github.io/ptcgp-api/v1/cards/pt_BR/A1/A1-004.json)
```

#### Exemplo de Resposta (uma carta)

```json
{
  "language": "pt_BR",
  "id": "A1-004",
  "name": "Venusaur ex",
  "localId": "004",
  "category": "Pokemon",
  "set": {
    "id": "A1",
    "name": "Dominação Genética"
  },
  "rarity": "Four Diamond",
  "cardImage": "/assets/cardImage/pt_BR/A1/A1-004_card.png",
  "artworkImage": "/assets/artworkImage/A1/A1-004_artwork.png",
  "illustrator": "PLANETA CG Works",
  "hp": 190,
  "types": [ "Grass" ],
  "stage": "Stage2",
  "evolveFrom": "Ivysaur",
  "isEx": true,
  "isUltraBeast": false,
  "abilities": [],
  "attacks": [
    {
      "cost": [ "Grass", "Colorless", "Colorless" ],
      "name": "Folha Navalha",
      "damage": { "value": 60, "modifier": null },
      "effect": null
    }
  ],
  "weaknesses": [
    { "type": "Fire", "value": "+20" }
  ],
  "rules": [ "Quando um Pokémon-ex é Nocauteado, seu oponente pega 2 pontos." ],
  "retreat": [ "Colorless", "Colorless", "Colorless" ],
  "description": ""
}
```

---

## Sugestões e Relatório de Erros

Se encontrar algum erro nos dados ou tiver sugestões para melhorar a API, sinta-se à vontade para abrir uma [**Issue**](https://github.com/Auriosh/ptcgp-api/issues) no repositório do GitHub.

## Licença

Este projeto é distribuído sob a **Licença MIT**. Veja o ficheiro [**LICENSE**](LICENSE) para mais detalhes.
