# ECG_classifier


## Data

### Resources:

1. [Kaggle ECG classification 1](https://www.kaggle.com/code/ojaswayadav/ecg-based-disease-classification)
2. [Kaggle ECG classification 2](https://www.kaggle.com/code/habibmrad1983/physionet-challenge-2020/notebook)
3. [Classification of 12-lead ECGs: The PhysioNet/Computing in Cardiology Challenge 2020](https://physionet.org/content/challenge-2020/1.0.2/)

### Get Data from _Kaggle_



The data in this repo contains 43,101 ECG samples from 4 different sources.

Each sample in the dataset contains 2 files:

1. Header file (`.hea`)
2. Signal file (`.mat`)

<details>
  <summary>Dataset Sources:</summary>

1. Southeast University, China, including the data from the China Physiological Signal Challenge 2018 (2 datasets from this source)
2. St. Petersburg Institute of Cardiological Technics, St. Petersburg, Russia.
3. The Physikalisch Technische Bundesanstalt, Brunswick, Germany (2 datasets from this source).
4. Georgia 12-Lead ECG Challenge Database, Emory University, Atlanta, Georgia, USA.


</details>

<details>
  <summary>The Header File:</summary>

The header file looks like this (example of a real sample from the dataset):

```
E00001.mat 12 500 5000 05-May-2020 14:50:55
E00001.mat 16+24 4880/mV 16 0 136 -28477 0 I
E00001.mat 16+24 4880/mV 16 0 87 545 0 II
E00001.mat 16+24 4880/mV 16 0 -48 29413 0 III
E00001.mat 16+24 4880/mV 16 0 -112 -18879 0 aVR
E00001.mat 16+24 4880/mV 16 0 92 -29015 0 aVL
E00001.mat 16+24 4880/mV 16 0 19 -17384 0 aVF
E00001.mat 16+24 4880/mV 16 0 -39 10780 0 V1
E00001.mat 16+24 4880/mV 16 0 58 -22686 0 V2
E00001.mat 16+24 4880/mV 16 0 87 -24025 0 V3
E00001.mat 16+24 4880/mV 16 0 97 -26617 0 V4
E00001.mat 16+24 4880/mV 16 0 87 21518 0 V5
E00001.mat 16+24 4880/mV 16 0 78 25805 0 V6
#Age: NaN
#Sex: Female
#Dx: 426783006
#Rx: Unknown
#Hx: Unknown
#Sx: Unknown
```

* The `#Dx: 426783006` row corresponds to the SNOMED-CT code diagnose, more about it later.

</details>


<details>
  <summary>The Signal File:</summary>

* The signal file from the `.mat` file opened as a numpy array with shape `[12, N]` while N is the length of the sample.
* When reviewing the data, it can be noticed that the most common length is `5000`, and most of the samples have length lower than `10,000`. Therefore, we choose to ignore samples with length out of this range to get consistent data, and we are left with `94%` of the whole dataset.

</details>


<details>
  <summary>Dataset Structure:</summary>

```
└─ data
   ├─ dataset_name_1
   │  ├─ Q0001.hea
   │  ├─ Q0001.mat
   │  ⋮
   │  ├─ Q9999.hea
   │  └─ Q9999.mat
   ⋮
   └─ dataset_name_6
      ├─ Q0001.hea
      ├─ Q0001.mat
      ⋮
      ├─ Q9999.hea
      └─ Q9999.mat
```

</details>


<details>
  <summary>Dataset Labels:</summary>

* All diagnoses are encoded with SNOMED-CT codes. We need a CSV-file to decode them.
* (Systematized Nomenclature of Medicine -- Clinical Terms) is a standardized, multilingual vocabulary of clinical terminology that is used by physicians and other health care providers for the electronic exchange of clinical health information.

</details>
