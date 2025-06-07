import os
import re

def rename_images_in_batch():
    """
    Ferramenta interativa para renomear arquivos de imagem em uma pasta específica
    de forma sequencial e padronizada, dentro de um intervalo definido e com tipo de imagem escolhido.
    """
    
    # Passo 1: Obter o caminho da pasta do usuário
    folder_path = input("➡️  Por favor, arraste ou cole o caminho da pasta com as imagens e pressione Enter: ").strip().replace("'", "").replace('"', '')

    if not os.path.isdir(folder_path):
        print(f"❌ Erro: O diretório '{folder_path}' não foi encontrado ou não é uma pasta válida.")
        return

    # Passo 2: Listar e ordenar os arquivos de imagem
    try:
        valid_extensions = ('.png', '.jpg', '.jpeg')
        image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)])
    except OSError as e:
        print(f"❌ Erro ao acessar a pasta: {e}")
        return

    if not image_files:
        print("ℹ️  Nenhuma imagem (.png, .jpg, .jpeg) encontrada na pasta.")
        return

    print(f"\n✅ {len(image_files)} imagens encontradas e ordenadas alfabeticamente.")

    # Passo 3: Perguntar o tipo de imagem a ser processado
    while True:
        image_type_input = input("➡️  Este lote é de 'card' (c) ou 'artwork' (a)? ").lower().strip()
        if image_type_input in ['c', 'card']:
            image_type_suffix = 'card'
            break
        elif image_type_input in ['a', 'artwork']:
            image_type_suffix = 'artwork'
            break
        else:
            print("❌ Resposta inválida. Por favor, digite 'c' para card ou 'a' para artwork.")
            
    # Passo 4: Obter informações de renomeação
    set_prefix = input("➡️  Digite o prefixo do set (ex: A1, A2b, P-A): ").strip()
    
    while True:
        try:
            start_number = int(input("➡️  Digite o número da carta inicial (ex: 1): ").strip())
            if start_number > 0:
                break
            else:
                print("❌ Por favor, insira um número maior que zero.")
        except ValueError:
            print("❌ Entrada inválida. Por favor, insira apenas um número.")

    while True:
        try:
            end_number_str = input("➡️  Digite o número da carta final (ou deixe em branco para ir até o fim): ").strip()
            if end_number_str == "":
                end_number = float('inf')
                break
            end_number = int(end_number_str)
            if end_number >= start_number:
                break
            else:
                print("❌ O número final deve ser maior ou igual ao número inicial.")
        except ValueError:
            print("❌ Entrada inválida. Por favor, insira apenas um número.")

    # Passo 5: Montar o plano de renomeação
    rename_plan = []
    current_card_number = start_number
    
    files_to_process = image_files
    if end_number != float('inf'):
        num_to_rename = end_number - start_number + 1
        if len(image_files) < num_to_rename:
            print(f"\n⚠️  Aviso: A pasta contém {len(image_files)} imagens, mas o intervalo solicitado ({num_to_rename}) é maior.")
            print("     Apenas as imagens disponíveis na pasta serão processadas.")
        files_to_process = image_files[:num_to_rename]

    for filename in files_to_process:
        formatted_number = str(current_card_number).zfill(3)
        new_filename = f"{set_prefix}-{formatted_number}_{image_type_suffix}.png"
        
        rename_plan.append((filename, new_filename))
        current_card_number += 1

    print("\n--- 🧐 Pré-visualização da Renomeação ---")
    for original, new in rename_plan:
        print(f"'{original}'  ->  '{new}'")
    
    print("------------------------------------------")
    
    while True:
        confirm = input("❓ Deseja aplicar estas alterações? (s/n): ").lower().strip()
        if confirm in ['s', 'n']:
            break
        print("❌ Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")

    # Passo 6: Executar a renomeação
    if confirm == 's':
        print("\n🚀 Renomeando arquivos...")
        renamed_count = 0
        for original, new in rename_plan:
            original_path = os.path.join(folder_path, original)
            new_path = os.path.join(folder_path, new)
            
            try:
                if os.path.exists(new_path) and original_path != new_path:
                    print(f"⚠️  Aviso: O arquivo de destino '{new}' já existe. Pulando '{original}'.")
                    continue
                
                os.rename(original_path, new_path)
                renamed_count += 1
            except OSError as e:
                print(f"❌ Erro ao renomear '{original}': {e}")
        
        print(f"\n🎉 Processo concluído! {renamed_count} arquivos foram renomeados.")
    else:
        print("\n🚫 Operação cancelada pelo usuário.")


if __name__ == '__main__':
    rename_images_in_batch()
