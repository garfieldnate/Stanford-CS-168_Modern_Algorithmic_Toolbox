import zipfile
from pathlib import Path

import pandas as pd

ZIP_FILE = Path(__file__).parents[1] / "materials" / "Week 4" / "p4dataset2021.txt.zip"
DATA_DIR = ZIP_FILE.with_suffix("")

# From the 1000 Genomes project readme: http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/README_populations.md
POPULATION_CODE_KEY = {
    "ACB": "African-Caribbean",
    "ASW": "African-American SW",
    "BEB": "Bengali",
    "CDX": "Dai Chinese",
    "CEU": "Utah (North/Western Europe)",
    "CHB": "Han Chinese",
    "CHD": "Denver Chinese",
    "CHS": "Southern Han Chinese",
    "CLM": "Colombian",
    "ESN": "Esan",
    "FIN": "Finnish",
    "GBR": "British",
    "GIH": "Gujarati",
    "GWD": "Gambian",
    "IBS": "Spanish",
    "ITU": "Indian",
    "JPT": "Tokyo Japanese",
    "KHV": "Kinh Vietnamese",
    "LWK": "Luhya",
    "MSL": "Mende",
    "MXL": "Mexican-American",
    "PEL": "Peruvian",
    "PJL": "Punjabi",
    "PUR": "Puerto Rican",
    "STU": "Sri Lankan",
    "TSI": "Tuscan",
    "YRI": "Yoruba",
}


def load_1000_genomes_data():
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
        zip_ref.extractall(ZIP_FILE.parents[0])

    raw_data = pd.read_csv(ZIP_FILE.with_suffix(""), header=None, sep=" ")
    ids = raw_data[0]
    sexes = raw_data[1]

    population_codes = raw_data[2]
    populations = []
    for row in population_codes:
        populations.append(POPULATION_CODE_KEY[row])
    populations = pd.Series(populations)
    genomes = raw_data.loc[:, 3:].reset_index(drop=True)
    genomes.columns = range(0, genomes.shape[1])
    return ids, sexes, populations, genomes
