import os
from config import *

global_text = {}
local_id = {}

def is_term(text):
    if SOURCE_LANGUAGE != "zhcn" and SOURCE_LANGUAGE != "zhtw":
        return len(text.split()) <= 1 and len(text) >= 2
    else:
        return len(text) <= 10 and text.isascii() == False


def parse_file(filename, lang_code):
    idx = 0
    with open(filename, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0 or line.startswith('//'):
                continue
            try:
                id, text = line.split('=', 1)
                text = text.split('///')[0].strip()
            except ValueError:
                print(f"Warning: Skipping malformed line in {filename}: {line}")
                continue
            
            if len(text) <= 0:
                continue
            if(lang_code == SOURCE_LANGUAGE):
                if(id in ID_BLACKLIST):
                    continue
                if(id in ID_WHITELIST or is_term(text) or not TERM_ONLY):
                    if id in local_id:
                        print(f"Warning: Duplicate ID {id} in {filename}. Previous text: {local_id[id]}, New text: {text}")
                        continue
                    local_id[id] = text
                    global_text[text] = {}
                    idx += 1
            else:
                if id in local_id:
                    src_text = local_id[id]
                    if src_text not in global_text:
                        print(f"Warning: Source text {src_text} for ID {id} not found in global_text. This should not happen.")
                        continue
                    if lang_code not in global_text[src_text]:
                        global_text[src_text][lang_code] = {}
                    if text not in global_text[src_text][lang_code]:
                        global_text[src_text][lang_code][text] = []
                    global_text[src_text][lang_code][text].append(id)
                    idx += 1
    
    print(f"Parsed {idx} terms from {filename}")

def finialize_output_list(target_lang):
    output_list = []
    abandoned_list = []
    for src_text, translations in global_text.items():
        if ALLOW_DUPLICATES:
            for target_text, ids in translations.get(target_lang, {}).items():
                output_list.append((src_text, target_text))
        else:
            if len(translations.get(target_lang, {})) > 1:
                for t, ids in translations.get(target_lang, {}).items():
                    abandoned_list.append((src_text, t, len(ids)))
            else:
                target_text = list(translations.get(target_lang, {}).keys())[0] if len(translations.get(target_lang, {})) > 0 else ""
                if target_text != "":
                    output_list.append((src_text, target_text))
    
    if not ALLOW_DUPLICATES:
        with open(os.path.join(output_path, f"{target_lang}_abandoned.tsv"), 'w', encoding='utf-8') as f:
            for src_text, t, count in abandoned_list:
                f.write(f"{src_text}\t{t}\t{count}\n")
            
    return output_list
if __name__ == "__main__":
    if OUTPUT_FORMAT not in ["ini", "tsv"]:
        print(f"Error: Invalid output format {OUTPUT_FORMAT}. Must be 'ini' or 'tsv'.")
        exit(1)
    for mod in reversed(MOD_LIST):
        local_id = {}
        path = os.path.join("mods", mod, f"{SOURCE_LANGUAGE}.sc2data", "localizeddata", "gamestrings.txt")
        if not os.path.exists(path):
            print(f"Warning: {path} does not exist")
            continue
        parse_file(path, SOURCE_LANGUAGE)
        for lang in LANGUAGE_LIST:
            if lang == SOURCE_LANGUAGE:
                continue
            path = os.path.join("mods", mod, f"{lang}.sc2data", "localizeddata", "gamestrings.txt")
            if not os.path.exists(path):
                print(f"Warning: {path} does not exist")
                continue
            parse_file(path, lang)
    
    output_path = f"glossary_{SOURCE_LANGUAGE}"
    if OUTPUT_FORMAT == "tsv":
        output_path += "_tsv"
    if TERM_ONLY:
        output_path += "_term_only"
    if ALLOW_DUPLICATES:
        output_path += "_multi_translation"
    if os.path.exists(output_path):
        #remove all files in output_path
        for filename in os.listdir(output_path):
            file_path = os.path.join(output_path, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        os.mkdir(output_path)

    if OUTPUT_FORMAT == "tsv":
        for lang in LANGUAGE_LIST:
            if lang == SOURCE_LANGUAGE:
                continue
            output_list = finialize_output_list(lang)
            with open(os.path.join(output_path, f"{lang}.tsv"), 'w', encoding='utf-8') as f:
                for src_text, target_text in output_list:
                    src_text = src_text.replace('\t', ' ')
                    target_text = target_text.replace('\t', ' ')
                    f.write(f"{src_text}\t{target_text}\n")
    else:
        print(f"Unsupported output format {OUTPUT_FORMAT}.")

