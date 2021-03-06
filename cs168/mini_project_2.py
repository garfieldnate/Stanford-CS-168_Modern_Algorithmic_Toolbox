import zipfile
from pathlib import Path

import pandas as pd

ZIP_FILE = Path(__file__).parents[1] / "materials" / "Week 2" / "p2_data.zip"
DATA_DIR = ZIP_FILE.with_suffix("")


def load_data():
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
        zip_ref.extractall(ZIP_FILE.parents[0])

    group_names = pd.read_csv(DATA_DIR / "groups.csv", header=None, squeeze=True)
    labels = pd.read_csv(DATA_DIR / "label.csv", header=None, squeeze=True)

    # data uses 1-indexing, so update indexes to match
    group_names.index += 1
    labels.index += 1

    data = pd.read_csv(
        DATA_DIR / "data50.csv",
        header=None,
        names=["article_id", "word_id", "count"],
    ).pivot(index="article_id", columns="word_id")["count"]
    data.fillna(0, inplace=True)

    return group_names, data, labels
