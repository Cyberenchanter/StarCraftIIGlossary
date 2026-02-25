import os
from config import *

global_text = set()
glossary = {}

def is_term(text):
    if SOURCE_LANGUAGE != "zhcn" and SOURCE_LANGUAGE != "zhtw":
        return len(text.split()) <= 5 and len(text) > 2
    else:
        return len(text) <= 10 and text.isascii() == False


def parse_file(filename, lang_code):
    idx = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('\ufeff'):
                line = line[1:]
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
                    if id in glossary:
                        print(f"Warning: Duplicate entry for {id} in {filename}. Previous text: {glossary[id][SOURCE_LANGUAGE]}, New text: {text}")
                        continue
                    if ALLOW_DUPLICATE_SOURCE:
                        glossary[id] = {SOURCE_LANGUAGE: text}
                        idx += 1
                    else:
                        if text in global_text:
                            print(f"Warning: Duplicate text for {id} in {filename}. Text: {text}")
                            continue
                        glossary[id] = {SOURCE_LANGUAGE: text}
                        global_text.add(text)
                        idx += 1
            else:
                if id in glossary:
                    if lang_code in glossary[id]:
                        print(f"Warning: Duplicate entry for {id} in {filename}. Previous text: {glossary[id][lang_code]}, New text: {text}")
                        continue
                    glossary[id][lang_code] = text
                    idx += 1
    
    print(f"Parsed {idx} terms from {filename}")

if __name__ == "__main__":
    for mod in MOD_LIST:
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
    if TERM_ONLY:
        output_path += "_term_only"
    if ALLOW_DUPLICATE_SOURCE:
        output_path += "_multi_translation"
    if os.path.exists(output_path):
        #remove all files in output_path
        for filename in os.listdir(output_path):
            file_path = os.path.join(output_path, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        os.mkdir(output_path)

    for lang in LANGUAGE_LIST:
        with open(os.path.join(output_path, f"{lang}.ini"), 'w', encoding='utf-8') as f:
            f.write("[default]\n")
            for id, translations in glossary.items():
                if lang in translations:
                    f.write(f"{id}={translations[lang]}\n")

