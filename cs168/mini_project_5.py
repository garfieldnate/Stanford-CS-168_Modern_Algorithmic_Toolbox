import zipfile
from pathlib import Path
from typing import List, Tuple

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


def load_analogy_data() -> List[Tuple]:
    """Returns list of 4-tuples of words: a is to b as c is to d"""
    analogies = []
    with open(
        Path(__file__).parents[1] / "materials" / "Week 5" / "analogy_task.txt"
    ) as f:
        for line in f.readlines():
            line = line.strip()
            words = line.split()
            assert len(words) == 4
            analogies.append(tuple(words))

    return analogies
