import os
import mne
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import Config

data_path = Config.data_path
output_path = Config.out_path

for subject_idx in range(1, 3):
    subject_id = str(subject_idx)
    if len(subject_id) == 1:
        subject_id_full = f'0{subject_id}'
    else:
        subject_id_full = subject_id
    
    eeg_file = glob.glob(f'{data_path}/{subject_id}/EEG/*.cdt')[0]
    raw_eeg = mne.io.read_raw_curry(eeg_file, preload=True)
    event_segments = {}
    for i in range(len(raw_eeg.annotations)):
        index = int(raw_eeg.annotations[i]['onset']*1000)
        if i % 2 == 0:
            event_segments[i//2] = [index]
        else:
            event_segments[(i-1)//2].append(index)
    
    out_dir = f'{output_path}/{subject_id}/EEG/'
    os.makedirs(out_dir, exist_ok=True)
    for segment_id in event_segments:
        print(segment_id, flush = True)
        segment = event_segments[segment_id]
        df_eeg_signal = {ch_name: raw_eeg[ch_name, segment[0]:segment[1]][0].flatten() for ch_name in raw_eeg.ch_names if ch_name != 'Trigger'}
        df_tmp = pd.DataFrame.from_dict(df_eeg_signal)
        df_tmp.to_csv(f'{out_dir}/event_{segment_id}.csv.gz', index=False, compression='gzip')
    