import zipfile
from pathlib import Path

import pandas as pd

ZIP_FILE = Path(__file__).parents[1] / "materials" / "Week 5" / "co_occur.csv.zip"
DATA_DIR = ZIP_FILE.with_suffix("")
DIC_FILE = Path(__file__).parents[1] / "materials" / "Week 5" / "dictionary.txt"


def load_co_occurence_data():
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
        zip_ref.extractall(ZIP_FILE.parents[0])

    co_occurrences = pd.read_csv(ZIP_FILE.with_suffix(""), header=None, sep=",")
    dictionary = pd.read_csv(DIC_FILE, header=None).squeeze()

    return co_occurrences, dictionary
