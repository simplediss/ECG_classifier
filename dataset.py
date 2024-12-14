import os
import shutil
import pandas as pd
from time import perf_counter
from pathlib import Path

import kagglehub
from loguru import logger


def _move_files(source_dir: str, target_dir: Path, extensions=('.hea', '.mat')) -> None:
    """Move all .hea and .mat files from source directory to target directory."""
    os.makedirs(target_dir, exist_ok=True)
    for root, _, files in os.walk(source_dir):
        for file_ in files:
            if file_.endswith(extensions):
                source_file = os.path.join(root, file_)
                target_file = os.path.join(target_dir, file_)
                shutil.move(source_file, target_file)


def download_kaggle_dataset(name: str, data_dir: Path) -> None:
    """Download a Kaggle dataset to the specified directory."""
    simplified_name = name.split('/')[-1].replace('-', '_')
    dataset_dir = data_dir / simplified_name
    if dataset_dir.exists():
        num_samples = len(list(dataset_dir.glob('*'))) // 2
        logger.info(f'Dataset {simplified_name} with {num_samples:,} samples already downloaded')
        return

    t0 = perf_counter()
    temp_path = kagglehub.dataset_download(name)
    _move_files(temp_path, dataset_dir)
    shutil.rmtree(temp_path)
    num_samples = len(list(dataset_dir.glob('*'))) // 2
    dt = f'{perf_counter() - t0:.0f} seconds'
    logger.info(f'Dataset {simplified_name} with {num_samples:,} samples downloaded ({dt})')


def download_kaggle_datasets(data_dir: Path) -> None:
    """Download ECG datasets from Kaggle to the specified directory."""
    datasets_names = [
        'bjoernjostein/china-physiological-signal-challenge-in-2018',
        'bjoernjostein/china-12lead-ecg-challenge-database',
        'bjoernjostein/georgia-12lead-ecg-challenge-database',
        'bjoernjostein/ptb-diagnostic-ecg-database',
        'bjoernjostein/ptbxl-electrocardiography-database',
        'bjoernjostein/st-petersburg-incart-12lead-arrhythmia-database',
    ]
    for name in datasets_names:
        download_kaggle_dataset(name, data_dir)


def download_snomed_mappings(snomed_dir: Path) -> None:
    if snomed_dir.exists():
        logger.info(f'SNOMED mappings already downloaded')
        return

    os.makedirs(snomed_dir, exist_ok=True)
    path = kagglehub.dataset_download("bjoernjostein/physionet-snomed-mappings")
    shutil.move(path + '/SNOMED_mappings_scored.csv', snomed_dir)
    shutil.move(path + '/SNOMED_mappings_unscored.csv', snomed_dir)
    shutil.rmtree(path)
    logger.info(f'SNOMED mappings downloaded')


def create_relevant_snomed_mappings(snomed_dir: Path, csv_name: str) -> None:
    csv_path = snomed_dir / csv_name
    if csv_path.exists():
        logger.info(f'Relevant SNOMED mappings already created')
        return

    os.makedirs(snomed_dir, exist_ok=True)
    code_to_str = {
        '54329005': 'anterior myocardial infarction',
        '57054005': 'acute myocardial infarction',
        '164861001': 'myocardial ischemia',
        '164865005': 'myocardial infarction',
        '164931005': 'st elevation',
        '413444003': 'acute myocardial ischemia',
        '425419005': 'inferior ischaemia',
        '425623009': 'lateral ischaemia',
        '426434006': 'anterior ischemia',
        '59931005': 't wave inversion',
        '251259000': 'high t-voltage'
    }

    df = pd.DataFrame(code_to_str, index=[0])
    df = df.T.sort_index()
    df.index.name = 'code'
    df.rename(columns={0: 'desc'}, inplace=True)
    df.to_csv(csv_path)
    logger.info(f'Relevant SNOMED mappings created')


def code_to_description(code: int, snomed: pd.DataFrame) -> str:
    """Convert a SNOMED code to its description from the relevant snomed df."""
    return snomed.loc[code, 'desc']


def description_to_code(description: str, snomed: pd.DataFrame) -> int:
    """Convert a SNOMED description to its code from the relevant snomed df."""
    return snomed[snomed['desc'] == description].index.item()
