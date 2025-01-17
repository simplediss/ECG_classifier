import shutil
from pathlib import Path
from functools import partial

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

import dataset
from plot import plot_ecg, save_as_png
from sample import get_samples_paths, load_hea, load_mat, load_sample


DATA_DIR = Path('./data/samples')
SNOMED_DIR = Path('./data/snomed_mappings')
RELEVANT_SNOMED_CSV = 'relevant_SNOMED_mappings.csv'
SAMPLE_RATE = 500  # [Hz]

# dataset.download_kaggle_datasets(DATA_DIR)
# dataset.download_snomed_mappings(SNOMED_DIR) 
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

    if desc_to_code('sinus rhythm') in filtered_labels and len(filtered_labels) >2:
        plot_ecg(data/1000, SAMPLE_RATE)
        save_as_png(f'./t_wave_dx1/{path.name}')
        # save_as_png(f'./{path.name}')
        break


# plots_dir = Path('./data/plots_for_classification')
# plots_dir.mkdir(exist_ok=True)
# relevant_dir = Path('./data/relevant_samples_data')
# relevant_dir.mkdir(exist_ok=True)

# for path in tqdm(samples_paths):
#     header = load_hea(path)
#     all_codes = header.codes
#     filtered_labels = header.filtered_codes(relevant_codes)
#     if not filtered_labels:
#         continue
#     data = load_mat(path)

#     curr_mat_path = path.with_stem(path.name + '.mat')
#     curr_hea_path = path.with_stem(path.name + '.hea')
#     shutil.copy(curr_mat_path, relevant_dir / curr_mat_path.name)
#     shutil.copy(curr_hea_path, relevant_dir / curr_hea_path.name)

#     plot_ecg(data/1000, SAMPLE_RATE)
#     save_as_png(f'{plots_dir}/{path.name}')









# path = Path('data\samples\georgia_12lead_ecg_challenge_database\E00180')
# header = load_hea(path)
# all_codes = header.codes
# filtered_labels = header.filtered_codes(relevant_codes)
# data = load_mat(path)
# plot_ecg(data[:,:2500]/1000, SAMPLE_RATE)
# save_as_png(f'./{path.name}')

# count = 0
# line_counts = {}
# Find a sample with myocardial ischemia and plot it.
# for path in samples_paths:
#     header = load_hea(path)
#     all_codes = header.codes
#     filtered_labels = header.filtered_codes(relevant_codes)
#     if not filtered_labels:
#         continue
#     data = load_mat(path)

#     if len(filtered_labels) == 1:
#         if desc_to_code('t wave inversion') in filtered_labels:
#             if(len(all_codes)>1):
#                 print(path)
#                 count+=1
#                 plot_ecg(data[:,:2500]/1000, SAMPLE_RATE)
#                 # save_as_png(f'./t_wave_dx1/{path.name}')
#                 # plt.show()
#             if count==11:
#                 break
#         # line = " | ".join(code_to_desc(label) for label in filtered_labels)
#         # if line not in line_counts:
#         #     line_counts[line] = 1
#         # else:
#         #     line_counts[line] += 1



# for path in samples_paths:
#     header = load_hea(path)
#     filtered_labels = header.filtered_codes(relevant_codes)
    
#     if not filtered_labels:
#         continue

#     data = load_mat(path)
#     if desc_to_code('acute myocardial infarction') in filtered_labels:
#         count+=1

# print(count)
    # if not filtered_labels:  # Skip samples with no relevant labels
    #     continue

    # data = load_mat(path)
    # if len(header.codes) == 0:  
    #     print(path)  
             


    # data = load_mat(path)
    # flag=0
    # if len(filtered_labels) == 2 and desc_to_code('lateral ischaemia') in filtered_labels:  
    #     for label in filtered_labels:
    #         if label == desc_to_code('lateral ischaemia'):
    #             flag+=1
    #     if flag==2:
    #             print(path)  
    #     flag=0     
        
#         line = " | ".join(code_to_desc(label) for label in filtered_labels)
        
#         # Update count
#         if line not in line_counts:
#             line_counts[line] = 1
#             print(line)  # Print the line only the first time
#         else:
#             line_counts[line] += 1

# print("***")

# # Print counts at the end
# print(sum([len(k) for k in line_counts.keys()]))
# print("Line Appearance Counts:")
# for line, count in line_counts.items():
#     print(f"{line} \t\t\t-> {count} samples")
    
