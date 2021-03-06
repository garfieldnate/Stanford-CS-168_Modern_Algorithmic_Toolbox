import zipfile
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from PIL import Image

MATERIALS = Path(__file__).parents[1] / "materials" / "Week 5"

ZIP_FILE = MATERIALS / "co_occur.csv.zip"
DATA_DIR = ZIP_FILE.with_suffix("")
DIC_FILE = MATERIALS / "dictionary.txt"
ALICE_FILE = MATERIALS / "p5_image.gif"


def load_co_occurence_data():
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
        zip_ref.extractall(ZIP_FILE.parents[0])

    co_occurrences = pd.read_csv(ZIP_FILE.with_suffix(""), header=None, sep=",")
    dictionary = pd.read_csv(DIC_FILE, header=None).squeeze()

    return co_occurrences, dictionary


def load_analogy_data() -> List[Tuple]:
    """Returns list of DataFrame with columns a, b, c and d: a is to b as c is to d"""
    analogies = []
    with open(
        Path(__file__).parents[1] / "materials" / "Week 5" / "analogy_task.txt"
    ) as f:
        for line in f.readlines():
            line = line.strip()
            words = line.split()
            assert len(words) == 4
            analogies.append(list(words))

    return pd.DataFrame(analogies, columns=["a", "b", "c", "d"])


def load_alice() -> np.matrix:
    """Load the example "Alice" picture as a numpy matrix.
    Code taken from https://www.frankcleary.com/svdimage/"""
    image = Image.open(ALICE_FILE)
    image_np = np.array(list(image.getdata(band=0)), float)
    image_np.shape = (image.size[1], image.size[0])
    image_np = np.matrix(image_np)
    return image_np
