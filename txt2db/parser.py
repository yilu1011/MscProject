import logging
import os
import re

from itertools import chain

from Information import Information
from utils import get_spaces

NEW_PAGE = r'^p\.[0-9]+\W*(recto|verso)'
NEW_INFORMATION = r'(\n|^)\W*[0-9]+\.'
NEW_DOCUMENT_SPLIT = r"(?=\nDocument [0-9]+[\n:])"
INFORMATION_CONTINUE = r'(\n|^)\W\W\W\W+\w'


def cleaned(document: str):
    document = re.sub(
        r'\W*\-+\W*[0-9]+ *(?=\n[tT]ype)',
        r'',
        document
    )
    document = re.sub(
        NEW_PAGE + r'[ \t]*\n(?=\w)',
        r' ',
        document
    )
    document = re.sub(r'"', r'\'', document)
    return document

def parse_document(document: str, carton_id: int):
    document = cleaned(document)
    lines = document.split('\n')
    informations = []
    information_id = 1
    base_info = Information({"carton": carton_id})

    for line in lines:
        for dim in Information.dimensions:
            if re.match(f'^\W*{dim}[\w\W]*:\W*\w', line.strip().lower()):
                try:
                    base_info[dim] = line.split(":")[1].strip()
                except Exception as e:
                    logging.debug(base_info)
                    logging.debug(line)
                    raise e
                information_id = 1
                continue

        if re.match(NEW_INFORMATION, line):
            info = Information(base_info)
            info["numéro"] = information_id
            info["résumé"] = line
            info["espace_mentioné"] = get_spaces(line)
            informations.append(info)
            information_id += 1
            continue
        
        if re.match(INFORMATION_CONTINUE, line):
            if informations:
                informations[-1]["résumé"] += " " + line.strip()
                informations[-1]["espace_mentioné"].update(get_spaces(line))

    return informations

def parse_file(filepath: str):
    with open(filepath, 'r+', encoding="utf-8") as file:
        file = file.read().strip()
        carton_id, corps = re.split(r'\n', file, maxsplit=1)
        
        # Extrait l'ID du carton
        carton_id = int(carton_id.split(' ')[1].strip())
        logging.info(f"\nCarton {carton_id}")

        # Extrait la liste des documents transcripts dans le carton
        documents = re.split(NEW_DOCUMENT_SPLIT, corps)
        documents = list(filter(
            lambda doc: not doc.lower().strip().startswith("contents"),
            documents
        ))
        logging.info(f"{len(documents)} document(s) dans le carton.")

        informations = []
        for document in documents:
            informations.extend([
                information
                for information in parse_document(document, carton_id)
            ])

        return informations

def parse_folder(folderpath: str):
    files = os.listdir(folderpath)
    logging.info(f"\n{len(files)} fichier(s) trouvé(s).")

    informations = list(chain.from_iterable([
        parse_file(folderpath + filename)
        for filename in files
    ]))

    logging.info(f"{len(informations)} information(s) au total.")
    return informations