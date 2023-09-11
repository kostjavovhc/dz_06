import sys
from pathlib import Path
import re
import shutil

CATEGORIES = {"Photoes": [".jpeg", ".png", ".jpg", ".svg"],
              "Docs": [".docx", ".doc", ".txt", ".pdf", ".xls", ".xlsx", ".pptx"],
              "Videos": [".avi", ".mp4", ".mov", ".mkv"],
              "Music": [".mp3", ".ogg", ".wav", ".amr"],
              "Archieves": ['.zip', '.gz', '.tar'],
              "Others": []
              }

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {} 
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def get_category(file:Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Others"


#функція перейменування, вставив її код напряму в move_file
def normalize_file(file:str) -> str:
    new = Path(file).name.translate(TRANS)
    file = re.sub(Path(file).name, new, str(file))
    re.sub(r"[^a-zA-Z0-9]", "_", Path(file).name)
    print(file)
    return file
    


def move_file(file: Path, category: str, root_dir:Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(file.name))


#MY UNPACK FUNCTION
#def unpack(file:Path) -> None:
#    for element in file.joinpath("Archieves").glob("**/*"):
#        if element.is_file() and element.suffix in CATEGORIES["Archieves"]:
#            shutil.unpack_archive(file.joinpath(element.name), file.joinpath(element.stem))

def unpack(file:Path) -> None:
    try:
        #for e in file.glob('*Archives\*'):
        #    if e.is_file() and e.suffix in CATEGORIES["Archieves"]:
        #        shutil.unpack_archive(file.joinpath(e.name), file.joinpath(e.stem))
        for elem in file.glob('*Archives\*'):
            new_folder = file.parent.joinpath(file.stem)
            shutil.unpack_archive(elem, new_folder)
    except shutil.ReadError:
        return None
    

def sort_folder(path:Path, elements=[]) -> None:
    #РЕКУРСИВНИЙ МЕТОД
    #for i in path.iterdir():
    #    if i.is_dir():
    #        sort_folder(i, elements)
    #    else:
    #        elements.append(i)
    #return elements

    for element in path.glob("**/*"):
        if element.is_file():
            category = get_category(element)
            move_file(element, category, path)
            normalize_file(element)
            unpack(element)
        elif element.is_dir():
            if element.name in CATEGORIES:
                continue
            else:
                shutil.rmtree(element)



def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return "Folder does not exist"
    
    sort_folder(path)
    
    #unpack(path)

    return "All ok"

if __name__ == "__main__":
    print(main())