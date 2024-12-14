from pathlib import Path
from functools import partial

import pandas as pd
import matplotlib.pyplot as plt

import dataset
from plot import plot_ecg, save_as_png
from sample import get_samples_paths, load_hea, load_mat, load_sample


DATA_DIR = Path('./data/samples')
SNOMED_DIR = Path('./data/snomed_mappings')
RELEVANT_SNOMED_CSV = 'relevant_SNOMED_mappings.csv'
SAMPLE_RATE = 500  # [Hz]

dataset.download_kaggle_datasets(DATA_DIR)
dataset.download_snomed_mappings(SNOMED_DIR) 
dataset.create_relevant_snomed_mappings(SNOMED_DIR, RELEVANT_SNOMED_CSV)

samples_paths = get_samples_paths(DATA_DIR, limit_sample_length=5000)
snomed = pd.read_csv(SNOMED_DIR / RELEVANT_SNOMED_CSV, index_col='code')
code_to_desc = partial(dataset.code_to_description, snomed=snomed)
desc_to_code = partial(dataset.description_to_code, snomed=snomed)
relevant_codes = snomed.index.to_list()


# Find a sample with myocardial ischemia and plot it.
for path in samples_paths:
    header = load_hea(path)
    all_codes = header.codes
    filtered_labels = header.filtered_codes(relevant_codes)
    if not filtered_labels:
        continue
    data = load_mat(path)

    if desc_to_code('myocardial ischemia') in filtered_labels and len(filtered_labels) == 1:
        plot_ecg(data/1000, SAMPLE_RATE)
        plt.show()
        break
