from Information import Information
from Inserter import Inserter
from parser import parse_folder

FOLDERPATH = "./transcriptions/"
SAVETOFILE = "./data/informations.csv"

if __name__ == "__main__":
    informations = parse_folder(FOLDERPATH)

    inserter_obj = Inserter(kind='csv', filepath=SAVETOFILE)
    inserter_obj.save(informations)