# Guarde este ficheiro como: build_api.py (na raiz do seu projeto)

import json
import os
import re
import requests
import sys
import time

# --- Configurações ---
SET_IDS_TO_PROCESS = ['A1', 'A1a', 'A2', 'A2a', 'A2b', 'A3', 'A3a', 'P-A']
LANGUAGE_CODES = ['pt-br', 'en', 'es', 'fr', 'de', 'it', 'ja', 'ko', 'zh-tw'] 
API_BASE_URL = "https://api.tcgdex.net/v2"
BASE_OUTPUT_DIR = 'docs'
ASSETS_BASE_DIR = 'assets'

# --- Funções de Conversão ---

def parse_damage(damage_input):
    """
    Converte um valor de dano (que pode ser string ou int) para um objeto estruturado.
    """
    if isinstance(damage_input, int):
        damage_str = str(damage_input)
    else:
        damage_str = damage_input

    if not damage_str:
        return {'value': None, 'modifier': None}
    
    match = re.match(r'(\d+)([+x×]?)', damage_str)
    if match:
        value = int(match.group(1))
        modifier = match.group(2) if match.group(2) else None
        if modifier == '×': modifier = 'x'
        return {'value': value, 'modifier': modifier}
    return {'value': None, 'modifier': None}

def parse_retreat(retreat_cost):
    if isinstance(retreat_cost, int) and retreat_cost > 0:
        return ["Colorless"] * retreat_cost
    return []

def get_language_code(api_lang):
    """Converte o código de idioma da API para o nosso padrão."""
    lang_map = {
        'pt-br': 'pt_BR', 'en': 'en_US', 'es': 'es_ES', 'fr': 'fr_FR',
        'de': 'de_DE', 'it': 'it_IT', 'ja': 'ja_JP', 'ko': 'ko_KR', 'zh-tw': 'zh_TW'
    }
    return lang_map.get(api_lang, api_lang)

def print_progress_bar(iteration, total, prefix = '', suffix = '', length = 50, fill = '█'):
    """
    Gera e exibe uma barra de progresso no terminal.
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

# --- Função Principal ---

def build_api_data():
    """
    Busca dados da API, processa-os e constrói a estrutura final de pastas
    e ficheiros JSON para a API na pasta /docs.
    """
    print("🚀 Iniciando a construção dos dados da API...")
    
    total_cards_processed = 0
    total_cards_skipped = 0

    for lang in LANGUAGE_CODES:
        lang_code_standard = get_language_code(lang)
        print(f"\n🌐 Processando idioma: {lang_code_standard}")
        
        all_sets_for_lang = []

        for set_id in SET_IDS_TO_PROCESS:
            print(f"  - Buscando índice de cartas para o set: {set_id}...")
            
            set_url = f"{API_BASE_URL}/{lang}/sets/{set_id}"
            
            try:
                response = requests.get(set_url, timeout=15)
                if response.status_code == 404:
                    print(f"    ℹ️  Set '{set_id}' não encontrado para o idioma {lang_code_standard}. Pulando.")
                    continue
                response.raise_for_status()
                set_data = response.json()
                card_index = set_data.get('cards', [])
            except requests.exceptions.RequestException as e:
                print(f"    ❌ Erro ao buscar o índice do set {set_id}: {e}")
                continue
            
            if not card_index:
                print(f"    ⚠️  Aviso: O set '{set_id}' foi encontrado, mas não continha nenhuma carta na resposta da API.")
                continue

            all_sets_for_lang.append({
                "id": set_data.get("id"), "name": set_data.get("name"),
                "logo": f"/{ASSETS_BASE_DIR}/logoImage/{lang_code_standard}/logo_{set_data.get('id')}_{lang_code_standard}.png"
            })
            
            cards_processed_in_set = 0
            cards_skipped_in_set = 0
            total_cards_in_set = len(card_index)
            
            for i, card_info in enumerate(card_index):
                card_id = card_info.get('id')
                if not card_id: continue

                # --- LÓGICA DE VERIFICAÇÃO ---
                target_dir = os.path.join(BASE_OUTPUT_DIR, 'v1', 'cards', lang_code_standard, set_id)
                card_filename = os.path.join(target_dir, f"{card_id}.json")

                # Atualiza a barra de progresso
                progress_prefix = f"    Processando '{set_id}'"
                print_progress_bar(i + 1, total_cards_in_set, prefix=progress_prefix, suffix="Completo", length=40)

                # Se o ficheiro já existe, pula para o próximo
                if os.path.exists(card_filename):
                    cards_skipped_in_set += 1
                    total_cards_skipped += 1
                    continue

                try:
                    card_url = f"{API_BASE_URL}/{lang}/cards/{card_id}"
                    card_response = requests.get(card_url, timeout=10)
                    if card_response.status_code == 404: continue
                    card_response.raise_for_status()
                    old_card = card_response.json()
                except requests.exceptions.RequestException:
                    continue

                new_card = {
                  "language": lang_code_standard, "id": card_id, "name": old_card.get('name', ''),
                  "localId": old_card.get('localId', ''), "category": old_card.get('category', 'Pokemon'),
                  "set": {"id": set_id, "name": set_data.get('name', '')},
                  "rarity": old_card.get('rarity', ''),
                  "cardImage": f"/{ASSETS_BASE_DIR}/cardImage/{lang_code_standard}/{set_id}/{card_id}_card.png",
                  "artworkImage": f"/{ASSETS_BASE_DIR}/artworkImage/{set_id}/{card_id}_artwork.png",
                  "illustrator": old_card.get('illustrator', ''), "hp": old_card.get('hp'),
                  "types": old_card.get('types', []), "stage": old_card.get('stage', 'Basic'),
                  "evolveFrom": old_card.get('evolveFrom'), "isEx": old_card.get('suffix') == 'EX',
                  "isUltraBeast": 'Ultra Beast' in old_card.get('description', '') if old_card.get('description') else False,
                  "abilities": old_card.get('abilities', []),
                  "attacks": [{"cost": a.get('cost',[]), "name": a.get('name',''), "damage": parse_damage(a.get('damage')), "effect": a.get('effect','')} for a in old_card.get('attacks',[])],
                  "weaknesses": old_card.get('weaknesses', []), "rules": [],
                  "retreat": parse_retreat(old_card.get('retreat')), "description": old_card.get('description', '')
                }

                if new_card["isEx"]: new_card["rules"].append("Quando um Pokémon-ex é Nocauteado, seu oponente pega 2 pontos.")

                os.makedirs(target_dir, exist_ok=True)
                with open(card_filename, 'w', encoding='utf-8') as f: json.dump(new_card, f, ensure_ascii=False, indent=2)
                
                total_cards_processed += 1
                cards_processed_in_set += 1
                time.sleep(0.05)
            
            print() 
            print(f"    ✅ Set '{set_id}' em '{lang_code_standard}' processado ({cards_processed_in_set} novas cartas salvas, {cards_skipped_in_set} já existentes).")

        if all_sets_for_lang:
            sets_index_path = os.path.join(BASE_OUTPUT_DIR, 'v1', 'cards', lang_code_standard, 'sets.json')
            os.makedirs(os.path.dirname(sets_index_path), exist_ok=True)
            with open(sets_index_path, 'w', encoding='utf-8') as f: json.dump(all_sets_for_lang, f, ensure_ascii=False, indent=2)
            print(f"  - ✅ Ficheiro de índice 'sets.json' para '{lang_code_standard}' criado.")

    print(f"\n🎉 Processo concluído! {total_cards_processed} novos registros foram criados, {total_cards_skipped} já existiam.")

if __name__ == '__main__':
    build_api_data()
