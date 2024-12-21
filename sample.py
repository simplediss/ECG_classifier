from pathlib import Path

import numpy as np
from loguru import logger
from scipy.io import loadmat


class SampleHeader:
    def __init__(self, header_data: list[str]):
        self.header_data = header_data

    def __str__(self) -> str:
        return '\n'.join(self.header_data)
    
    def __len__(self) -> int:
        return int(self.header_data[0].split(' ')[3])
    
    @property
    def age(self) -> int:
        return int(self.header_data[13][6:])
    
    @property
    def gender(self) -> str:
        return self.header_data[14][6:]
    
    @property
    def codes(self) -> list[int]:
        codes_str = self.header_data[15][5:]
        return [int(code) for code in codes_str.split(',')]
    
    def filtered_codes(self, relevant_codes: list[int]) -> list[int]:
        filtered_codes_str = [str(code) for code in self.codes if code in relevant_codes]
        filtered_codes_str = list(sorted(set(filtered_codes_str)))
        filtered_codes_int = [int(code) for code in filtered_codes_str]
        return filtered_codes_int


def load_mat(path: Path) -> np.ndarray:
    """Load a signal .mat file into a numpy array with shape [12, N]."""
    mat_path = path if path.suffix == '.mat' else path.with_suffix('.mat')
    return np.asarray(loadmat(mat_path)['val'], dtype=np.float64)


def load_hea(path: Path) -> SampleHeader:
    """Load a header .hea file into a custom SampleHeader object."""
    hea_path = path if path.suffix == '.hea' else path.with_suffix('.hea')
    with open(hea_path, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    return SampleHeader(lines)


def load_sample(path: Path) -> tuple[np.ndarray, SampleHeader]:
    """Load a sample (signal and header)."""
    data = load_mat(path)
    header_data = load_hea(path)
    return data, header_data


def get_samples_paths(data_dir: Path, limit_sample_length: tuple | int | None = None) -> list[Path]:
    """Get a list of all sample paths in the specified data directory."""
    samples_paths = []
    dirs = [dir for dir in data_dir.iterdir() if dir.is_dir()]
    for ds_path in dirs:
        ds_samples_paths = sorted(set([i.with_suffix('') for i in ds_path.iterdir()]))
        samples_paths += list(ds_samples_paths)
    logger.info(f'Got total of {len(samples_paths):,} samples')

    if limit_sample_length:
        lengths = [len(load_hea(path)) for path in samples_paths]
        if isinstance(limit_sample_length, int):
            min_length, max_length = limit_sample_length, limit_sample_length
        else:
            min_length, max_length = limit_sample_length
        samples_paths = [path for path, length in zip(samples_paths, lengths)
                            if min_length <= length <= max_length]
        logger.info(f'Filtering samples that not satisfies: {min_length} <= length <= {max_length}')
        logger.info(f'Got total of {len(samples_paths):,} samples after filtering')

    return samples_paths
